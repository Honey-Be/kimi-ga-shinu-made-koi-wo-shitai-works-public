#!/usr/bin/env python3
# 번외편 III 헌정곡 「해송」 2안 — 음원용 LilyPond(MIDI 전용)을 만든다.
# 선율 · 코드는 헌정곡_2안_공통.ily(리드시트와 같은 것)를 쓰고, 이 스크립트가 기타 아르페지오(저음현 포함) ·
# 테너 색소폰(간주 1 · 2, 3절 대선율, 아웃트로) · 드럼(브러시 / 핫 로드) · 템포 지도를 더한다.
# 출력: 헌정곡_2안_음원용.ly → lilypond → MIDI 두 개(무대판 · 녹음본) → MuseScore → FLAC.
# 공개용 스냅샷에 실린다(2026-10-08, 제안자가 공개 범위를 넓혔다).
from pathlib import Path

HERE = Path(__file__).resolve().parent

QUAL = {"maj7": (0, 4, 7, 11), "m7": (0, 3, 7, 10), "7": (0, 4, 7, 10),
        "": (0, 4, 7), "m": (0, 3, 7), "7sus4": (0, 5, 7, 10),
        "add9": (0, 4, 7, 2), "m6": (0, 3, 7, 9), "m7b5": (0, 3, 6, 10), "dim7": (0, 3, 6, 9)}
PC = {"C": 0, "D": 2, "Eb": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "A": 9, "Bb": 10}
# 저음: 6번현 F2(스코르다투라) · 저음현 C2 · B♭1 · D2, 나머지는 메인 현
BASS = {5: 41, 6: 42, 7: 43, 9: 45, 10: 34, 0: 36, 2: 38, 3: 51, 4: 52}
NAMES = ["c", "cis", "d", "es", "e", "f", "fis", "g", "aes", "a", "bes", "b"]


def lily(m):
    o = m // 12 - 4
    return NAMES[m % 12] + ("'" * o if o > 0 else "," * (-o))


def chord(spec):
    name, _, bass = spec.partition("/")
    root = name[:2] if name[:2] in ("Bb", "Eb", "F#") else name[0]
    qual = name[len(root):]
    r = PC[root]
    tones = [(r + i) % 12 for i in QUAL[qual]]
    b = PC[bass] if bass else r
    return tones, b


def upper(tones, bass_pc):
    cand = [t for t in tones if t != bass_pc] or tones
    out, m = [], 53  # F3부터 위로
    while len(out) < 3:
        for t in sorted(cand, key=lambda t: (t - m) % 12):
            n = m + (t - m) % 12
            if n not in out:
                out.append(n)
                m = n + 1
                break
    return out


def guitar_bar(segs):
    notes = []
    for spec, beats in segs:
        tones, b = chord(spec)
        bass = BASS[b]
        t1, t2, t3 = upper(tones, b)
        pat = {3: [bass, t1, t2, t3, t2, t1], 2: [bass, t1, t2, t3], 1: [bass, t2]}[beats]
        notes += [lily(n) + "8" for n in pat]
    return " ".join(notes) + " |"


# 2026-10-04 개정 — 헌정곡_2안_공통.ily의 코드와 같다(〈소나무〉의 장조 구간 둘(A♭ · B♭)의 기법만 F로 옮겨 빌림)
A1 = [[("Fadd9", 2), ("C/E", 1)], [("Dm7", 3)], [("Gm7", 2), ("C7", 1)], [("C7sus4", 1), ("F", 2)]]
B1 = [[("F7", 1), ("Bb", 2)], [("Gm7/C", 3)], [("C7", 3)], [("F", 3)]]
A1b = [[("Fadd9", 2), ("C/E", 1)], [("Dm7", 3)], [("Gm7", 2), ("C7", 1)], [("C7", 1), ("F", 2)]]
A2 = [[("F", 2), ("A7sus4", 1)], [("Dm7", 2), ("Dm7/C", 1)], [("Bbmaj7", 2), ("C7", 1)], [("C7sus4", 1), ("F", 2)]]
B2 = [[("F7", 1), ("Bb", 2)], [("Gm7/C", 3)], [("C7sus4", 2), ("C7", 1)], [("F", 3)]]
A2b = [[("Fadd9", 2), ("C/E", 1)], [("Dm7", 2), ("D7", 1)], [("Gm7", 2), ("C7", 1)], [("C7", 1), ("F", 2)]]
A3 = [[("F", 2), ("C/E", 1)], [("Dm7", 2), ("Dm7/C", 1)], [("Bbmaj7", 2), ("C7", 1)], [("C7", 1), ("F", 2)]]
B3 = [[("F7", 1), ("Bb", 2)], [("Gm7", 2), ("Gm7/F", 1)], [("Em7b5", 1), ("C7/E", 2)], [("F", 3)]]
A3end = [[("F", 2), ("C/E", 1)], [("Dm7", 2), ("F#dim7", 1)], [("Gm7", 2), ("C7", 1)], [("C7sus4", 3)]]
INTRO = [[("Fadd9", 3)], [("Fmaj7/E", 3)], [("Dm7", 3)], [("Gm7/C", 2), ("C7", 1)]]
INT2 = [[("F7", 1), ("Bb", 2)], [("Gm7/C", 3)], [("C7", 3)], [("F", 3)], [("Gm7", 3)], [("Em7b5", 2), ("A7", 1)]]
BRIDGE = [[("Dm", 2), ("Dm/C", 1)], [("Bbmaj7", 3)], [("Gm7", 3)], [("A7sus4", 2), ("A7", 1)],
          [("Bbmaj7", 3)], [("Cadd9", 3)], [("F/A", 3)], [("Gm7/C", 3)], [("C7sus4", 3)]]
