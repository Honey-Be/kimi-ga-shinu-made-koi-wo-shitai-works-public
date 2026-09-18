# 〈비창〉 1악장 시퀀스 — 대본·덱·동기 재생 데모

『きみが死ぬまで恋をしたい』(あおのなち / 一迅社)의 **비공식 2차 창작**. 차이코프스키 교향곡 6번 「비창」 1악장(18:29)을 배경음악으로 쓰는 한 시퀀스의 **대본**과, 그것을 touying 슬라이드로 옮겨 **재생 위치에 맞춰 강조하는 웹 데모**, 그리고 **인물관계도 도표**를 담는다.

> 이것은 팬이 쓴 구상이다. 원작의 공식 자료가 아니고, 원작자·출판사의 승인이나 후원을 받지 않았다.
> 원작에 관한 모든 권리는 원작자와 출판사에 있다.

---

## 무엇이 있나

```
out/bgm/11_비창_1악장_시퀀스_대본/
    script_{ko,ja}.md      대본 — 한국어 / 일본어, Markdown
    script_{ko,ja}.typ     같은 대본, Typst (>= 0.14)
    cues.json              음원 파형에서 잡은 구간·비트 시각
    demo/
        slides_{ko,ja}.typ 생성물 — 대본을 touying 덱으로(표지 1 + 비트 52 = 53쪽)
        README.md          덱과 데모가 어떻게 만들어지는가

docs/_diagrams/
    kimishinu_relations_{ko,ja}_v2.2.typ    인물관계도 — 계승전쟁 셋을 축으로 네 장

tools/
    pathetique_demo_build.py   대본 → 덱 생성 · 정합 검사(gen / check)
    pathetique_demo_e2e.py     playwright 헤드리스 검증(데스크톱 + 모바일)
    relations_diagram_gen.py   인물관계도 생성기(KO/JA 한 데이터)

web/
    pathetique-sync/    Astro 7 앱 — 재생 위치로 덱 페이지를 갈아끼우고 비트를 강조
    touying-exporter/   submodule — touying-exporter 의 fork(MIT).
                        Typst 0.15.x 대응 · `--format astro` · 페이지 메타데이터 · Astro 통합
```

## 데모가 하는 일

`<audio>`의 재생 위치 → 비트 이분탐색 → 덱 페이지 교체. 동기 표의 원천은 **덱 자신**이다 — 각 비트 페이지에 Typst 메타데이터

```typst
#context [#metadata((page: here().page(), beat: 26, t_sec: 420.0, …)) <sync-beat>]
```

를 심고, fork 가 `--query-label sync-beat` 로 그것을 모아 `manifest.json` 에 페이지별로 붙인다. 별도의 sync.json 이 없다.

폰에서는 슬라이드 글자가 작아 읽을 수 없으므로, 각 비트의 **전문**을 메타데이터에 함께 실어 목록에서 현재 비트만 펼친다. 「크게 보기」는 전체화면 API 가 되면 그것으로, 안 되면 CSS 오버레이 + 세로 화면에서 덱 90° 회전.

### 쓰는 법

```sh
just demo-setup audio=/path/to/your.m4a   # submodule · uv venv · pnpm · (선택) 음원 복사
just demo-slides                          # 대본 → 덱 → typst 컴파일 53쪽 확인
just demo-build                           # Astro 빌드 (integration 이 덱을 SVG 로 내보낸다)
just demo-check                           # manifest ↔ 대본 ↔ cues.json 대조(오래된 덱 검출 포함)
just demo-e2e                             # playwright — 데스크톱 8지점 + 모바일 세로/가로
just relations                            # 인물관계도 .typ 다시 생성
```

**음원은 이 저장소에 없다.** 차이코프스키는 공유저작물이나 *녹음*은 아니다 — 권리 확인 전에는 넣지 않는다. 각자 자기 사본을 쓴다(데모가 쓴 것은 카라얀 / 베를린 필하모닉, 18:29.1).

## 이 저장소에 없는 것

이것은 더 큰 비공개 작업 저장소의 **공개용 스냅샷**이다. 다음은 담기지 않았다.

- **원전** — 결말 구상 통합 문서와 동반 문서, 프리퀄, 비교분석
- `proposals/` (판본별 제안·결정 기록), `briefs/` (작업 규칙 요약), `index/`
- 대본의 `check.md`(정합성 검사)와 `JUDGMENT.md`(판정 기준)
- 작업 규칙 문서(CLAUDE.md·HANDOVER.md)와 해시 매니페스트

그래서 여기 있는 파일이 **`원전`·`proposals/P64`·`check.md`·`docs/kimishinu_merged_…` 를 가리키는 곳이 있다.** 그 참조는 비공개 저장소를 가리키며, 일부러 함께 싣지 않았다 — 대본 문면은 검사 당시 그대로 두는 편이 낫다고 보았다.

## 대사에 관하여

대본의 대사는 **전부 원작자의 것이 아니라 이 구상의 것**이다. 원전 큐 표가 적은 *내용*을 말로 옮긴 것이며, 문면은 2026-09-18에 구상자가 정했다. 원작이 이 장면을 달리 그리면 이 층은 함께 무효다.

## 라이선스

**NEWSNIPER Ethical Public License v1 (NEPLv1)** — `LICENSE`(적용 고지)와 `LICENSES/` 를 본다.

| | |
|---|---|
| `tools/` · `web/pathetique-sync/` · `justfile` | 소프트웨어 부분 — 상업적 이용 허용, 동일조건 없음 |
| `out/` · `docs/` (대본·덱·도표) | 저작 부분 — **비상업 한정 + 동일조건** |
| `web/touying-exporter/` | 별도 라이선스 — **MIT** (© 2024 OrangeX4 및 기여자) |

**원작 권리자에 대한 특칙(제4조)** — あおのなち 및 一迅社는 이 저작물 전부를 **저작자 표시 의무 없이, 상업적 이용을 포함하여** 원작과 그 파생 저작물에 편입·개변·이용할 수 있다. 표시는 권장 사항일 뿐이다. 이 구상이 쓸모가 있다고 판단되면 그렇게 쓰시라고 만든 조항이다.

**금지 용도(제5조)** — 반인륜범죄·전쟁범죄·아동대상범죄에는 어떤 허락도 미치지 않는다. 학술·보도·인권 기록·교육·법 집행은 여기 해당하지 않는다.

NEPLv1 은 OSI 가 정의하는 「오픈소스」가 아니다(제5조의 이용 분야 제한 때문). 라이선스 정본: <https://github.com/newsniper-org/ethical-public-license>

## 원작 권리자께

이 저장소의 전부 또는 일부를 내리기를 원하시면 알려 주십시오. 그렇게 하겠습니다(NEPLv1 제6.4조).

---

*구상·대본: NEWSNIPER · 원작: あおのなち 『きみが死ぬまで恋をしたい』(一迅社)*
