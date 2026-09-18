#!/usr/bin/env python3
"""〈비창〉 1악장 시퀀스 대본 → touying 덱 생성기 / 검사기.

  gen    out/bgm/11_…/script_{ko,ja}.typ 를 파싱해 out/bgm/11_…/demo/slides_{ko,ja}.typ 를 쓴다.
         비트(줄머리 *M:SS*)마다 서브슬라이드 하나 — 현재 비트는 강조색, 지난 비트는 회색.
         각 비트 페이지에 <sync-beat> 메타데이터(page·beat·t_sec·…)를 심는다 — 동기 표의 유일한 원천.
         표지에는 <sync-meta>(원본 sha256 등)를 심어, 내보낸 덱이 원본보다 오래됐는지를 check 가 알 수 있게 한다.
  check  web/pathetique-sync/public/decks/{ko,ja}/manifest.json 을 원본·cues.json 과 대조한다.
         slides_*.typ 가 지금의 원본에서 다시 만든 것과 같은지, manifest 의 <sync-meta> 가 지금의 원본을 가리키는지도 본다.

원본 마크업(Typst)은 그대로 옮긴다 — 문장을 고치지 않는다. 생성물 머리에 그렇게 적는다.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT_DIR = ROOT / "out/bgm/11_비창_1악장_시퀀스_대본"
DEMO_DIR = SCRIPT_DIR / "demo"
DECKS_DIR = ROOT / "web/pathetique-sync/public/decks"
CUES = SCRIPT_DIR / "cues.json"

TOUYING = "0.7.4"
GENERATOR = "tools/pathetique_demo_build.py"
MIN_DWELL = 2.0  # 비단조 시각을 앞 비트 뒤로 밀 때의 간격(초)
MAX_UNITS = 26  # 슬라이드 한 장에 넣는 줄 예산

LANG = {
    "ko": dict(
        section_word="구간", cpl=62, font='("Noto Sans CJK KR", "NanumSquare_ac")',
        title="〈비창〉 1악장 시퀀스 대본 — 2-5-c",
        subtitle="레이란의 오열부터 두 자매가 잠드는 순간까지",
        footer="〈비창〉 1악장 시퀀스 대본 · 비공개 내부 자료 · KO",
        meta_line="원전 v2.1.15 · 대사 전부 제안자 확정(2026-09-18) · 마차 안 예외 셋(규칙 4·10·14) · 카라얀 / 베를린 필하모닉 18:29.1 · 이 덱은 생성물이다",
        cont="(이어서)",
    ),
    "ja": dict(
        section_word="区間", cpl=58, font='("Noto Sans CJK JP", "NanumSquare_ac")',
        title="「悲愴」第1楽章シーケンス台本 ― 2-5-c",
        subtitle="レイランの号泣から二人の姉妹が眠りに落ちる瞬間まで",
        footer="「悲愴」第1楽章シーケンス台本 · 非公開の内部資料 · JA",
        meta_line="原典 v2.1.15 · 台詞はすべて提案者確定（2026-09-18）· 馬車内の例外三つ（規則4・10・14） · カラヤン / ベルリン・フィルハーモニー 18:29.1 · このデッキは生成物である",
        cont="（続き）",
    ),
}

SEC_RE = re.compile(
    r"^=== (?:구간|区間)\s*(\d+)\s*[—―]\s*(.*?)\s*·\s*(\d+:\d\d(?:\.\d)?)[–-](\d+:\d\d(?:\.\d)?)\s*·\s*(.+?)\s*$"
)
BEAT_RE = re.compile(
    r"^\s*\*(\d+:\d\d(?:\.\d)?)(?:[–-](\d+:\d\d(?:\.\d)?))?\*\s*(?:`(\[[^\]]*\])`)?\s*(.*?)\s*$"
)
TS_RE = re.compile(r"^(\d+):(\d\d(?:\.\d)?)$")
# 대본의 장식용 문단 — 덱에는 옮기지 않는다(구간 사이의 가로줄 등)
SKIP_PARA_RE = re.compile(r"^#(line|pagebreak|v)\(")
# 흐린 주석으로 보이는 문단: _(…)_ / _（…）_ 로 시작하는 것. 그 밖의 평문 문단은 본문 크기 그대로
NOTE_RE = re.compile(r"^_[（(]")


def ts_to_sec(ts: str) -> float:
    m = TS_RE.match(ts)
    if not m:
        raise ValueError(f"bad timestamp {ts!r}")
    return int(m.group(1)) * 60 + float(m.group(2))


def strip_markup(s: str) -> str:
    s = re.sub(r"`\[[^\]]*\]`", "", s)
    s = re.sub(r"(^|\s)\\(?=\s|$)", " ", s)  # 줄 끝의 ` \`(이어쓰기)
    s = re.sub(r"[*_`]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def typ_str(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


QUOTE_OPEN_RE = re.compile(r"^#quote\(block: true\)\[\s*")


def plain_text(b: "Beat") -> str:
    """비트의 전문(본문 + 인용 + 후속 문단)을 마크업 없이 — 폰에서 슬라이드 글자가 작아 목록에 펼쳐 보이기 위한 것.
    인용은 줄 단위로(대사 한 줄 = 한 줄), 나머지는 문단 하나로."""
    parts = [strip_markup(b.body)]
    for q in b.quotes:
        inner = QUOTE_OPEN_RE.sub("", q.strip())
        inner = re.sub(r"\s*\]\s*$", "", inner)
        lines = [strip_markup(ln) for ln in inner.split("\n")]
        parts.append("\n".join(ln for ln in lines if ln))
    for n in b.notes:
        parts.append(strip_markup(n))
    return "\n".join(p for p in parts if p)


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@dataclass
class Beat:
    ts: str
    ts_end: str | None
    cue: str | None  # `[…]` 포함, 백틱 제외
    body: str  # Typst 마크업 그대로
    section: int
    t_sec: float = 0.0
    t_sec_raw: float = 0.0
    quotes: list[str] = field(default_factory=list)  # #quote 블록 원문
    notes: list[str] = field(default_factory=list)  # 후속 문단 원문(_(…)_ 주석 또는 평문)
    subs: list[dict] = field(default_factory=list)  # 인용 안의 *M:SS* (페이지 없음)
    index: int = 0  # 1-based, 전체
    slide: int = 0

    @property
    def label(self) -> str:
        s = strip_markup(self.body)
        return s if len(s) <= 44 else s[:43] + "…"

    def units(self, cpl: int) -> int:
        u = math.ceil(max(len(strip_markup(self.body)), 1) / cpl) + 1
        for q in self.quotes:
            u += max(q.count("\n") - 1, 1)
        for n in self.notes:
            u += math.ceil(max(len(strip_markup(n)), 1) / cpl)
        return u


@dataclass
class Section:
    n: int
    label: str
    start: str
    end: str
    scene: str
    preface: list[str] = field(default_factory=list)
    beats: list[Beat] = field(default_factory=list)


def parse_script(path: Path) -> list[Section]:
    lines = path.read_text(encoding="utf8").split("\n")
    sections: list[Section] = []
    cur: Section | None = None
    block: list[str] = []

    def flush():
        nonlocal block
        if cur is None or not block:
            block = []
            return
        text = "\n".join(block)
        first = block[0]
        if SKIP_PARA_RE.match(first):
            pass  # 장식 문단(#line 등)은 덱에 옮기지 않는다
        elif first.startswith("#quote(block: true)["):
            if not cur.beats:
                raise ValueError(f"{path.name}: quote before any beat in section {cur.n}")
            cur.beats[-1].quotes.append(text)
            for ln in block[1:-1]:
                m = BEAT_RE.match(ln.rstrip(" \\"))
                if m and m.group(1):
                    cur.beats[-1].subs.append(
                        dict(t=m.group(1), t_end=m.group(2), cue=m.group(3), label=strip_markup(m.group(4)))
                    )
        elif BEAT_RE.match(first) and BEAT_RE.match(first).group(1):
            # 한 문단 안의 ` \` 이어쓰기 뒤에 또 *M:SS*가 오면 별도 비트
            pieces: list[str] = []
            for ln in block:
                m = BEAT_RE.match(ln)
                if m and m.group(1):
                    pieces.append(ln)
                else:
                    pieces[-1] += "\n" + ln
            for p in pieces:
                p = p.rstrip()
                if p.endswith("\\"):
                    p = p[:-1].rstrip()
                m = BEAT_RE.match(p.split("\n", 1)[0])
                rest = p.split("\n", 1)[1] if "\n" in p else ""
                body = m.group(4) + ("\n" + rest if rest else "")
                cur.beats.append(Beat(m.group(1), m.group(2), m.group(3), body, cur.n))
        else:
            (cur.beats[-1].notes if cur.beats else cur.preface).append(text)
        block = []

    for ln in lines:
        if ln.startswith("== 4.") or ln.startswith("== 4．"):
            flush()
            break
        m = SEC_RE.match(ln)
        if m:
            flush()
            cur = Section(int(m.group(1)), m.group(2), m.group(3), m.group(4), m.group(5))
            sections.append(cur)
            continue
        if cur is None:
            continue
        if ln.strip() == "":
            flush()
        else:
            block.append(ln)
    flush()
    if len(sections) != 6:
        raise ValueError(f"{path.name}: expected 6 sections, got {len(sections)}")
    return sections


def assign_times(sections: list[Section]) -> list[str]:
    warnings = []
    prev = -1.0
    i = 0
    for sec in sections:
        for b in sec.beats:
            i += 1
            b.index = i
            b.t_sec_raw = ts_to_sec(b.ts)
            b.t_sec = b.t_sec_raw
            if b.t_sec <= prev:
                b.t_sec = round(prev + MIN_DWELL, 2)
                warnings.append(f"비단조: 비트 {i} {b.ts} ({b.t_sec_raw:.1f}s) → {b.t_sec:.1f}s 로 민다")
            prev = b.t_sec
            for s in b.subs:
                s["t_sec"] = ts_to_sec(s["t"])
    return warnings


def split_slides(sections: list[Section], cpl: int, units_by_index: dict[int, int] | None = None) -> list[tuple[Section, list[Beat], bool]]:
    """(section, beats, is_continuation) — 절마다 새 슬라이드, 예산 초과 시 분할.
    units_by_index 를 주면 그 값으로 분할한다(KO/JA 가 같은 자리에서 갈라지게 두 언어의 최대값을 쓴다)."""
    slides = []
    k = 0
    for sec in sections:
        chunk: list[Beat] = []
        used = 0
        cont = False
        for b in sec.beats:
            u = units_by_index[b.index] if units_by_index else b.units(cpl)
            if chunk and used + u > MAX_UNITS:
                k += 1
                slides.append((sec, chunk, cont))
                chunk, used, cont = [], 0, True
            chunk.append(b)
            b.slide = k + 1
            used += u
        if chunk:
            k += 1
            slides.append((sec, chunk, cont))
    return slides


def render_deck(lang: str, sections: list[Section], slides, source_sha256: str) -> str:
    L = LANG[lang]
    nb = sum(len(s.beats) for s in sections)
    out = []
    w = out.append
    w("// 생성물 — 손으로 고치지 않는다. tools/pathetique_demo_build.py gen 이 script_%s.typ 에서 만든다." % lang)
    w("// 원본 문장은 그대로이며, 비트마다 서브슬라이드 하나 · 현재 비트 강조색 · <sync-beat> 메타데이터.")
    w(f'#import "@preview/touying:{TOUYING}": *')
    w("#import themes.simple: *")
    w("")
    w('#let accent = rgb("#c0392b")')
    w('#let past = rgb("#9a9a9a")')
    w('#let ink = rgb("#1a1a1a")')
    w('#let dim = rgb("#6b6b6b")')
    w("")
    w(f'#show: simple-theme.with(aspect-ratio: "16-9", header: none, primary: accent, footer: [{L["footer"]}])')
    w(f'#set text(font: {L["font"]}, lang: "{lang}", size: 11pt)')
    w("#set par(leading: 0.6em, spacing: 0.7em, justify: false)")
    w("#show quote.where(block: true): set block(inset: (left: 1.4em, y: 0.25em))")
    w("#show raw.where(block: false): set text(size: 0.85em)")
    w("")
    w("// 비트 하나: j 번째 서브슬라이드에서 강조. 그 페이지에만 <sync-beat> 메타데이터를 심는다.")
    w("#let beat(self, j, meta, ts, cue, body, subs: ()) = {")
    w("  let cur = self.subslide == j")
    w("  let col = if cur { accent } else if self.subslide > j { past } else { ink }")
    w("  if cur {")
    w("    context [#metadata((page: here().page(), ..meta)) <sync-beat>]")
    w("    for s in subs { context [#metadata((page: here().page(), ..s)) <sync-beat>] }")
    w("  }")
    w("  block(width: 100%, above: 0.55em, below: 0.55em, inset: (left: 0.5em),")
    w("    stroke: (left: if cur { 2.5pt + accent } else { 2.5pt + white }),")
    w("    text(fill: col)[#text(weight: \"bold\")[#ts]#if cue != none [ #cue] #body])")
    w("}")
    w("#let sec-title(n, label, range, scene, cont) = block(below: 0.6em)[")
    w(f'  #text(size: 9pt, fill: dim)[{L["section_word"]} #n · #label · #range #if cont [· {L["cont"]}]] \\')
    w("  #text(size: 12.5pt, weight: \"bold\")[#scene]")
    w("]")
    w("#let preface(body) = block(below: 0.6em, text(size: 9pt, fill: dim)[#body])")
    w("#let note(body) = text(size: 9pt, fill: dim)[#body]")
    w("")
    w("#title-slide[")
    w(f'  #text(size: 1.7em, weight: "bold")[{L["title"]}]')
    w("  #v(0.4em)")
    w(f'  #text(size: 1.1em)[{L["subtitle"]}]')
    w("  #v(1em)")
    w(f'  #text(size: 0.75em, fill: dim)[{L["meta_line"]}]')
    w("  // 덱의 출처 — check 가 manifest 의 이 값과 지금의 원본을 대조해 오래된 내보내기를 잡는다")
    w(f'  #context [#metadata((page: here().page(), kind: "sync-meta", lang: "{lang}", source: "script_{lang}.typ", '
      f'source_sha256: "{source_sha256}", beats: {nb}, touying: "{TOUYING}", generator: "{GENERATOR}")) <sync-meta>]')
    w("]")
    for sec, beats, cont in slides:
        w("")
        w(f"#slide(repeat: {len(beats)}, self => [")
        w(f"  #sec-title({sec.n}, [{sec.label}], [{sec.start}–{sec.end}], [{sec.scene}], {'true' if cont else 'false'})")
        if sec.preface and not cont:
            for p in sec.preface:
                w(f"  #preface[{p}]")
        for j, b in enumerate(beats, start=1):
            meta = (
                f"(beat: {b.index}, t: {typ_str(b.ts)}, t_sec: {b.t_sec:.2f}, t_sec_raw: {b.t_sec_raw:.2f}, "
                f"t_end: {typ_str(b.ts_end) if b.ts_end else 'none'}, section: {b.section}, slide: {b.slide}, "
                f"sub: false, label: {typ_str(b.label)}, text: {typ_str(plain_text(b))})"
            )
            subs = ", ".join(
                f"(beat: {b.index}, t: {typ_str(s['t'])}, t_sec: {s['t_sec']:.2f}, "
                f"t_end: {typ_str(s['t_end']) if s['t_end'] else 'none'}, section: {b.section}, slide: {b.slide}, "
                f"sub: true, label: {typ_str(((s['cue'] + ' ') if s['cue'] else '') + s['label'])})"
                for s in b.subs
            )
            subs_arg = f", subs: ({subs},)" if subs else ""
            ts = b.ts + (f"–{b.ts_end}" if b.ts_end else "")
            cue = f"`{b.cue}`" if b.cue else "none"
            w(f"  #beat(self, {j}, {meta}, {typ_str(ts)}, {cue}{subs_arg})[")
            w("    " + b.body.replace("\n", "\n    "))
            for q in b.quotes:
                w("    " + q.replace("\n", "\n    "))
            for n in b.notes:
                if NOTE_RE.match(n):
                    w(f"    #note[{n}]")
                else:
                    # 평문 문단은 대본과 같은 크기로 — 주석이 아니다
                    w("")
                    w("    " + n.replace("\n", "\n    "))
            w("  ]")
        w("])")
    w("")
    return "\n".join(out)


@dataclass
class Built:
    sections: list[Section]
    slides: list
    deck: str  # 렌더된 slides_{lang}.typ 본문
    source_sha256: str
    warnings: list[str]


def build_all() -> dict[str, Built]:
    """두 언어의 대본을 파싱·시각 배정·록스텝 검사·슬라이드 분할·렌더까지 메모리에서 한다(gen·check 공용)."""
    parsed: dict[str, list[Section]] = {}
    warns: dict[str, list[str]] = {}
    for lang in ("ko", "ja"):
        secs = parse_script(SCRIPT_DIR / f"script_{lang}.typ")
        warns[lang] = assign_times(secs)
        parsed[lang] = secs
    # 록스텝: (ts, cue 유무, 인용 수, sub 수) 가 KO/JA 에서 같아야 한다
    sig = {
        lang: [(b.ts, b.cue is not None, len(b.quotes), len(b.subs)) for s in secs for b in s.beats]
        for lang, secs in parsed.items()
    }
    if sig["ko"] != sig["ja"]:
        diffs = [(a, bb) for a, bb in zip(sig["ko"], sig["ja"]) if a != bb]
        raise ValueError(f"록스텝 불일치 (KO {len(sig['ko'])} / JA {len(sig['ja'])} 비트): {diffs[:3]}")
    # 두 언어가 같은 자리에서 슬라이드를 나누도록, 비트마다 두 언어 비용의 최대값으로 분할한다
    units_by_index: dict[int, int] = {}
    for lang, secs in parsed.items():
        for s in secs:
            for b in s.beats:
                units_by_index[b.index] = max(units_by_index.get(b.index, 0), b.units(LANG[lang]["cpl"]))
    built = {}
    for lang, secs in parsed.items():
        slides = split_slides(secs, LANG[lang]["cpl"], units_by_index)
        sha = sha256_of(SCRIPT_DIR / f"script_{lang}.typ")
        built[lang] = Built(secs, slides, render_deck(lang, secs, slides, sha), sha, warns[lang])
    built["_units"] = units_by_index  # type: ignore[assignment]
    return built


def cmd_gen(args) -> int:
    DEMO_DIR.mkdir(parents=True, exist_ok=True)
    try:
        built = build_all()
    except ValueError as e:
        print("FAIL", e)
        return 1
    units_by_index = built.pop("_units")
    for lang, bt in built.items():
        for wmsg in bt.warnings:
            print(f"[{lang}] {wmsg}")
        out = DEMO_DIR / f"slides_{lang}.typ"
        out.write_text(bt.deck, encoding="utf8")
        nb = sum(len(s.beats) for s in bt.sections)
        units = [sum(units_by_index[b.index] for b in beats) for _, beats, _ in bt.slides]
        print(f"[{lang}] {nb} beats, {sum(len(b.subs) for s in bt.sections for b in s.beats)} subs, "
              f"{len(bt.slides)} slides (units {units}) → {out.relative_to(ROOT)}; pages = 1 + {nb} = {1 + nb}")
    return 0


def cmd_check(args) -> int:
    ok = True

    def fail(msg):
        nonlocal ok
        ok = False
        print("FAIL", msg)

    mans = {}
    for lang in ("ko", "ja"):
        p = DECKS_DIR / lang / "manifest.json"
        if not p.exists():
            fail(f"{p.relative_to(ROOT)} 없음 — 먼저 export")
            continue
        mans[lang] = json.loads(p.read_text(encoding="utf8"))
        svgs = sorted((DECKS_DIR / lang).glob("page-*.svg"))
        if len(svgs) != mans[lang]["count"]:
            fail(f"[{lang}] svg {len(svgs)}개 ≠ manifest count {mans[lang]['count']}")
    if len(mans) < 2:
        return 1

    try:
        built = build_all()
    except ValueError as e:
        fail(str(e))
        return 1
    built.pop("_units")

    # 오래됨 검사 ①: 손에 있는 slides_*.typ 가 지금의 원본에서 다시 만든 것과 같은가
    for lang, bt in built.items():
        deck_path = DEMO_DIR / f"slides_{lang}.typ"
        if not deck_path.exists():
            fail(f"{deck_path.relative_to(ROOT)} 없음 — just demo-slides")
        elif deck_path.read_text(encoding="utf8") != bt.deck:
            fail(f"{deck_path.relative_to(ROOT)} 가 지금의 원본·생성기와 어긋난다 — just demo-slides 로 다시 만든다")

    # 오래됨 검사 ②: 내보낸 manifest 의 <sync-meta> 가 지금의 원본(sha256)을 가리키는가
    for lang, m in mans.items():
        metas = [x for x in m.get("labels", {}).get("sync-meta", []) if isinstance(x, dict)]
        if not metas:
            fail(f"[{lang}] manifest 에 <sync-meta> 가 없다 — 옛 생성기의 덱이거나 --query-label sync-meta 없이 내보냈다")
            continue
        sm = metas[0]
        if sm.get("page") != 1:
            fail(f"[{lang}] <sync-meta> 가 1쪽이 아니다: {sm.get('page')}")
        if sm.get("source_sha256") != built[lang].source_sha256:
            fail(f"[{lang}] 내보낸 덱이 오래됐다: manifest 의 원본 sha256 ≠ 지금의 script_{lang}.typ — just demo-slides && just demo-export")

    src_beats = [b for s in built["ko"].sections for b in s.beats]
    n = len(src_beats)

    for lang, m in mans.items():
        allv = m.get("labels", {}).get("sync-beat", [])
        lab = [x for x in allv if not x.get("sub")]
        subs = [x for x in allv if x.get("sub")]
        if not lab:
            fail(f"[{lang}] manifest 에 <sync-beat> 가 하나도 없다 — --query-label sync-beat 로 내보냈는가")
            continue
        if len(lab) != n:
            fail(f"[{lang}] sync-beat {len(lab)}개 ≠ 원본 비트 {n}개")
        pages = [x["page"] for x in lab]
        if pages != list(range(2, 2 + len(lab))):
            fail(f"[{lang}] 페이지가 2..{1+len(lab)} 연속이 아니다: {pages[:8]}…")
        if m["count"] != 1 + len(lab):
            fail(f"[{lang}] manifest count {m['count']} ≠ 1 + {len(lab)} (슬라이드 넘침?)")
        ts = [x["t_sec"] for x in lab]
        if any(b <= a for a, b in zip(ts, ts[1:])):
            fail(f"[{lang}] t_sec 이 엄격 증가하지 않는다")
        for x, b in zip(lab, src_beats):
            if abs(x["t_sec"] - b.t_sec) > 1e-6 or x["beat"] != b.index:
                fail(f"[{lang}] 비트 {b.index} {b.ts}: manifest {x.get('t')} / {x['t_sec']} ≠ 원본 {b.t_sec}")
                break
        print(f"[{lang}] {len(lab)} beats + {len(subs)} subs on pages {pages[0]}–{pages[-1]}, count {m['count']}")

    ko = [(x["page"], x["t_sec"], x["beat"]) for x in mans["ko"].get("labels", {}).get("sync-beat", [])]
    ja = [(x["page"], x["t_sec"], x["beat"]) for x in mans["ja"].get("labels", {}).get("sync-beat", [])]
    if ko != ja:
        fail("KO/JA 페이지 배정이 다르다")

    cues = json.loads(CUES.read_text(encoding="utf8"))
    first_by_sec = {}
    for b in src_beats:
        first_by_sec.setdefault(b.section, b)
    for s in cues["sections"]:
        b = first_by_sec.get(s["n"])
        # cues.json 의 start 는 "1:46.1" 처럼 표기, start_sec 은 분석값(106.15) — 표기가 같으면 통과
        if b is None or (b.ts != s["start"] and abs(b.t_sec_raw - s["start_sec"]) > 0.1):
            fail(f"구간 {s['n']} 첫 비트 {b.ts if b else None} ≠ cues.json start {s['start']}")
    # cues.json 의 비트 시각이 대본 비트(또는 인용 안 sub)에 있는가 — 초 단위로 비교("4:19" == "4:19.0")
    known = sorted({b.t_sec_raw for b in src_beats} | {s["t_sec"] for b in src_beats for s in b.subs})
    missing = [c["t"] for c in cues["beats"] if not any(abs(ts_to_sec(c["t"]) - k) < 0.05 for k in known)]
    if missing:
        print("cues.json 비트 가운데 대본 .typ 에 없는 시각(보고만):", missing)

    print("check:", "OK" if ok else "FAILED")
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("gen", help="slides_{ko,ja}.typ 생성")
    sub.add_parser("check", help="manifest.json 을 원본·cues.json·slides_*.typ 과 대조(오래됨 포함)")
    args = ap.parse_args(argv)
    return {"gen": cmd_gen, "check": cmd_check}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
