# 『네가 죽을 때까지 사랑하고 싶어』 결말 구상 파생 콘텐츠 — 공개용 스냅샷
# 원전 PDF: just compile · 데모: setup → slides → build(또는 dev) → check → e2e
set shell := ["bash", "-euo", "pipefail", "-c"]

fonts := "--font-path /usr/share/fonts/noto-cjk --font-path /usr/share/fonts/nanum"
web := "web/pathetique-sync"
demo := "out/bgm/_combined"
vpy := web + "/.venv/bin/python"
fontdirs := "/usr/share/fonts/noto-cjk /usr/share/fonts/nanum"

# 음원 셋은 저장소에 없다. 자기 사본의 경로를 넘긴다 — 주지 않은 곡은 건너뛴다.
#   just demo-setup audio_dv="/path/dvorak.m4a" audio_br="/path/brahms5.flac" audio_tc="/path/pathetique.m4a"
# 자르거나 이어붙이지 않는다. 그대로 복사할 뿐이다(재인코딩 0).
audio_dv := ""
audio_br := ""
audio_tc := ""

default:
    @just --list --unsorted

# submodule + uv venv(editable) + pnpm install + (선택) 음원 복사
demo-setup:
    git submodule update --init web/touying-exporter
    uv venv {{web}}/.venv --python 3.14
    uv pip install --python {{vpy}} -e "web/touying-exporter[test]"
    cd {{web}} && pnpm install
    @mkdir -p {{web}}/public/audio
    @if [ -n "{{audio_dv}}" ]; then cp -f "{{audio_dv}}" {{web}}/public/audio/dvorak-songs-my-mother.m4a && echo "드보르자크 복사"; else echo "드보르자크 없음"; fi
    @if [ -n "{{audio_br}}" ]; then cp -f "{{audio_br}}" {{web}}/public/audio/brahms-requiem-v.flac && echo "브람스 복사"; else echo "브람스 없음"; fi
    @if [ -n "{{audio_tc}}" ]; then cp -f "{{audio_tc}}" {{web}}/public/audio/pathetique-mvt1.m4a && echo "차이코프스키 복사"; else echo "차이코프스키 없음"; fi
    @echo "없는 곡은 재생되지 않는다 — 목록·막대로 탐색은 된다"

# fork(touying-exporter)의 pytest
demo-test:
    {{vpy}} -m pytest web/touying-exporter/tests -q

# 두 시퀀스(12번 + 11번) → 한 덱 slides_{ko,ja}.typ + 악장표 movements.json. typst 로 쪽수(1 + 84 = 85) 확인
demo-slides:
    python3 tools/sequence_demo_build.py gen
    mkdir -p build/demo
    typst compile {{fonts}} "{{demo}}/slides_ko.typ" build/demo/slides_ko.pdf
    typst compile {{fonts}} "{{demo}}/slides_ja.typ" build/demo/slides_ja.pdf
    @for l in ko ja; do printf '%s: %s pages\n' $l "$(pdfinfo build/demo/slides_$l.pdf | awk '/^Pages:/{print $2}')"; done

# 11번만 담는 앞 판의 덱(1 + 52 = 53쪽) — 지금 앱은 이것을 쓰지 않는다
demo-slides-11:
    python3 tools/pathetique_demo_build.py gen

# 덱 → 페이지별 SVG + manifest.json (integration 이 자동으로 하는 것과 같은 명령)
demo-export:
    #!/usr/bin/env bash
    set -euo pipefail
    for l in ko ja; do
      {{vpy}} -m touying compile "{{demo}}/slides_$l.typ" --format astro \
        --out-dir "{{web}}/public/decks/$l" --query-label sync-beat --query-label sync-meta --font-paths {{fontdirs}} --silent
      echo "decks/$l: $(ls "{{web}}/public/decks/$l"/page-*.svg | wc -l) pages"
    done

# manifest.json ↔ 두 대본 ↔ 악장표 대조
demo-check:
    python3 tools/sequence_demo_build.py check

demo-dev:
    cd {{web}} && pnpm install --silent && pnpm dev

demo-build:
    cd {{web}} && pnpm install --silent && pnpm build

demo-e2e:
    python3 tools/sequence_demo_e2e.py

demo-clean:
    rm -rf {{web}}/dist {{web}}/.astro {{web}}/public/decks build/demo

