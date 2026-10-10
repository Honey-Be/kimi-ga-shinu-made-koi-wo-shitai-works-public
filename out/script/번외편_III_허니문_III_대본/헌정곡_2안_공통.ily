% 번외편 III 헌정곡 「해송」 2안 — 리드시트와 음원용이 함께 쓰는 정의(선율 · 가사 · 코드).
% 공개용 스냅샷에 실린다(2026-10-08, 제안자가 공개 범위를 넓혔다).

global = { \key f \major \time 3/4 }

% ───────── 선율 ─────────
verseAB = {
  % A (줄 1–2)
  f'8. f'16 f'4 g'4 | a'8. a'16 a'4. a'8 | g'8 a'8 bes'4 e'4 | g'4 f'4 r8 c''8 |
  % B (줄 3–4)
  c''8 a'8 d''4. c''8 | c''8 bes'8 bes'4. bes'8 | bes'8 g'8 c''4. bes'8 | bes'8 a'8 a'4 r8 c'8 |
  % A (줄 5–6)
  f'8. f'16 f'4 g'4 | a'8. a'16 a'4. a'8 | g'8 a'8 bes'4 e'4 |
}

melody = \relative c' {
  \global
  \tempo "Andante — 개량 기타 홀로" 4 = 84
  % 인트로 4마디
  \mark \markup \box "Intro"
  R2.*3 | r2 r8 c8 |
  \bar "||"
  \mark \markup \box "1절"
  \absolute { \verseAB g'4 f'4 r4 | }
  \bar "||"
  \mark \markup \box "간주 1 — 색소폰"
  R2.*7 | r2 r8 \absolute { c'8 } |
  \bar "||"
  \mark \markup \box "2절"
  \absolute { \verseAB g'4 f'4 r4 | }
  \bar "||"
  \mark \markup \box "간주 2 — 색소폰 대선율"
  R2.*6 |
  \bar "||"
  \mark \markup \box "Bridge — d단조, 루바토"
  \absolute {
    d'8 e'8 f'4 a'4 | a'8 g'8 f'4 d'4 |
    d'8 e'8 f'4 g'4 | a'4. g'8 e'4 |
    f'8 g'8 a'8 bes'8 c''4 | c''8 d''8 e''4 c''4 |
    c''4 a'8 g'8 r4 | g'4 a'4 bes'4 | c''2\fermata r8 c'8 |
  }
  \bar "||"
  \mark \markup \box "3절 — f, 전조 없음"
  \absolute { \verseAB g'4 f'4 r4 | }
  \bar "||"
  \mark \markup \box "Outro"
  R2.*5 |
  \bar "|."
}

% 색소폰 아웃트로(큐) — 같은 보표의 둘째 성부
saxOutro = \relative c'' {
  \global
  \skip 2.*4 \skip 2.*12 \skip 2.*8 \skip 2.*12 \skip 2.*6 \skip 2.*9 \skip 2.*12
  bes4^\markup \italic "Sax (테너, 실음)" a g | f2.~ | f2.^\markup \small "녹음본: 여기서 페이드아웃(물음)" | e2.^\markup \small "무대만: E → F" | f2.\fermata |
}

% ───────── 가사 ─────────
words = \lyricmode {
  % 1절
  오 해 -- 송 -- 아, 오 해 -- 송 -- 아 한 -- 결 -- 같 -- 은 네 잎 -- 새
  바 -- 닷 -- 바 -- 람 찬 밤 -- 에 -- 도 내 곁 -- 에 푸 -- 르 -- 게 선 너
  오 해 -- 송 -- 아, 오 해 -- 송 -- 아 한 -- 결 -- 같 -- 은 네 잎 -- 새
  % 2절
  봄 -- 과 여 -- 름, 가 -- 을 겨 -- 울 너 -- 와 하 -- 나 -- 씩 셀 -- 래
  정 -- 해 -- 진 것 없 -- 는 날 -- 들 그 날 -- 들 -- 을 전 -- 부 너 -- 와
  봄 -- 과 여 -- 름, 가 -- 을 겨 -- 울 하 -- 나 -- 씩 세 -- 어 갈 -- 래
  % 브릿지
  파 -- 도 -- 는 오 -- 고 또 가 -- 도
  너 -- 는 여 -- 기 서 있 -- 어
  그 -- 러 -- 니 나 -- 도 여 -- 기 설 -- 게
  네 곁 -- 에 오 -- 늘 -- 부 -- 터
  % 3절
  오 해 -- 송 -- 아, 오 해 -- 송 -- 아 내 곁 -- 에 있 -- 어 줄 -- 래
  남 -- 은 봄 -- 과 남 -- 은 겨 -- 울 남 -- 은 날 -- 을 전 -- 부 나 -- 와
  오 해 -- 송 -- 아, 오 해 -- 송 -- 아 내 곁 -- 에 있 -- 어 줄 -- 래
}

