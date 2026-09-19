#!/usr/bin/env python3
"""시퀀스 대본 Markdown → Typst 변환기.

`out/bgm/**/script_{ko,ja}.md` 를 같은 내용의 `.typ` 로 옮긴다.
**같은 변환기를 두 언어에 쓰므로 .typ 는 .md 와 자동으로 록스텝이 된다** —
구조가 어긋나면 그것은 .md 쪽에서 이미 어긋난 것이다.

    python3 tools/script_md2typ.py out/bgm/12_…/script_ko.md
    python3 tools/script_md2typ.py out/bgm/12_…/script_*.md --check

`--check` 는 쓰지 않고 대조만 한다(생성물이 최신인지).

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


def inline(t: str) -> str:
    """한 줄 안의 마크업을 옮긴다."""
    out: list[str] = []
    # `코드` 는 안쪽을 건드리지 않는다
    for i, part in enumerate(re.split(r"(`[^`]*`)", t)):
        if i % 2:
            out.append("#raw(" + typ_str(part[1:-1]) + ")")
            continue
        s = esc(part)
        # **굵게** → *굵게*. 짝을 regex 로 맞추지 않고 하나씩 바꾼다 —
        # 굵은 범위가 `코드` 를 건너뛰는 경우(**앞 `x` 뒤**)에도 짝이 맞기 때문이다.
        s = s.replace("**", "*")
        s = re.sub(r"(?<!\w)_\((.+?)\)_", r"_(\1)_", s)   # _(괄호)_ 는 그대로
        s = s.replace("~", "\\~")
        out.append(s)
    return "".join(out)


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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--check", action="store_true", help="쓰지 않고 최신인지 대조만 한다")
    a = ap.parse_args()

    stale = []
    for p in (Path(x) for x in a.paths):
        md = p.read_text()
        lang = "ja" if p.stem.endswith("_ja") else "ko"
        dst = p.with_suffix(".typ")
        typ = convert(md, p.name, title_of(md, p.stem), lang, dst.name)
        if a.check:
            if not dst.exists() or dst.read_text() != typ:
                stale.append(str(dst))
        else:
            dst.write_text(typ)
            print(f"{p} → {dst}  ({len(typ)} 바이트)")
    if a.check:
        if stale:
            print("최신이 아님: " + ", ".join(stale))
            return 1
        print("생성물 최신 — 전부 일치")
    return 0


if __name__ == "__main__":
    sys.exit(main())