OUT_STAGE = [[("C7sus4", 3)], [("C7sus4", 3)], [("Gm7/C", 3)], [("C7", 3)], [("F", 3)]]
OUT_ALBUM = [[("C7sus4", 3)]] * 4

BODY = INTRO + A1 + B1 + A1b + A1 + B1 + A2 + B2 + A2b + INT2 + BRIDGE + A3 + B3 + A3end
assert len(BODY) == 63, len(BODY)


def guitar(outro, album):
    bars = [guitar_bar(b) for b in BODY + outro]
    dyn = {0: r"\mp", 4: r"\mp", 42: r"\p", 51: r"\mf", 63: r"\mp"}
    out = []
    for i, bar in enumerate(bars):
        if i in dyn:
            head, rest = bar.split(" ", 1)
            bar = head + dyn[i] + " " + rest
        if album and i == 63:
            head, rest = bar.split(" ", 1)
            bar = head + r"\> " + rest
        out.append(bar)
    if album:
        out[-1] = out[-1][:-2] + r"\ppp |"
    else:
        out[-1] = "<f, c f a c'>2.\\fermata |"  # 마지막 F — 6번현 F2와 공명현으로
    return "\n  ".join(out)


SAX_INT1 = r"r2 r8 c8 | f8.\mp f16 f4 g4 | a8. a16 a4. a8 | g8 a8 bes4 e4 | g4 f2 | c'8 a8 d'4. c'8 | c'8 bes8 bes4. bes8 | bes8 g8 c'4. bes8 | bes8 a8 a2 |"
SAX_INT2 = r"a4\mp c'4 d'4 | c'2 bes4 | bes2. | a2. | bes4 a4 g4 | g2 cis'4 |"
SAX_V3 = r"c''2.\mf | a'2 g'4 | f'2 e'4 | e'4 f'2 | es'4 d'2 | d'2 e'4 | bes'2. | a'2. | c''2. | a'2 g'4 | f'2 e'4 | f'2. |"


def sax(album):
    # 마디: 인트로 4 · 1절 12(16마디째 끝에서 간주 1의 못갖춘마디) · 간주 1 8 · 2절 12 · 간주 2 6 · 브릿지 9 · 3절 12 · 아웃트로
    parts = ["R2.*15 |", SAX_INT1, "R2.*12 |", SAX_INT2, "R2.*9 |", SAX_V3]
    if album:
        parts.append(r"bes'4\mp\> a'4 g'4 | f'2.~ | f'2.~ | f'2.\ppp |")
    else:
        parts.append(r"bes'4\mp a'4 g'4 | f'2.~ | f'2. | e'2. | f'2.\fermata |")
    return "\n  ".join(parts)


BRUSH = r"bd4\pp sn4 sn4 |"
RODS = r"bd4\mp sn8 sn8 sn4 |"


def drums(album):
    bars = ["R2.*16 |"] + [BRUSH] * 26 + ["R2.*9 |"] + [RODS] * 12
    bars += [r"bd2.\p |", "R2.*3 |"] if album else [r"bd2.\p |", "R2.*4 |"]
    return "\n  ".join(bars)


def tempo(album):
    t = [r"\tempo 4 = 84 s2.*42", r"\tempo 4 = 76 s2.*8", r"\tempo 4 = 44 s2.",
         r"\tempo 4 = 88 s2.*12"]
    t += [r"\tempo 4 = 80 s2.*4"] if album else [r"\tempo 4 = 80 s2.*4", r"\tempo 4 = 40 s2."]
    return " ".join(t)


def score(album):
    outro = OUT_ALBUM if album else OUT_STAGE
    return rf"""
\score {{
  <<
    \new Staff \with {{ midiInstrument = "voice oohs" midiMaximumVolume = #0.95 }} <<
      \new Voice {{ \melody }}
      \new Voice {{ {tempo(album)} }}
    >>
    \new Staff \with {{ midiInstrument = "tenor sax" midiMaximumVolume = #0.8 }} {{ \global
  {sax(album)}
    }}
    \new Staff \with {{ midiInstrument = "acoustic guitar (nylon)" midiMaximumVolume = #0.75 }} {{ \global
  {guitar(outro, album)}
    }}
    \new DrumStaff \with {{ midiMaximumVolume = #0.45 }} \drummode {{
  {drums(album)}
    }}
  >>
  \midi {{ }}
}}
"""


ly = r"""% 번외편 III 헌정곡 「해송」 2안 — 음원용(MIDI 전용). _gen_audio_ly.py가 만든다 — 직접 고치지 않는다.
% 첫째 \score = 무대판(그 밤 — 마지막에 F로 닫는다), 둘째 \score = 녹음본(앨범의 숨긴 곡 — C7sus4에서 사라진다).
% 공개용 스냅샷에 실린다(2026-10-08, 제안자가 공개 범위를 넓혔다).
\version "2.24.0"
\include "헌정곡_2안_공통.ily"
""" + score(False) + score(True)
(HERE / "헌정곡_2안_음원용.ly").write_text(ly)
print("ok")
