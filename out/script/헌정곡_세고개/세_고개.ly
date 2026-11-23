\version "2.24.0"
#(set-global-staff-size 17.5)

\header {
  title = "세 고개"
  subtitle = "키이란이 에이란에게 헌정한 아리랑"
  subsubtitle = "원전 v2.12 (RULES 315) · 윤병익 원작 채보 (MusicXML) 정본"
  composer = "작사·작곡: 키이란 (Kiiran)"
  arranger = "채보: 윤병익"
  tagline = ##f
}

\paper {
  #(set-paper-size "a4")
  property-defaults.fonts.serif = "Noto Serif CJK KR"
  property-defaults.fonts.sans = "Noto Sans CJK KR"
  indent = 0
  top-margin = 12\mm
  bottom-margin = 12\mm
  left-margin = 14\mm
  right-margin = 14\mm
  ragged-last-bottom = ##t
}

global = {
  \key g \minor
  \time 4/4
  \tempo "Slow Ballad — 서정적이고 애절하게" 4 = 66
}

harmonies = \chordmode {
  g1:m | % 1
  bes1 | % 2
  c2:m f2 | % 3
  g1:m | % 4
  g1:m | % 5
  f2 g2:m | % 6
  bes1 | % 7
  d1:m | % 8
  g2:m bes2 | % 9
  c2:m g2:m | % 10
  bes2 f2 | % 11
  g1:m | % 12
  g1:m | % 13
  bes1 | % 14
  g1:m | % 15
  bes2 d2:m | % 16
  g2:m bes2 | % 17
  c2:m g2:m | % 18
  bes1 | % 19
  c2:m g2:m | % 20
  bes2 f2 | % 21
  g1:m | % 22
  g1:m | % 23
  bes1 | % 24
  c1:m | % 25
  bes2 d2:m | % 26
  g1:m | % 27
  bes2 g2:m | % 28
  bes2 f2 | % 29
  g1:m | % 30
  g1:m | % 31
  bes1 | % 32
  c2:m ees2 | % 33
  bes2 d2:m | % 34
  g2:m bes2 | % 35
  c2:m g2:m | % 36
  bes2 f2 | % 37
  g1:m | % 38
  g2:m bes2 | % 39
  c2:m g2:m | % 40
  s2 bes2 | % 41
  s2 ees2 | % 42
  g1:m | % 43
  s2 g2:m | % 44
  g1:m | % 45
}

