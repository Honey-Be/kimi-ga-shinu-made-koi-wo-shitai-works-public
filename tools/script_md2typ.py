#!/usr/bin/env python3
"""시퀀스 대본 Markdown → Typst 변환기.

`out/bgm/**/script_{ko,ja}.md` 를 같은 내용의 `.typ` 로 옮긴다.
**같은 변환기를 두 언어에 쓰므로 .typ 는 .md 와 자동으로 록스텝이 된다** —
구조가 어긋나면 그것은 .md 쪽에서 이미 어긋난 것이다.

    python3 tools/script_md2typ.py out/bgm/12_…/script_ko.md
    python3 tools/script_md2typ.py out/bgm/12_…/script_*.md --check

`--check` 는 쓰지 않고 대조만 한다(생성물이 최신인지).

**손으로 쓴 .typ 는 건너뛴다.** 생성물에는 머리에 「생성물 — 손으로 고치지 않는다」
표지가 있고, 그 표지가 없는 .typ 는 이 생성기가 생기기 전에 손으로 쓴 파일이다
(〈비창〉 1악장 대본이 그렇다). 그런 파일은 대조에서도 빼고 덮어쓰지도 않는다 —
`proposals/P75` 5절, 제안자의 결정.

다루는 것 — 제목/소제목 · **굵게** · _(기울임 괄호)_ · `코드` · > 인용 블록 ·
표 · --- 구분선 · 글머리표 · 번호 목록.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

LANG = {"ko": "ko", "ja": "ja"}
FONT_NOTE = (
    "// 컴파일: typst compile --font-path /usr/share/fonts/noto-cjk "
    "--font-path /usr/share/fonts/nanum {name}"
)

PREAMBLE = """// {title}
// 생성물 — 손으로 고치지 않는다. 원본은 {src} 이며 `tools/script_md2typ.py` 가 옮긴다.
{fontnote}
#set page(paper: "a4", margin: (x: 2cm, y: 2.2cm))
#set text(lang: "{lang}", size: 10pt)
#set par(justify: false, leading: 0.7em)
#set heading(numbering: none)
#set table(inset: 5pt, stroke: 0.4pt)
#show table: set text(size: 8.5pt)
#show table.cell.where(y: 0): strong
#show quote.where(block: true): set block(inset: (left: 1.2em, y: 0.4em))
#show heading.where(level: 4): set block(above: 1.4em, below: 0.7em)
"""


def esc(t: str) -> str:
    """Typst 에서 뜻을 갖는 글자를 막는다 — 인라인 마크업을 처리하기 *전*에 부른다."""
    return t.replace("\\", "\\\\").replace("#", "\\#").replace("$", "\\$").replace("@", "\\@")


def _scan(t: str, splits: frozenset[int]) -> tuple[list[str], int, int, list[int]]:
    """한 줄을 훑는다. splits 는 「닫기+열기로 쪼갤 ** 묶음」의 시작 위치."""
    out: list[str] = []
    i = 0
    n = len(t)
    strong = emph = 0  # 열린 #strong[…] · #emph[…] 수
    closed = False  # 직전 토막이 함수 닫는 괄호로 끝났나
    cands: list[int] = []  # 닫기+열기로 쪼갤 후보 — 행이 안 균형 잡힐 때 쓴다
    while i < n:
        c = t[i]
        prev = t[i - 1] if i else ""
        if c == "`":
            j = t.find("`", i + 1)
            if j == -1:  # 짝 없는 백틱 — 글자대로 둔다
                out.append(esc("`"))
                i += 1
            else:
                out.append("#raw(" + typ_str(t[i + 1 : j]) + ")")
                i = j + 1
                closed = True
        elif t[i : i + 2] == "**" and i not in splits:
            flanked = prev and not prev.isspace() and i + 2 < n and not t[i + 2].isspace()
            if flanked and not strong and emph:
                cands.append(i)
            if strong and prev and not prev.isspace():
                out.append("]")
                strong -= 1
                closed = True
            else:
                out.append("#strong[")
                strong += 1
                closed = False
            i += 2
        elif c == "*" or (
            c == "_"
            and not (
                0 < i < n - 1
                and t[i - 1].isascii()
                and t[i - 1].isalnum()
                and t[i + 1].isascii()
                and t[i + 1].isalnum()
            )
        ):
            if emph and prev and not prev.isspace():
                out.append("]")
                emph -= 1
                closed = True
            else:
                out.append("#emph[")
                emph += 1
                closed = False
            i += 1
        elif c in "[]":
            out.append("\\" + c)
            closed = False
            i += 1
        elif c == "(" and closed:
            out.append("\\(")  # #strong[…](…) 가 함수 호출로 읽히지 않게
            closed = False
            i += 1
        else:
            out.append(esc(c).replace("~", "\\~"))
            closed = False
            i += 1
    return out, strong, emph, cands


def emphasis(t: str) -> str:
    """markdown 강조를 Typst 로 옮긴다 — **굵게** → #strong[…], 기울임(*…* · _…_) → #emph[…].

    한 줄을 한 번에 훑는다. `코드` 스팬을 미리 자르면 스팬을 낀 기울임
    (_(… `code` …)_)에서 열림 상태가 조각 사이에서 리셋되어 닫는 _ 를 다시
    열어버리므로, 백틱 구간은 불투명하게 건너뛴다(#raw 로 내보내고 이어서
    훑는다). 강조를 마크업 *…*_…_ 로 두면 Typst 의 인접 규칙(낱말 글자 뒤의
    여는 _, *_…_* 순서)과 ***…***(굵게+기울임)·겹침에서 마커가 짝을 잃어
    못 읽으므로 둘 다 함수꼴로 낸다. 열고 닫음은 스택으로 센다 — 같은 종류의
    겹침(*…* *(…)* …)이 있으므로 토글로는 안 되고, 닫는 마커는 「직전
    글자가 공백이 아니다」(right-flanking)로 가른다. 「*닫기·열기*가 붙은
    ** 묶음(…\\*\\*）\\*\\*(…)」은 굵게로 읽으면 행이 안 균형 잡히므로, 그럴 때
    묶음을 홑별 둘로 쪼개 다시 훑는다. 낱말 안의 밑줄(OPEN_QUESTIONS)은
    강조가 아니므로 양쪽이 ASCII 낱말 글자면 그대로 둔다. 대괄호는 닫는
    괄호와 겹치지 않게 다 이스케이프하고, 함수꼴로 닫힌 뒤 바로 오는
    ( 는 인자 목록으로 붙으므로 \\( 로 막는다. 재시도에도 줄 끝에 열린
    채 남는 강조는(원전이 미짝인 경우 — 관대한 markdown 렌더러처럼) 닫아 준다.
    """
    out, strong, emph, cands = _scan(t, frozenset())
    if strong or emph:  # 균형 안 잡힘 — 후보 묶음을 하나씩 쪼개 본다
        for pos in cands:
            out2, s2, e2, _ = _scan(t, frozenset({pos}))
            if not s2 and not e2:
                return "".join(out2)
            out, strong, emph = out2, s2, e2
    if strong or emph:  # 그래도 남으면 닫는다 — ] 은 열린 것 가장 안쪽부터 닫으므로 쌓인 수만큼이면 충분하다
        out = out + ["]" * (strong + emph)]
    return "".join(out)


def inline(t: str) -> str:
    """한 줄 안의 마크업을 옮긴다."""
    return emphasis(t)


def typ_str(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def split_row(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def convert(md: str, src: str, title: str, lang: str, name: str) -> str:
    lines = md.split("\n")
    out: list[str] = [
        PREAMBLE.format(
            title=title, src=src, lang=LANG[lang], fontnote=FONT_NOTE.format(name=name)
        )
    ]
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            out.append("")
            i += 1
            continue

        if re.fullmatch(r"-{3,}", stripped):
            out.append("#line(length: 100%)")
            i += 1
            continue

        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            out.append("=" * len(m.group(1)) + " " + inline(m.group(2)))
            i += 1
            continue

        # 표 — 머리줄 + 구분줄 + 본문
        if stripped.startswith("|") and i + 1 < n and re.fullmatch(
            r"\|[\s:|-]+\|", lines[i + 1].strip()
        ):
            header = split_row(stripped)
            i += 2
            body: list[list[str]] = []
            while i < n and lines[i].strip().startswith("|"):
                body.append(split_row(lines[i].strip()))
                i += 1
            cols = len(header)
            widths = ", ".join(["auto"] * (cols - 1) + ["1fr"]) if cols > 1 else "1fr"
            out.append(f"#table(\n  columns: ({widths}),")
            out.append(
                "  table.header(" + ", ".join(f"[{inline(c)}]" for c in header) + "),"
            )
            for row in body:
                row = (row + [""] * cols)[:cols]
                out.append("  " + ", ".join(f"[{inline(c)}]" for c in row) + ",")
            out.append(")")
            continue

        # 인용 블록
        if stripped.startswith(">"):
            buf: list[str] = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            # 빈 줄로 갈린 문단들을 한 인용 블록 안에 둔다
            chunks = [c.strip() for c in "\n".join(buf).split("\n\n")]
            body = "\n\n".join(inline(c) for c in chunks if c)
            out.append("#quote(block: true)[\n" + body + "\n]")
            continue

        # 글머리표 / 번호 목록
        m = re.match(r"^(\s*)([-*])\s+(.*)$", line)
        if m:
            out.append(m.group(1) + "- " + inline(m.group(3)))
            i += 1
            continue
        m = re.match(r"^(\s*)(\d+)\.\s+(.*)$", line)
        if m:
            out.append(m.group(1) + f"{m.group(2)}. " + inline(m.group(3)))
            i += 1
            continue

        out.append(inline(line))
        i += 1

    return "\n".join(out).rstrip() + "\n"


def title_of(md: str, fallback: str) -> str:
    m = re.search(r"^#\s+(.*)$", md, re.M)
    return m.group(1) if m else fallback


GEN_MARK = "// 생성물 — 손으로 고치지 않는다."


def is_generated(dst: Path) -> bool:
    """이 .typ 가 생성기의 것인가 — 머리의 표지로 가른다.

    표지가 없으면 손으로 쓴 파일이므로 대조에서 빼고 덮어쓰지도 않는다.
    """
    return any(ln.startswith(GEN_MARK) for ln in dst.read_text().split("\n")[:6])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--check", action="store_true", help="쓰지 않고 최신인지 대조만 한다")
    a = ap.parse_args()

    stale, byhand = [], []
    for p in (Path(x) for x in a.paths):
        dst = p.with_suffix(".typ")
        if dst.exists() and not is_generated(dst):
            byhand.append(str(dst))
            continue
        md = p.read_text()
        lang = "ja" if p.stem.endswith("_ja") else "ko"
        typ = convert(md, p.name, title_of(md, p.stem), lang, dst.name)
        if a.check:
            if not dst.exists() or dst.read_text() != typ:
                stale.append(str(dst))
        else:
            dst.write_text(typ)
            print(f"{p} → {dst}  ({len(typ)} 바이트)")
    for d in byhand:
        print(f"건너뜀 — 손으로 쓴 것: {d}")
    if a.check:
        if stale:
            print("최신이 아님: " + ", ".join(stale))
            return 1
        print("생성물 최신 — 전부 일치")
    return 0


if __name__ == "__main__":
    sys.exit(main())