% ───────── 코드 ─────────
% 2026-10-04 개정 — 박일곤 〈소나무〉(《O Tannenbaum》의 다른 개작)의 *장조 구간 둘*(A♭장조 · B♭장조)에서 *기법만* 빌려 F장조로 옮겼다:
% 부속화음 V/vi(A7sus4 → Dm) · V/ii(D7 → Gm7) · 경과 감7(F♯°7 → Gm7) · viiø7(Em7♭5) · 베이스 걸음(F → Fmaj7/E → Dm7 · G → F → E → F) · V7sus4 · add9.
% 진행 자체를 옮기지 않았다. 절마다 색을 달리한다 — 1절 담백 · 2절 부속화음 · 3절 베이스 걸음과 경과 감7(전조 없음).
chordsVerseOne = \chordmode {
  f2:9^7 c4/e | d2.:m7 | g2:m7 c4:7 | c4:sus4.7 f2 |
  f4:7 bes2 | g2.:m7/c | c2.:7 | f2. |
  f2:9^7 c4/e | d2.:m7 | g2:m7 c4:7 | c4:7 f2 |
}
chordsVerseTwo = \chordmode {
  % A — 첫 마디 끝에 V/vi(A7sus4)를 끼워 Dm7로
  f2 a4:sus4.7 | d2:m7 d4:m7/c | bes2:maj7 c4:7 | c4:sus4.7 f2 |
  % B
  f4:7 bes2 | g2.:m7/c | c2:sus4.7 c4:7 | f2. |
  % A — 「봄과 여름 …」 둘째 마디 끝에 V/ii(D7 → Gm7)
  f2:9^7 c4/e | d2:m7 d4:7 | g2:m7 c4:7 | c4:7 f2 |
}
chordsVerseThree = \chordmode {
  % A
  f2 c4/e | d2:m7 d4:m7/c | bes2:maj7 c4:7 | c4:7 f2 |
  % B — 베이스가 G → F → E → F로 걷는다(Gm7 · Gm7/F · Em7♭5 · C7/E → F)
  f4:7 bes2 | g2:m7 g4:m7/f | e4:m7.5- c2:7/e | f2. |
  % A — 경과 감7(F♯°7 → Gm7), 끝마디 C7sus4: 선율의 마지막 F가 sus4가 되어 「줄래」가 풀리지 않는다
  f2 c4/e | d2:m7 fis4:dim7 | g2:m7 c4:7 | c2.:sus4.7 |
}
harmony = \chordmode {
  \set chordChanges = ##t
  % 인트로 — 베이스가 F → E → D → C로 걷는다
  f2.:9^7 | f2.:maj7/e | d2.:m7 | g2:m7/c c4:7 |
  % 1절
  \chordsVerseOne
  % 간주 1 — 1절의 A · B
  f2:9^7 c4/e | d2.:m7 | g2:m7 c4:7 | c4:sus4.7 f2 |
  f4:7 bes2 | g2.:m7/c | c2.:7 | f2. |
  % 2절
  \chordsVerseTwo
  % 간주 2 — d단조의 iiø7 – V7로 넘긴다
  f4:7 bes2 | g2.:m7/c | c2.:7 | f2. | g2.:m7 | e2:m7.5- a4:7 |
  % 브릿지 (d단조)
  d2:m d4:m/c | bes2.:maj7 | g2.:m7 | a2:sus4.7 a4:7 |
  bes2.:maj7 | c2.:9^7 | f2./a | g2.:m7/c | c2.:sus4.7 |
  % 3절
  \chordsVerseThree
  % 아웃트로 — C2 페달. 녹음본은 C7sus4에서 페이드아웃, 무대는 Gm7/C → C7 → F
  c2.:sus4.7 | c2.:sus4.7 | g2.:m7/c | c2.:7 | f2. |
}
