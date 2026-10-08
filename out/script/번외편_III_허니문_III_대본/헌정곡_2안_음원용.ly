% 번외편 III 헌정곡 「해송」 2안 — 음원용(MIDI 전용). _gen_audio_ly.py가 만든다 — 직접 고치지 않는다.
% 첫째 \score = 무대판(그 밤 — 마지막에 F로 닫는다), 둘째 \score = 녹음본(앨범의 숨긴 곡 — C7sus4에서 사라진다).
% 공개용 스냅샷에 실린다(2026-10-08, 제안자가 공개 범위를 넓혔다).
\version "2.24.0"
\include "헌정곡_2안_공통.ily"

\score {
  <<
    \new Staff \with { midiInstrument = "voice oohs" midiMaximumVolume = #0.95 } <<
      \new Voice { \melody }
      \new Voice { \tempo 4 = 84 s2.*42 \tempo 4 = 76 s2.*8 \tempo 4 = 44 s2. \tempo 4 = 88 s2.*12 \tempo 4 = 80 s2.*4 \tempo 4 = 40 s2. }
    >>
    \new Staff \with { midiInstrument = "tenor sax" midiMaximumVolume = #0.8 } { \global
  R2.*15 |
  r2 r8 c8 | f8.\mp f16 f4 g4 | a8. a16 a4. a8 | g8 a8 bes4 e4 | g4 f2 | c'8 a8 d'4. c'8 | c'8 bes8 bes4. bes8 | bes8 g8 c'4. bes8 | bes8 a8 a2 |
  R2.*12 |
  a4\mp c'4 d'4 | c'2 bes4 | bes2. | a2. | bes4 a4 g4 | g2 cis'4 |
  R2.*9 |
  c''2.\mf | a'2 g'4 | f'2 e'4 | e'4 f'2 | es'4 d'2 | d'2 e'4 | bes'2. | a'2. | c''2. | a'2 g'4 | f'2 e'4 | f'2. |
  bes'4\mp a'4 g'4 | f'2.~ | f'2. | e'2. | f'2.\fermata |
    }
    \new Staff \with { midiInstrument = "acoustic guitar (nylon)" midiMaximumVolume = #0.75 } { \global
  f,8\mp g8 a8 c'8 a8 g8 |
  e8 f8 a8 c'8 a8 f8 |
  d,8 f8 a8 c'8 a8 f8 |
  c,8 f8 g8 bes8 c,8 bes8 |
  f,8\mp g8 a8 c'8 e8 c'8 |
  d,8 f8 a8 c'8 a8 f8 |
  g,8 f8 bes8 d'8 c,8 bes8 |
  c,8 g8 f,8 a8 c'8 a'8 |
  f,8 c'8 bes,,8 f8 d'8 f'8 |
  c,8 f8 g8 bes8 g8 f8 |
  c,8 g8 bes8 e'8 bes8 g8 |
  f,8 a8 c'8 a'8 c'8 a8 |
  f,8 g8 a8 c'8 e8 c'8 |
  d,8 f8 a8 c'8 a8 f8 |
  g,8 f8 bes8 d'8 c,8 bes8 |
  c,8 bes8 f,8 a8 c'8 a'8 |
  f,8 g8 a8 c'8 e8 c'8 |
  d,8 f8 a8 c'8 a8 f8 |
  g,8 f8 bes8 d'8 c,8 bes8 |
  c,8 g8 f,8 a8 c'8 a'8 |
  f,8 c'8 bes,,8 f8 d'8 f'8 |
  c,8 f8 g8 bes8 g8 f8 |
  c,8 g8 bes8 e'8 bes8 g8 |
  f,8 a8 c'8 a'8 c'8 a8 |
  f,8 a8 c'8 a'8 a,8 d'8 |
  d,8 f8 a8 c'8 c,8 a8 |
  bes,,8 f8 a8 d'8 c,8 bes8 |
  c,8 g8 f,8 a8 c'8 a'8 |
  f,8 c'8 bes,,8 f8 d'8 f'8 |
  c,8 f8 g8 bes8 g8 f8 |
  c,8 f8 g8 bes8 c,8 bes8 |
  f,8 a8 c'8 a'8 c'8 a8 |
  f,8 g8 a8 c'8 e8 c'8 |
  d,8 f8 a8 c'8 d,8 a8 |
  g,8 f8 bes8 d'8 c,8 bes8 |
  c,8 bes8 f,8 a8 c'8 a'8 |
  f,8 c'8 bes,,8 f8 d'8 f'8 |
  c,8 f8 g8 bes8 g8 f8 |
  c,8 g8 bes8 e'8 bes8 g8 |
  f,8 a8 c'8 a'8 c'8 a8 |
  g,8 f8 bes8 d'8 bes8 f8 |
  e8 g8 bes8 d'8 a,8 cis'8 |
  d,8\p f8 a8 f'8 c,8 a8 |
  bes,,8 f8 a8 d'8 a8 f8 |
  g,8 f8 bes8 d'8 bes8 f8 |
  a,8 g8 d'8 e'8 a,8 cis'8 |
  bes,,8 f8 a8 d'8 a8 f8 |
  c,8 g8 d'8 e'8 d'8 g8 |
  a,8 f8 c'8 f'8 c'8 f8 |
  c,8 f8 g8 bes8 g8 f8 |
  c,8 f8 g8 bes8 g8 f8 |
  f,8\mf a8 c'8 a'8 e8 c'8 |
  d,8 f8 a8 c'8 c,8 a8 |
  bes,,8 f8 a8 d'8 c,8 bes8 |
  c,8 bes8 f,8 a8 c'8 a'8 |
  f,8 c'8 bes,,8 f8 d'8 f'8 |
  g,8 f8 bes8 d'8 f,8 bes8 |
  e8 bes8 e8 g8 bes8 c'8 |
  f,8 a8 c'8 a'8 c'8 a8 |
  f,8 a8 c'8 a'8 e8 c'8 |
  d,8 f8 a8 c'8 fis,8 c'8 |
  g,8 f8 bes8 d'8 c,8 bes8 |
  c,8 f8 g8 bes8 g8 f8 |
  c,8\mp f8 g8 bes8 g8 f8 |
  c,8 f8 g8 bes8 g8 f8 |
  c,8 f8 g8 bes8 g8 f8 |
  c,8 g8 bes8 e'8 bes8 g8 |
  <f, c f a c'>2.\fermata |
    }
    \new DrumStaff \with { midiMaximumVolume = #0.45 } \drummode {
  R2.*16 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  R2.*9 |
  bd4\mp sn8 sn8 sn4 |
  bd4\mp sn8 sn8 sn4 |
  bd4\mp sn8 sn8 sn4 |
  bd4\mp sn8 sn8 sn4 |
  bd4\mp sn8 sn8 sn4 |
  bd4\mp sn8 sn8 sn4 |
  bd4\mp sn8 sn8 sn4 |
  bd4\mp sn8 sn8 sn4 |
  bd4\mp sn8 sn8 sn4 |
  bd4\mp sn8 sn8 sn4 |
  bd4\mp sn8 sn8 sn4 |
  bd4\mp sn8 sn8 sn4 |
  bd2.\p |
  R2.*4 |
    }
  >>
  \midi { }
}

\score {
  <<
    \new Staff \with { midiInstrument = "voice oohs" midiMaximumVolume = #0.95 } <<
      \new Voice { \melody }
      \new Voice { \tempo 4 = 84 s2.*42 \tempo 4 = 76 s2.*8 \tempo 4 = 44 s2. \tempo 4 = 88 s2.*12 \tempo 4 = 80 s2.*4 }
    >>
    \new Staff \with { midiInstrument = "tenor sax" midiMaximumVolume = #0.8 } { \global
  R2.*15 |
  r2 r8 c8 | f8.\mp f16 f4 g4 | a8. a16 a4. a8 | g8 a8 bes4 e4 | g4 f2 | c'8 a8 d'4. c'8 | c'8 bes8 bes4. bes8 | bes8 g8 c'4. bes8 | bes8 a8 a2 |
  R2.*12 |
  a4\mp c'4 d'4 | c'2 bes4 | bes2. | a2. | bes4 a4 g4 | g2 cis'4 |
  R2.*9 |
  c''2.\mf | a'2 g'4 | f'2 e'4 | e'4 f'2 | es'4 d'2 | d'2 e'4 | bes'2. | a'2. | c''2. | a'2 g'4 | f'2 e'4 | f'2. |
  bes'4\mp\> a'4 g'4 | f'2.~ | f'2.~ | f'2.\ppp |
    }
    \new Staff \with { midiInstrument = "acoustic guitar (nylon)" midiMaximumVolume = #0.75 } { \global
  f,8\mp g8 a8 c'8 a8 g8 |
  e8 f8 a8 c'8 a8 f8 |
  d,8 f8 a8 c'8 a8 f8 |
  c,8 f8 g8 bes8 c,8 bes8 |
  f,8\mp g8 a8 c'8 e8 c'8 |
  d,8 f8 a8 c'8 a8 f8 |
  g,8 f8 bes8 d'8 c,8 bes8 |
  c,8 g8 f,8 a8 c'8 a'8 |
  f,8 c'8 bes,,8 f8 d'8 f'8 |
  c,8 f8 g8 bes8 g8 f8 |
  c,8 g8 bes8 e'8 bes8 g8 |
  f,8 a8 c'8 a'8 c'8 a8 |
  f,8 g8 a8 c'8 e8 c'8 |
  d,8 f8 a8 c'8 a8 f8 |
  g,8 f8 bes8 d'8 c,8 bes8 |
  c,8 bes8 f,8 a8 c'8 a'8 |
  f,8 g8 a8 c'8 e8 c'8 |
  d,8 f8 a8 c'8 a8 f8 |
  g,8 f8 bes8 d'8 c,8 bes8 |
  c,8 g8 f,8 a8 c'8 a'8 |
  f,8 c'8 bes,,8 f8 d'8 f'8 |
  c,8 f8 g8 bes8 g8 f8 |
  c,8 g8 bes8 e'8 bes8 g8 |
  f,8 a8 c'8 a'8 c'8 a8 |
  f,8 a8 c'8 a'8 a,8 d'8 |
  d,8 f8 a8 c'8 c,8 a8 |
  bes,,8 f8 a8 d'8 c,8 bes8 |
  c,8 g8 f,8 a8 c'8 a'8 |
  f,8 c'8 bes,,8 f8 d'8 f'8 |
  c,8 f8 g8 bes8 g8 f8 |
  c,8 f8 g8 bes8 c,8 bes8 |
  f,8 a8 c'8 a'8 c'8 a8 |
  f,8 g8 a8 c'8 e8 c'8 |
  d,8 f8 a8 c'8 d,8 a8 |
  g,8 f8 bes8 d'8 c,8 bes8 |
  c,8 bes8 f,8 a8 c'8 a'8 |
  f,8 c'8 bes,,8 f8 d'8 f'8 |
  c,8 f8 g8 bes8 g8 f8 |
  c,8 g8 bes8 e'8 bes8 g8 |
  f,8 a8 c'8 a'8 c'8 a8 |
  g,8 f8 bes8 d'8 bes8 f8 |
  e8 g8 bes8 d'8 a,8 cis'8 |
  d,8\p f8 a8 f'8 c,8 a8 |
  bes,,8 f8 a8 d'8 a8 f8 |
  g,8 f8 bes8 d'8 bes8 f8 |
  a,8 g8 d'8 e'8 a,8 cis'8 |
  bes,,8 f8 a8 d'8 a8 f8 |
  c,8 g8 d'8 e'8 d'8 g8 |
  a,8 f8 c'8 f'8 c'8 f8 |
  c,8 f8 g8 bes8 g8 f8 |
  c,8 f8 g8 bes8 g8 f8 |
  f,8\mf a8 c'8 a'8 e8 c'8 |
  d,8 f8 a8 c'8 c,8 a8 |
  bes,,8 f8 a8 d'8 c,8 bes8 |
  c,8 bes8 f,8 a8 c'8 a'8 |
  f,8 c'8 bes,,8 f8 d'8 f'8 |
  g,8 f8 bes8 d'8 f,8 bes8 |
  e8 bes8 e8 g8 bes8 c'8 |
  f,8 a8 c'8 a'8 c'8 a8 |
  f,8 a8 c'8 a'8 e8 c'8 |
  d,8 f8 a8 c'8 fis,8 c'8 |
  g,8 f8 bes8 d'8 c,8 bes8 |
  c,8 f8 g8 bes8 g8 f8 |
  c,8\mp\> f8 g8 bes8 g8 f8 |
  c,8 f8 g8 bes8 g8 f8 |
  c,8 f8 g8 bes8 g8 f8 |
  c,8 f8 g8 bes8 g8 f8\ppp |
    }
    \new DrumStaff \with { midiMaximumVolume = #0.45 } \drummode {
  R2.*16 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  bd4\pp sn4 sn4 |
  R2.*9 |
  bd4\mp sn8 sn8 sn4 |
  bd4\mp sn8 sn8 sn4 |
  bd4\mp sn8 sn8 sn4 |
  bd4\mp sn8 sn8 sn4 |
  bd4\mp sn8 sn8 sn4 |
  bd4\mp sn8 sn8 sn4 |
  bd4\mp sn8 sn8 sn4 |
  bd4\mp sn8 sn8 sn4 |
  bd4\mp sn8 sn8 sn4 |
  bd4\mp sn8 sn8 sn4 |
  bd4\mp sn8 sn8 sn4 |
  bd4\mp sn8 sn8 sn4 |
  bd2.\p |
  R2.*3 |
    }
  >>
  \midi { }
}
