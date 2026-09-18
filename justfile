# 〈비창〉 1악장 시퀀스 데모 — touying 덱 + touying-exporter(fork) + Astro
# 순서: setup → slides → build(또는 dev) → check → e2e
set shell := ["bash", "-euo", "pipefail", "-c"]

fonts := "--font-path /usr/share/fonts/noto-cjk --font-path /usr/share/fonts/nanum"
script_dir := "out/bgm/11_비창_1악장_시퀀스_대본"
web := "web/pathetique-sync"
demo := script_dir + "/demo"
vpy := web + "/.venv/bin/python"
fontdirs := "/usr/share/fonts/noto-cjk /usr/share/fonts/nanum"
# 음원은 저장소에 없다. 자기 사본의 경로를 넘긴다:  just demo-setup audio="/path/to.m4a"
audio := ""

default:
    @just --list --unsorted

# submodule + uv venv(editable) + pnpm install + (선택) 음원 복사
demo-setup:
    git submodule update --init web/touying-exporter
    uv venv {{web}}/.venv --python 3.14
    uv pip install --python {{vpy}} -e "web/touying-exporter[test]"
    cd {{web}} && pnpm install
    @if [ -n "{{audio}}" ]; then mkdir -p {{web}}/public/audio && cp -f "{{audio}}" {{web}}/public/audio/pathetique-mvt1.m4a && echo "음원 복사 완료"; else echo "음원 없음 — 재생 없이 탐색만 된다"; fi

# fork(touying-exporter)의 pytest
demo-test:
    {{vpy}} -m pytest web/touying-exporter/tests -q

# 대본 .typ → touying 덱 생성, typst 로 컴파일해 쪽수(1 + 52 = 53) 확인
demo-slides:
    python3 tools/pathetique_demo_build.py gen
    mkdir -p build/demo
    typst compile {{fonts}} {{demo}}/slides_ko.typ build/demo/slides_ko.pdf
    typst compile {{fonts}} {{demo}}/slides_ja.typ build/demo/slides_ja.pdf
    @for l in ko ja; do printf '%s: %s pages\n' $l "$(pdfinfo build/demo/slides_$l.pdf | awk '/^Pages:/{print $2}')"; done

# 덱 → 페이지별 SVG + manifest.json (integration 이 자동으로 하는 것과 같은 명령)
demo-export:
    #!/usr/bin/env bash
    set -euo pipefail
    for l in ko ja; do
      {{vpy}} -m touying compile "{{demo}}/slides_$l.typ" --format astro \
        --out-dir "{{web}}/public/decks/$l" --query-label sync-beat --query-label sync-meta --font-paths {{fontdirs}} --silent
      echo "decks/$l: $(ls "{{web}}/public/decks/$l"/page-*.svg | wc -l) pages"
    done

demo-check:
    python3 tools/pathetique_demo_build.py check

demo-dev:
    cd {{web}} && pnpm install --silent && pnpm dev

demo-build:
    cd {{web}} && pnpm install --silent && pnpm build

demo-e2e:
    python3 tools/pathetique_demo_e2e.py

demo-clean:
    rm -rf {{web}}/dist {{web}}/.astro {{web}}/public/decks build/demo

# 인물관계도 도표 생성 → docs/_diagrams/
relations:
    python3 tools/relations_diagram_gen.py

clean:
    rm -rf build
