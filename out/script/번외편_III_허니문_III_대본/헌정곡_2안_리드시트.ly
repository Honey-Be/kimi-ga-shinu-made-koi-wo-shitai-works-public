% 번외편 III — 미미가 숨겨 둔 곡 · 가제 「해송(海松)」 · 2안 리드시트 (2026-10-03)
% 원곡: 《O Tannenbaum》 — 공유 저작물(독일 민요, 가사 Ernst Anschütz 1824). 선율 · 리듬은 de.wikipedia 「O Tannenbaum」의 LilyPond 악보(G장조)를 F장조로 옮겼다.
% 이 번들이 지은 것: 한국어 가사 2안 · 브릿지 선율(d단조) · 전체 반주 코드 · 인트로 · 간주 · 아웃트로 · 색소폰 아웃트로 프레이즈.
% 컴파일: lilypond -o <출력경로> 헌정곡_2안_리드시트.ly
% 공개용 스냅샷에 실린다(2026-10-08, 제안자가 공개 범위를 넓혔다).
\version "2.24.0"
#(set-global-staff-size 17)

\header {
  title = "해송 (가제)"
  subtitle = "미미가 숨겨 둔 곡 — 2안 리드시트"
  composer = "선율: 《O Tannenbaum》(독일 민요)"
  arranger = "가사 · 브릿지 선율 · 코드: 2안"
  tagline = ##f
}

\paper {
  #(set-paper-size "a4")
  property-defaults.fonts.serif = "Noto Serif CJK KR"
  property-defaults.fonts.sans = "Noto Sans CJK KR"
  indent = 0

  ragged-last-bottom = ##t
}

\include "헌정곡_2안_공통.ily"

\score {
  <<
    \new ChordNames \harmony
    \new Staff \with { instrumentName = "보컬" } <<
      \new Voice = "mel" { \voiceOne \melody }
      \new Voice { \voiceTwo \saxOutro }
    >>
    \new Lyrics \lyricsto "mel" \words
  >>
  \layout { }
  \midi { \tempo 4 = 84 }
}
