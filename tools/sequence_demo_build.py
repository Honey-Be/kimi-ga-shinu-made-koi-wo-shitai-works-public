#!/usr/bin/env python3
"""두 시퀀스를 연이어 보는 덱 생성기 / 검사기.

  gen    12번(동귀어진 → 폭로방송)과 11번(〈비창〉 1악장)을 **하나의 덱**으로 잇는다.
         out/bgm/_combined/slides_{ko,ja}.typ 를 쓴다.
  check  내보낸 manifest.json 을 원본·악장표와 대조한다.

**음원은 셋이고 자르지도 이어붙이지도 않는다**(제안자 조건 — 통째로 무편집).
대신 이 파일이 **악장표**(movements)를 만든다 — 음원 셋과 그 사이의 무음 구간에
전역 시각을 부여하는 표이며, 웹 쪽은 그 표를 보고 `<audio>` 의 src 를 갈아 끼운다.
**ffmpeg 로 이어붙이지 않는다** — 재인코딩이 한 번도 일어나지 않게 하기 위해서다.

    드보르자크 3:42.0 → 무음(가안) → 브람스 6:52.2 → 무음(가안) → 차이코프스키 18:29.1

무음 구간의 길이는 원전에 없다. 이 파일이 **가안**으로 정하며 덱과 화면에 그렇게 적는다.
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

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pathetique_demo_build as P11  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DIR12 = ROOT / "out/bgm/12_동귀어진_폭로방송_시퀀스_대본"
DIR11 = ROOT / "out/bgm/11_비창_1악장_시퀀스_대본"
OUT = ROOT / "out/bgm/_combined"
DECKS = ROOT / "web/pathetique-sync/public/decks"

TOUYING = P11.TOUYING
GENERATOR = "tools/sequence_demo_build.py"
MAX_UNITS = 22

# 음원 셋 — 파일은 저장소에 없다(기계-로컬). 길이는 ffprobe 로 잰 값.
TRACKS = {
    "dvorak":       dict(dur=222.00, src="/audio/dvorak-songs-my-mother.m4a",
                         name_ko="드보르자크 〈어머니가 가르쳐 주신 노래〉",
                         name_ja="ドヴォルザーク〈我が母の教え給いし歌〉"),
    "brahms5":      dict(dur=412.21, src="/audio/brahms-requiem-v.flac",
                         name_ko="브람스 『독일 레퀴엠』 제5곡",
                         name_ja="ブラームス『ドイツ・レクイエム』第五曲"),
    "tchaikovsky":  dict(dur=1109.10, src="/audio/pathetique-mvt1.m4a",
                         name_ko="차이코프스키 교향곡 6번 1악장",
                         name_ja="チャイコフスキー交響曲第6番 第1楽章"),
}

# 무음 비트의 가안 길이 — 글자 수에 비례하되 이 범위 안에서. 두 언어의 최대값을 쓴다(타임라인이 같아야 하므로).
SILENT_MIN, SILENT_MAX, SILENT_CPS = 10.0, 30.0, 15.0

SEQ = {
    "12": dict(dirname=DIR12, ext="md"),
    "11": dict(dirname=DIR11, ext="typ"),
}

L = {
    "ko": dict(
        word_sec="구간", word_seq="시퀀스", cpl=62,
        font='("Noto Sans CJK KR", "NanumSquare_ac")',
        title="동귀어진 → 폭로방송 → 〈비창〉 1악장",
        subtitle="두 시퀀스를 연이어 — 에이란이 금서와 마주한 자리부터 두 자매가 잠드는 순간까지",
        footer="두 시퀀스 연속 대본 · 비공개 내부 자료 · KO",
        meta="원전 v2.2.2 · 음원 셋을 자르지 않고 통째로 · 그 사이의 무음 길이는 이 덱의 가안이다 · 생성물",
        cont="(이어서)", silent="무음", nominal="가안",
        seq12="동귀어진 → 폭로방송", seq11="〈비창〉 1악장",
    ),
    "ja": dict(
        word_sec="区間", word_seq="シークエンス", cpl=58,
        font='("Noto Sans CJK JP", "NanumSquare_ac")',
        title="相討ち → 暴露放送 → 「悲愴」第1楽章",
        subtitle="二つのシークエンスを続けて ― エイランが禁書と向き合った場から二人の姉妹が眠りに落ちる瞬間まで",
        footer="二シークエンス連続台本 · 非公開の内部資料 · JA",
        meta="原典 v2.2.2 · 音源三つを切らず丸ごと · その間の無音の長さはこのデッキの仮案である · 生成物",
        cont="（続き）", silent="無音", nominal="仮案",
        seq12="相討ち → 暴露放送", seq11="「悲愴」第1楽章",
    ),
}

# --- 12번 대본(.md) 파서 -------------------------------------------------

H3 = re.compile(r"^### ([ABC])\s*[—―]\s*(.+?)\s*$")
H4 = re.compile(r"^#### ([ABC]-\d+′?)\s*·\s*(?:\*\*(.+?)\*\*\s*·\s*)?(.+?)\s*$")
BODY_START = re.compile(r"^## (?:대본|台本)\s*$")
BODY_END = re.compile(r"^## (?:이 대본이 하지 않은 것|この台本がしなかったこと)\s*$")
CUE_LINE = re.compile(r"^`(\[.*\])`\s*$")


@dataclass
class Beat:
    bid: str
    label: str          # 장소·제목
    stamp: str | None   # `**0:00.0–0:48**` 안쪽, 없으면 None
    section: str        # A / B / C
    seq: str            # "12" / "11"
    blocks: list[tuple[str, str]] = field(default_factory=list)  # (kind, text) kind = para|quote|note|cue
    track: str | None = None
    track_t: float = 0.0
    dur: float = 0.0
    t0: float = 0.0     # 전역 시각
    index: int = 0
    slide: int = 0

    def plain(self) -> str:
        out = []
        for kind, t in self.blocks:
            if kind == "cue":
                continue
            out.append(strip_md(t))
        return "\n".join(x for x in out if x)

    def units(self, cpl: int) -> int:
        u = 2
        for kind, t in self.blocks:
            if kind == "cue":
                continue
            u += math.ceil(max(len(strip_md(t)), 1) / cpl)
        return u


@dataclass
class Sec:
    key: str
    label: str
    seq: str
    beats: list[Beat] = field(default_factory=list)


def strip_md(s: str) -> str:
    s = re.sub(r"`([^`]*)`", r"\1", s)
    s = re.sub(r"^\s*> ?", "", s, flags=re.M)
    s = re.sub(r"[*_]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def md_to_typ(s: str) -> str:
    """대본 Markdown 한 조각 → Typst. tools/script_md2typ.py 와 같은 규칙의 작은 판."""
    out = []
    for i, part in enumerate(re.split(r"(`[^`]*`)", s)):
        if i % 2:
            out.append("#raw(" + typ_str(part[1:-1]) + ")")
            continue
        t = part.replace("\\", "\\\\").replace("#", "\\#").replace("$", "\\$").replace("@", "\\@")
        t = t.replace("**", "*").replace("~", "\\~")
        out.append(t)
    return "".join(out)


def typ_str(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


def parse12(path: Path) -> list[Sec]:
    lines = path.read_text(encoding="utf8").split("\n")
    secs: list[Sec] = []
    cur: Sec | None = None
    beat: Beat | None = None
    block: list[str] = []
    inside = False

    def flush():
        nonlocal block
        if beat is None or not block:
            block = []
            return
        text = "\n".join(block).strip()
        if not text:
            block = []
            return
        if CUE_LINE.match(block[0]):
            kind = "cue"
        elif block[0].lstrip().startswith(">"):
            kind = "quote"
        elif block[0].lstrip().startswith("_("):
            kind = "note"
        else:
            kind = "para"
        beat.blocks.append((kind, text))
        block = []

    for ln in lines:
        if BODY_START.match(ln):
            inside = True
            continue
        if inside and BODY_END.match(ln):
            flush()
            break
        if not inside:
            continue
        m = H3.match(ln)
        if m:
            flush()
            beat = None
            cur = Sec(m.group(1), m.group(2), "12")
            secs.append(cur)
            continue
        m = H4.match(ln)
        if m and cur is not None:
            flush()
            beat = Beat(m.group(1), m.group(3), m.group(2), cur.key, "12")
            cur.beats.append(beat)
            continue
        if ln.strip() == "":
            flush()
        elif beat is not None:
            block.append(ln)
    flush()
    if len(secs) != 3:
        raise ValueError(f"{path.name}: A/B/C 세 절이어야 하는데 {len(secs)}개")
    return secs


# --- 악장표 ---------------------------------------------------------------

def load_cues12() -> dict[str, dict]:
    c = json.loads((DIR12 / "cues.json").read_text(encoding="utf8"))
    return {b["id"]: b for b in c["beats"]}


def build_timeline(secs12: dict[str, list[Sec]], secs11) -> tuple[list[dict], list[str]]:
    """전역 시각을 배정하고 악장표를 만든다. secs12 는 언어별 파싱 결과(무음 길이를 두 언어 최대로)."""
    cues = load_cues12()
    warns: list[str] = []

    # 무음 비트의 가안 길이 — 두 언어의 최대
    nominal: dict[str, float] = {}
    for lang, secs in secs12.items():
        for s in secs:
            for b in s.beats:
                if cues.get(b.bid, {}).get("track"):
                    continue
                d = min(SILENT_MAX, max(SILENT_MIN, len(b.plain()) / SILENT_CPS))
                nominal[b.bid] = max(nominal.get(b.bid, 0.0), round(d, 1))

    movements: list[dict] = []
    t = 0.0
    order = [b for s in secs12["ko"] for b in s.beats]
    i = 0
    while i < len(order):
        b = order[i]
        tr = cues.get(b.bid, {}).get("track")
        if tr:
            run = [b]
            j = i + 1
            while j < len(order) and cues.get(order[j].bid, {}).get("track") == tr:
                run.append(order[j])
                j += 1
            movements.append(dict(kind="audio", track=tr, t0=round(t, 2),
                                  dur=TRACKS[tr]["dur"], beats=[x.bid for x in run]))
            t += TRACKS[tr]["dur"]
            i = j
        else:
            run = [b]
            j = i + 1
            while j < len(order) and not cues.get(order[j].bid, {}).get("track"):
                run.append(order[j])
                j += 1
            dur = round(sum(nominal[x.bid] for x in run), 1)
            movements.append(dict(kind="silence", track=None, t0=round(t, 2),
                                  dur=dur, beats=[x.bid for x in run], nominal=True))
            t += dur
            i = j
    movements.append(dict(kind="audio", track="tchaikovsky", t0=round(t, 2),
                          dur=TRACKS["tchaikovsky"]["dur"], beats=["11"]))
    total = round(t + TRACKS["tchaikovsky"]["dur"], 2)

    # 비트에 전역 시각 붙이기 — 두 언어에 같은 값을 넣는다
    for lang, secs in secs12.items():
        acc = {m["track"] or f"sil{k}": m for k, m in enumerate(movements)}
        del acc
        t = 0.0
        for mv in movements:
            if mv["beats"] == ["11"]:
                continue
            if mv["kind"] == "audio":
                for bid in mv["beats"]:
                    c = cues[bid]
                    bb = _find(secs, bid)
                    bb.track = mv["track"]
                    bb.track_t = float(c["start"])
                    bb.t0 = round(mv["t0"] + float(c["start"]), 2)
                    bb.dur = round(float(c["end"]) - float(c["start"]), 2)
            else:
                cursor = mv["t0"]
                for bid in mv["beats"]:
                    bb = _find(secs, bid)
                    bb.track = None
                    bb.t0 = round(cursor, 2)
                    bb.dur = nominal[bid]
                    cursor += nominal[bid]
    t11 = movements[-1]["t0"]
    for sec in secs11:
        for b in sec.beats:
            b.t_sec_global = round(t11 + b.t_sec, 2)  # type: ignore[attr-defined]
    return movements, warns + [f"총 길이 {total:.1f}초 ({int(total//60)}:{total%60:04.1f})"]


def _find(secs: list[Sec], bid: str) -> Beat:
    for s in secs:
        for b in s.beats:
            if b.bid == bid:
                return b
    raise KeyError(bid)


# --- 렌더 -----------------------------------------------------------------

def split(items: list, cost, budget: int) -> list[list]:
    out, chunk, used = [], [], 0
    for it in items:
        u = cost(it)
        if chunk and used + u > budget:
            out.append(chunk)
            chunk, used = [], 0
        chunk.append(it)
        used += u
    if chunk:
        out.append(chunk)
    return out


def fmt(t: float) -> str:
    m = int(t // 60)
    return f"{m}:{t - m * 60:04.1f}"


def render(lang: str, secs12: list[Sec], secs11, movements, units: dict[str, int], shas: dict[str, str]) -> str:
    C = L[lang]
    w = []
    a = w.append
    a(f"// 생성물 — 손으로 고치지 않는다. {GENERATOR} gen 이 만든다.")
    a("// 12번 시퀀스와 11번 시퀀스를 한 덱으로 잇는다. 전역 시각(t_sec)은 악장표 기준이다.")
    a(f'#import "@preview/touying:{TOUYING}": *')
    a("#import themes.simple: *")
    a("")
    a('#let accent = rgb("#c0392b")')
    a('#let past = rgb("#9a9a9a")')
    a('#let ink = rgb("#1a1a1a")')
    a('#let dim = rgb("#6b6b6b")')
    a('#let quiet = rgb("#7a6a8a")')
    a("")
    a(f'#show: simple-theme.with(aspect-ratio: "16-9", header: none, primary: accent, footer: [{C["footer"]}])')
    a(f'#set text(font: {C["font"]}, lang: "{lang}", size: 11pt)')
    a("#set par(leading: 0.6em, spacing: 0.7em, justify: false)")
    a("#show quote.where(block: true): set block(inset: (left: 1.4em, y: 0.25em))")
    a("#show raw.where(block: false): set text(size: 0.85em)")
    a("")
    a("#let beat(self, j, meta, tag, title, body) = {")
    a("  let cur = self.subslide == j")
    a("  let col = if cur { accent } else if self.subslide > j { past } else { ink }")
    a("  if cur { context [#metadata((page: here().page(), ..meta)) <sync-beat>] }")
    a("  block(width: 100%, above: 0.55em, below: 0.55em, inset: (left: 0.5em),")
    a("    stroke: (left: if cur { 2.5pt + accent } else { 2.5pt + white }),")
    a("    text(fill: col)[#text(weight: \"bold\")[#tag] #text(size: 0.92em)[#title] #body])")
    a("}")
    a("#let head(seq, sec, cont) = block(below: 0.6em)[")
    a("  #text(size: 9pt, fill: dim)[#seq · #sec #if cont [· " + C["cont"] + "]] \\")
    a("]")
    a("#let note(body) = text(size: 9pt, fill: dim)[#body]")
    a("#let quietnote(body) = text(size: 9pt, fill: quiet)[#body]")
    a("")
    a("#title-slide[")
    a(f'  #text(size: 1.6em, weight: "bold")[{C["title"]}]')
    a("  #v(0.4em)")
    a(f'  #text(size: 1.0em)[{C["subtitle"]}]')
    a("  #v(0.9em)")
    a(f'  #text(size: 0.72em, fill: dim)[{C["meta"]}]')
    meta = (f'(page: here().page(), kind: "sync-meta", lang: "{lang}", generator: "{GENERATOR}", '
            f'touying: "{TOUYING}", '
            + ", ".join(f'sha_{k}: "{v}"' for k, v in sorted(shas.items())) + ")")
    a(f"  #context [#metadata({meta}) <sync-meta>]")
    a("]")

    idx = 0
    # --- 12번
    for sec in secs12:
        chunks = split(sec.beats, lambda b: units[b.bid], MAX_UNITS)
        for ci, chunk in enumerate(chunks):
            a("")
            a(f"#slide(repeat: {len(chunk)}, self => [")
            a(f'  #head([{C["seq12"]}], [{sec.key} — {md_to_typ(sec.label)}], {"true" if ci else "false"})')
            for j, b in enumerate(chunk, start=1):
                idx += 1
                b.index = idx
                tag = b.bid
                stamp = f" {b.stamp}" if b.stamp else ""
                m = (f'(beat: {idx}, seq: "12", bid: {typ_str(b.bid)}, section: {typ_str(b.section)}, '
                     f"t_sec: {b.t0:.2f}, dur: {b.dur:.2f}, "
                     f"track: {typ_str(b.track) if b.track else 'none'}, track_t: {b.track_t:.2f}, "
                     f"t: {typ_str(fmt(b.t0))}, sub: false, "
                     f"label: {typ_str((b.label[:44]))}, text: {typ_str(b.plain())})")
                a(f"  #beat(self, {j}, {m}, {typ_str(tag)}, [{md_to_typ(b.label + stamp)}])[")
                for kind, t in b.blocks:
                    if kind == "cue":
                        a(f"    #text(size: 9pt, fill: dim)[{md_to_typ(t)}]")
                    elif kind == "quote":
                        inner = "\n".join(re.sub(r"^\s*> ?", "", x) for x in t.split("\n"))
                        a("    #quote(block: true)[" + md_to_typ(inner) + "]")
                    elif kind == "note":
                        a(f"    #note[{md_to_typ(t)}]")
                    else:
                        a("")
                        a("    " + md_to_typ(t))
                a("  ]")
            a("])")
    # --- 11번 (기존 파서의 결과를 같은 모양으로)
    for sec in secs11:
        chunks = split(sec.beats, lambda b: units[f"11:{b.index}"], MAX_UNITS)
        for ci, chunk in enumerate(chunks):
            a("")
            a(f"#slide(repeat: {len(chunk)}, self => [")
            a(f'  #head([{C["seq11"]}], [{C["word_sec"]} {sec.n} — {sec.label}], {"true" if ci else "false"})')
            for j, b in enumerate(chunk, start=1):
                idx += 1
                g = getattr(b, "t_sec_global")
                m = (f'(beat: {idx}, seq: "11", bid: {typ_str("11-" + str(b.index))}, section: {typ_str(str(b.section))}, '
                     f"t_sec: {g:.2f}, dur: 0.0, track: \"tchaikovsky\", track_t: {b.t_sec:.2f}, "
                     f"t: {typ_str(fmt(g))}, sub: false, "
                     f"label: {typ_str(b.label)}, text: {typ_str(P11.plain_text(b))})")
                ts = b.ts + (f"–{b.ts_end}" if b.ts_end else "")
                a(f"  #beat(self, {j}, {m}, {typ_str(ts)}, [])[")
                a("    " + b.body.replace("\n", "\n    "))
                for q in b.quotes:
                    a("    " + q.replace("\n", "\n    "))
                for n in b.notes:
                    a(f"    #note[{n}]" if P11.NOTE_RE.match(n) else "\n    " + n.replace("\n", "\n    "))
                a("  ]")
            a("])")
    a("")
    return "\n".join(w)


# --- 명령 -----------------------------------------------------------------

def build_all():
    secs12 = {l: parse12(DIR12 / f"script_{l}.md") for l in ("ko", "ja")}
    secs11 = {}
    for l in ("ko", "ja"):
        s = P11.parse_script(DIR11 / f"script_{l}.typ")
        P11.assign_times(s)
        secs11[l] = s
    sig = {l: [b.bid for s in secs12[l] for b in s.beats] for l in secs12}
    if sig["ko"] != sig["ja"]:
        raise ValueError(f"12번 KO/JA 비트 id 불일치: {set(sig['ko']) ^ set(sig['ja'])}")
    movements, warns = build_timeline(secs12, secs11["ko"])
    # 11번 전역 시각을 JA 쪽에도
    t11 = movements[-1]["t0"]
    for b in (b for s in secs11["ja"] for b in s.beats):
        b.t_sec_global = round(t11 + b.t_sec, 2)  # type: ignore[attr-defined]

    units: dict[str, int] = {}
    for l in ("ko", "ja"):
        for s in secs12[l]:
            for b in s.beats:
                units[b.bid] = max(units.get(b.bid, 0), b.units(L[l]["cpl"]))
        for s in secs11[l]:
            for b in s.beats:
                k = f"11:{b.index}"
                units[k] = max(units.get(k, 0), b.units(L[l]["cpl"]))
    shas = {
        "12ko": P11.sha256_of(DIR12 / "script_ko.md")[:16],
        "12ja": P11.sha256_of(DIR12 / "script_ja.md")[:16],
        "11ko": P11.sha256_of(DIR11 / "script_ko.typ")[:16],
        "11ja": P11.sha256_of(DIR11 / "script_ja.typ")[:16],
        "cues": P11.sha256_of(DIR12 / "cues.json")[:16],
    }
    decks = {l: render(l, secs12[l], secs11[l], movements, units, shas) for l in ("ko", "ja")}
    return secs12, secs11, movements, decks, shas, warns


def cmd_gen(args) -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    secs12, secs11, movements, decks, shas, warns = build_all()
    for w in warns:
        print(w)
    for l, txt in decks.items():
        p = OUT / f"slides_{l}.typ"
        p.write_text(txt, encoding="utf8")
        n12 = sum(len(s.beats) for s in secs12[l])
        n11 = sum(len(s.beats) for s in secs11[l])
        print(f"[{l}] 12번 {n12} + 11번 {n11} = {n12 + n11} beats → {p.relative_to(ROOT)}")
    mv = OUT / "movements.json"
    mv.write_text(json.dumps(dict(
        generator=GENERATOR,
        note="음원 셋을 자르거나 이어붙이지 않는다. 무음 구간의 길이는 이 표의 가안이다.",
        tracks={k: {kk: vv for kk, vv in v.items()} for k, v in TRACKS.items()},
        movements=movements,
        total=round(movements[-1]["t0"] + movements[-1]["dur"], 2),
        sources=shas,
    ), ensure_ascii=False, indent=2) + "\n", encoding="utf8")
    print(f"악장 {len(movements)}개 → {mv.relative_to(ROOT)}")
    for m in movements:
        kind = m["track"] or "—(무음·가안)"
        print(f"  {fmt(m['t0']):>7} +{m['dur']:7.2f}  {kind:<12} {len(m['beats'])} beats")
    return 0


def cmd_check(args) -> int:
    ok = True

    def fail(m):
        nonlocal ok
        ok = False
        print("FAIL", m)

    secs12, secs11, movements, decks, shas, _ = build_all()
    for l, txt in decks.items():
        p = OUT / f"slides_{l}.typ"
        if not p.exists():
            fail(f"{p.relative_to(ROOT)} 없음 — just demo-slides")
        elif p.read_text(encoding="utf8") != txt:
            fail(f"{p.relative_to(ROOT)} 가 지금의 원본과 어긋난다 — just demo-slides")
    mans = {}
    for l in ("ko", "ja"):
        p = DECKS / l / "manifest.json"
        if not p.exists():
            fail(f"{p.relative_to(ROOT)} 없음 — just demo-export")
            continue
        mans[l] = json.loads(p.read_text(encoding="utf8"))
    if len(mans) < 2:
        print("check:", "FAILED")
        return 1
    n = sum(len(s.beats) for s in secs12["ko"]) + sum(len(s.beats) for s in secs11["ko"])
    for l, m in mans.items():
        lab = [x for x in m.get("labels", {}).get("sync-beat", []) if not x.get("sub")]
        if len(lab) != n:
            fail(f"[{l}] sync-beat {len(lab)}개 ≠ 원본 {n}개")
        ts = [x["t_sec"] for x in lab]
        if any(b <= a for a, b in zip(ts, ts[1:])):
            bad = [(a, b) for a, b in zip(ts, ts[1:]) if b <= a][:3]
            fail(f"[{l}] 전역 t_sec 이 엄격 증가하지 않는다: {bad}")
        pages = [x["page"] for x in lab]
        if pages != list(range(2, 2 + len(lab))):
            fail(f"[{l}] 페이지가 2..{1 + len(lab)} 연속이 아니다")
        if m["count"] != 1 + len(lab):
            fail(f"[{l}] manifest count {m['count']} ≠ 1 + {len(lab)} (슬라이드 넘침?)")
        sm = [x for x in m.get("labels", {}).get("sync-meta", []) if isinstance(x, dict)]
        if not sm:
            fail(f"[{l}] <sync-meta> 없음")
        elif any(sm[0].get(f"sha_{k}") != v for k, v in shas.items()):
            fail(f"[{l}] 내보낸 덱이 오래됐다 — just demo-slides && just demo-export")
        # 악장 경계를 넘지 않는가
        for x in lab:
            if x.get("track"):
                mv = [mm for mm in movements if mm["track"] == x["track"]]
                if not mv or not (mv[0]["t0"] - 0.01 <= x["t_sec"] <= mv[-1]["t0"] + mv[-1]["dur"] + 0.01):
                    fail(f"[{l}] 비트 {x.get('bid')} 의 전역 시각이 악장 밖이다: {x['t_sec']}")
                    break
        print(f"[{l}] {len(lab)} beats, count {m['count']}, 총 {fmt(movements[-1]['t0'] + movements[-1]['dur'])}")
    ko = [(x["page"], x["t_sec"]) for x in mans["ko"]["labels"]["sync-beat"]]
    ja = [(x["page"], x["t_sec"]) for x in mans["ja"]["labels"]["sync-beat"]]
    if ko != ja:
        fail("KO/JA 페이지·시각 배정이 다르다")
    print("check:", "OK" if ok else "FAILED")
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("gen")
    sub.add_parser("check")
    a = ap.parse_args(argv)
    return {"gen": cmd_gen, "check": cmd_check}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
