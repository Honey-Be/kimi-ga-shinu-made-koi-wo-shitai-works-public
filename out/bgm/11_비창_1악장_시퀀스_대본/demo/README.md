# demo — 〈비창〉 1악장 시퀀스 대본을 배경음악에 맞춰 강조하는 로컬 데모

**로컬 전용(음원 때문).** 화면에 오르는 것은 이미 검사된 대본(`../script_{ko,ja}.typ`)의 문장뿐이고 새 사실은 없다. 두 자매의 대사 여섯 묶음은 **제안자가 문면을 정했다**(2026-09-18, 이 번들의 가안을 다듬은 것); 잠꼬대 둘과 마차 안 대사도 같은 날 정했다 — 대사 문면은 전부 제안자의 것이며, 마차 안의 셋(지명 발음·라우라의 덧붙임·대공의 호령)은 제안자가 허용한 규정 예외이며 원전 v2.1.15가 그것을 적는다(P63; 대본 규칙 4·10·14). **음원은 저장소에 없다** — 루트의 m4a 를 `web/pathetique-sync/public/audio/` 에 복사해 읽으며(`just demo-setup`; astro build 가 심링크를 dist 로 옮기지 않아 복사한다), `.gitignore` 가 `*.m4a` 와 그 디렉터리를 막는다. 음원은 저장소에 넣지도 배포하지도 않는다 — 권리 확인 전이기 때문이다. 각자 자기 사본을 `web/pathetique-sync/public/audio/pathetique-mvt1.m4a` 에 둔다.

## 무엇이 있나

| 파일 | 성격 |
|---|---|
| `slides_ko.typ` · `slides_ja.typ` | **생성물** — `tools/pathetique_demo_build.py gen` 이 `../script_{ko,ja}.typ` 에서 만든다. 손으로 고치지 않는다. touying 0.7.4, 16:9, 표지 1장 + 비트 52개 = 53쪽 |
| (web/pathetique-sync/) | Astro 7.3.3 앱 — `<audio>` 의 재생 위치로 덱의 페이지를 갈아끼우고 비트 목록을 강조한다 |
| (web/touying-exporter/) | touying-exporter 의 Honey-Be fork(submodule). `--format astro` 로 페이지별 SVG + `manifest.json` 을 낸다 |

## 어떻게 만드나

비트 = 대본에서 줄머리 `*M:SS*` 로 시작하는 것 — 문단 50개 + ` \` 이어쓰기 뒤에 다시 `*M:SS*` 로 시작하는 둘(10:25·13:20) = 52개. 한 비트가 한 서브슬라이드다 — 그 페이지에서 **현재 비트는 강조색, 지난 비트는 회색**. 각 비트 페이지에 Typst 메타데이터 `#context [#metadata((page: here().page(), beat:, t_sec:, …)) <sync-beat>]` 를 심고, fork 가 `--query-label sync-beat` 로 그것을 모아 `manifest.json` 에 페이지별로 붙인다. **이 manifest 가 동기 표의 유일한 원천**이다(별도 sync.json 없음). 표지(1쪽)에는 `<sync-meta>`(원본 `script_*.typ` 의 sha256 · 비트 수 · 생성기)를 심어, `check` 가 **오래된 덱·오래된 내보내기**를 잡는다 — `slides_*.typ` 를 메모리에서 다시 만들어 손에 있는 파일과 비교하고, manifest 의 sha256 을 지금의 원본과 대조한다. 대본의 `#line(length: 100%)` 같은 장식 문단은 덱에 옮기지 않으며, `_(…)_` 로 시작하는 문단만 흐린 주석으로, 그 밖의 평문 문단은 본문 크기 그대로 둔다. 구간마다 새 슬라이드, 줄 예산을 넘으면 같은 구간 안에서 나눈다(KO/JA 가 같은 자리에서 갈라지도록 두 언어 비용의 최대값으로 나눈다).

```
just demo-setup     # submodule + uv venv(editable) + pnpm install + 음원 복사(public/audio, gitignore)
just demo-slides    # gen → typst 컴파일 → 53쪽 확인
just demo-build     # astro build (integration 이 fork CLI 로 덱을 내보낸다)   |  just demo-dev
just demo-check     # manifest ↔ 원본 ↔ cues.json 대조
just demo-e2e       # playwright 헤드리스 확인 (dist 를 python 정적 서버·빈 포트로 띄운다 — astro preview 는 단일 인스턴스라 폰 확인용 preview 와 겹치지 않게; chromium 은 AAC 를 못 틀므로 pathetique.seek 로 시각 주입)
```

## 폰에서 (2026-09-18)

슬라이드는 16:9 그림이라 폰 폭에서는 글자를 읽을 수 없다. 그래서 각 비트의 메타데이터에 **전문**(`text` — 본문 + 인용 줄 단위 + 후속 문단, 마크업 제거)을 함께 심고, 목록에서 **현재 비트만 전문을 펼친다** — 폰에서는 목록이 읽는 화면이다. 키보드 대신 **이동 버튼**(‹‹ 구간 · ‹ 비트 · 비트 › · 구간 ›› · 크게)이 덱 아래 있고, **크게 보기**는 전체화면 API 가 되면 그것으로(가로 고정 시도), 안 되면(iPhone) CSS 오버레이로 — **세로 화면이면 덱을 90° 돌려** 긴 변을 쓴다. 크게 보는 중에는 스와이프로 비트를 오간다(세로 화면에서는 세로 스와이프). 세로 폰은 덱 위·목록 아래(목록만 스크롤), 가로 폰은 얇은 머리·발과 좁은 오른쪽 목록. `just demo-e2e` 가 390×844 세로·844×390 가로 뷰포트에서 전문 펼침·버튼 이동·크게 보기(회전·화면 안)·넘침 없음을 본다.

## 원본과 어긋나게 둔 것 없음 · 정한 것 셋

- **비단조 시각 둘**: `*4:24–4:45*`(264.0 s)가 `*4:24.3*` 뒤에, `*14:06–14:30*`(846.0 s)이 `*14:06.4*` 뒤에 온다. 대본은 그대로 두고 덱의 `t_sec` 만 앞 비트 + 2 초로 민다(`t_sec_raw` 보존, gen 이 경고를 낸다).
- **인용 안의 `*7:20–7:45*`**: 페이지를 만들지 않는다(대사 덩어리를 쪼개지 않기 위해). manifest 에 `sub: true` 로만 들어가 목록에서 들여쓰기로 보인다.
- **표지(1쪽)**: 첫 비트(0:00.0) 전에는 표지를 보여준다 — 실제로는 0초부터 첫 비트라 재생 중에는 나오지 않는다.

cues.json 의 `1:43`(총휴지)은 대본 .typ 의 `*1:42–1:46.1*` 에 해당하며 시각 표기만 다르다 — `check` 가 보고만 한다.