# 12번 대본의 .md → .typ (같은 변환기를 두 언어에 쓰므로 생성물이 자동으로 록스텝)
scripts-typ:
    python3 tools/script_md2typ.py "out/bgm/12_동귀어진_폭로방송_시퀀스_대본/script_ko.md" "out/bgm/12_동귀어진_폭로방송_시퀀스_대본/script_ja.md"

# 음원의 구간 경계를 파형에서 잡는다:  just audio-sections f="/path/to.flac"
f := ""
audio-sections:
    python3 tools/audio_sections.py "{{f}}" --map 10

# 인물관계도 도표 생성 → docs/_diagrams/
relations:
    python3 tools/relations_diagram_gen.py

clean:
    rm -rf build

# 원전(Typst) KO/JA → PDF (build/ 아래에, git에는 넣지 않는다)
compile:
    mkdir -p build
    typst compile {{fonts}} docs/kimishinu_merged_ko_v2.11.2.typ build/merged_ko.pdf
    typst compile {{fonts}} docs/kimishinu_merged_ja_v2.11.2.typ build/merged_ja.pdf
    typst compile {{fonts}} docs/reference/kimishinu_history_ko_v2.11.2.typ build/history_ko.pdf
    typst compile {{fonts}} docs/reference/kimishinu_history_ja_v2.11.2.typ build/history_ja.pdf
    @for f in merged_ko merged_ja history_ko history_ja; do printf '%s: %s pages\n' $f "$(pdfinfo build/$f.pdf | awk '/^Pages:/{print $2}')"; done

# 대본·단편소설(.typ) — 각 파일 머리 주석에 컴파일 명령이 있다.
# 결말부 단편소설은 음원 미첨부: typst compile --root . --input with-audio=false ...
scripts-pdf:
    mkdir -p build
    typst compile {{fonts}} "out/script/결말부_연속시퀀스_단편소설/단편소설_ko.typ" --root . --input with-audio=false build/결말부_단편소설_ko.pdf
    typst compile {{fonts}} "out/script/번외편_I_허니문_I_대본/script_ko.typ" build/I_script_ko.pdf
    typst compile {{fonts}} "out/script/번외편_I_허니문_I_대본/script_ja.typ" build/I_script_ja.pdf
    typst compile {{fonts}} "out/script/번외편_II_허니문_II_대본/script_ko.typ" build/II_script_ko.pdf
    typst compile {{fonts}} "out/script/번외편_II_허니문_II_대본/script_ja.typ" build/II_script_ja.pdf
    typst compile {{fonts}} "out/script/번외편_IV_허니문_IV_대본/script_ko.typ" build/IV_script_ko.pdf
    typst compile {{fonts}} "out/script/번외편_IV_허니문_IV_대본/script_ja.typ" build/IV_script_ja.pdf
    typst compile {{fonts}} "out/bgm/11_비창_1악장_시퀀스_대본/script_ko.typ" build/11_script_ko.pdf
    typst compile {{fonts}} "out/bgm/11_비창_1악장_시퀀스_대본/script_ja.typ" build/11_script_ja.pdf
    typst compile {{fonts}} "out/bgm/12_동귀어진_폭로방송_시퀀스_대본/script_ko.typ" build/12_script_ko.pdf
    typst compile {{fonts}} "out/bgm/12_동귀어진_폭로방송_시퀀스_대본/script_ja.typ" build/12_script_ja.pdf
    @echo "단편소설·헌정곡은 각 폴더의 파일 머리 주석대로 컴파일한다(III 대본은 아직 없다)"

# 프리퀄·스핀오프 .md → .typ (tools/script_md2typ.py 생성물) + 컴파일 확인
docs-typ:
    python3 tools/script_md2typ.py docs/kimishinu_prequel_ko_v0.16.md docs/kimishinu_prequel_ja_v0.16.md docs/kimishinu_spinoff_ko_v0.6.md docs/kimishinu_spinoff_ja_v0.6.md
    @mkdir -p build
    @for f in kimishinu_prequel_ko_v0.16 kimishinu_prequel_ja_v0.16 kimishinu_spinoff_ko_v0.6 kimishinu_spinoff_ja_v0.6; do \
      typst compile {{fonts}} "docs/$f.typ" "build/$f.pdf" && printf '%s: %s pages\n' "$f" "$(pdfinfo "build/$f.pdf" | awk '/^Pages:/{print $2}')"; done