melody = {
  \global
  \mark \markup \box "Intro"
  R1 | % 1
  R1 | % 2
  R1 | % 3
  R1 | % 4
  \bar "||" \mark \markup \box "1절"
  g4. bes8 d'2 | % 5
  c'16 d'8. c'8 bes8 g2 | % 6
  r8 bes16 d'16 d'8 d'16 f'16~ f'16 f'16 f'8 g'8 f'8 | % 7
  d'8 d'4 f'8 d'2 | % 8
  \bar "||" \mark \markup \box "후렴"
  r8. g'16 g'8 f'8 d'4. c'8 | % 9
  c'16 c'8. c'8 bes8 g2 | % 10
  r8 d16 f8 g16 g8 d'8 c'16 bes16 g8 f8 | % 11
  g1 | % 12
  \bar "||" \mark \markup \box "2절"
  r8. d'16 d'8 d'8 d'8. f'8 g'16 bes'16 g'16 | % 13
  f'4. g'8 d'2 | % 14
  r8 f'8 g'16 g'8 bes'16 bes'16 bes'16 bes'8 g'16 f'16 d'8 | % 15
  d'4. f'8 d'2 | % 16
  g'8. g'16 g'8 f'8 d'2 | % 17
  c'8. d'16 c'8 bes8 g2 | % 18
  \bar "||" \mark \markup \box "후렴"
  r8. bes16 bes8 c'8 d'4. c'16 bes16 | % 19
  c'16 c'8. c'8 bes16 g16 g2 | % 20
  r8 d16 f8 g16 g8 d'8 c'16 bes16 g8 f8 | % 21
  g1~ | % 22
  \bar "||" \mark \markup \box "간주 (Interlude)"
  g1 | % 23
  R1 | % 24
  R1 | % 25
  R1 | % 26
  R1 | % 27
  R1 | % 28
  R1 | % 29
  \bar "||" \mark \markup \box "3절"
  r2. d'16 f'8. | % 30
  g'4. g'8 g'2 | % 31
  f'8. g'8. f'8 d'4. c'16 bes16 | % 32
  r8 c'16 c'16 c'8 d'8 c'16 bes16 bes16 g8 g8 bes16~ | % 33
  bes16 d'2... | % 34
  \bar "||" \mark \markup \box "후렴"
  r8. g'16 g'8 f'16 d'16 d'4. c'16 bes16 | % 35
  c'16 c'8. c'8 bes16 g16 g2 | % 36
  r8 d16 f8 g16 g8 d'8 c'16 bes16 g8 f8 | % 37
  g1 | % 38
  \bar "||" \mark \markup \box "끝 후렴"
  r8. g'16 g'8 f'16 d'16 d'4. c'16 bes16 | % 39
  c'16 c'8. c'8 bes16 g16 g2 | % 40
  r8. f16 g16 bes16 c'16 d'4 f'8 d'8 c'16~ | % 41
  c'16 bes8 g8 f16 g2~ g8~ | % 42
  \bar "||" \mark \markup \box "Outro"
  g1 | % 43
  R1 | % 44
  R1 | % 45
  \bar "|."
}

words = \lyricmode {
  % m.05
  "언" "덕" "위"
  % m.06
  "작" "은" "돌" "앞" "에"
  % m.07
  "먼" "저" "와" "앉" "은" "사" "람" "이" "있"
  % m.08
  _ "었" "어" "요"
  % m.09
  "넘" "어" "가" "요" "한"
  % m.10
  "고" "개" "두" "고" "개"
  % m.11
  "셋" "이" "서" "넘" "던" "길" "이" "었" "대"
  % m.12
  "요"
  % m.13
  "울" "어" "도" "괜" "찮" "아" "요" _
  % m.14
  "울" "음" "도"
  % m.15
  "한" "소" "절" _ "노" "래" "가" "되" _ "는"
  % m.16
  "거" "니" "까"
  % m.17
  "다" "받" "았" "어" "요"
  % m.18
  "다" "받" "았" "어" "요"
  % m.19
  "넘" "어" "가" "요," "한" _
  % m.20
  "고" "개" "두" "고" _ "개"
  % m.21
  "셋" "이" "서" "넘" "던" "길" "이" "었" "대"
  % m.22
  "요"
  % m.30
  "저" "녁"
  % m.31
  "밥" "짓" "는"
  % m.32
  "냄" "새" "처" "럼" "문" "득"
  % m.33
  "돌" "아" "보" "면" "거" _ "기" "있" "는" "사"
  % m.34
  "람"
  % m.35
  "넘" "어" "가" _ "요" "한" _
  % m.36
  "고" "개" "두" "고" _ "개"
  % m.37
  "셋" "이" "서" "넘" "던" "길" "이" "었" "대"
  % m.38
  "요"
  % m.39
  "넘" "어" "가" _ "요" "한" _
  % m.40
  "고" "개" "두" "고" _ "개"
  % m.41
  "세" "사" "람" _ "이" "웃" "고" "있"
  % m.42
  "을" "거" "예" "요"
}

\score {
  <<
    \new ChordNames { \harmonies }
    \new Staff \with {
      instrumentName = "Vocal"
      midiInstrument = "acoustic grand"
    } {
      \new Voice = "singer" { \melody }
    }
    \new Lyrics \lyricsto "singer" { \words }
  >>
  \layout {
    \context {
      \Staff
      \consists "Ambitus_engraver"
    }
  }
  \midi { }
}
