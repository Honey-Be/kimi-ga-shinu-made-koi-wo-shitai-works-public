#!/usr/bin/env python3
"""두 시퀀스 연속 재생 데모의 헤드리스 검증 (playwright + chromium).

`pnpm build` 결과(dist/)를 python 정적 서버(빈 포트)로 띄우고, 시각 몇 개에서
  · 덱이 manifest 가 말하는 페이지를 보여주는지 (img src == page-NNN.svg)
  · 비트 목록의 .active 가 그 비트인지
  · KO/JA 토글 뒤에도 같은 페이지인지
를 확인한다. Chromium 은 AAC(m4a)를 재생하지 못하므로 <audio> 대신
window.sequence.seek(t) 로 전역 시각을 주입한다 (페이지가 노출하는 e2e 용 API).
또한 악장(음원 셋 + 무음 둘)의 경계를 넘을 때 <audio> 의 src 가 바뀌는지도 본다.

시스템 python3 으로 실행한다 (playwright 는 시스템에 설치되어 있다):
    python3 tools/sequence_demo_e2e.py [--build] [--port 4321]
"""

import argparse
import bisect
import json
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WEB = ROOT / "web/pathetique-sync"


def serve_static(root: Path, port: int):
    """dist/ 를 127.0.0.1:port 로 띄우는 정적 서버(데몬 스레드). Range 요청을 받는다."""
    import http.server
    import os
    import threading

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=str(root), **kw)

        def log_message(self, *a):  # 조용히
            pass

        def send_head(self):
            rng = self.headers.get("Range")
            path = self.translate_path(self.path)
            if not rng or not os.path.isfile(path):
                return super().send_head()
            size = os.path.getsize(path)
            m = re.match(r"bytes=(\d*)-(\d*)$", rng)
            if not m:
                return super().send_head()
            start = int(m.group(1)) if m.group(1) else max(size - int(m.group(2)), 0)
            end = int(m.group(2)) if m.group(1) and m.group(2) else size - 1
            end = min(end, size - 1)
            if start > end:
                self.send_error(416)
                return None
            f = open(path, "rb")
            f.seek(start)
            self.send_response(206)
            self.send_header("Content-Type", self.guess_type(path))
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
            self.send_header("Content-Length", str(end - start + 1))
            self.end_headers()
            return _Limited(f, end - start + 1)

    class _Limited:
        def __init__(self, f, n):
            self.f, self.n = f, n

        def read(self, k=-1):
            if self.n <= 0:
                return b""
            k = self.n if k < 0 else min(k, self.n)
            d = self.f.read(k)
            self.n -= len(d)
            return d

        def close(self):
            self.f.close()

    srv = http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def wait_http(url, timeout=60):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            with urllib.request.urlopen(url, timeout=2) as r:
                if r.status < 500:
                    return
        except Exception:
            time.sleep(0.5)
    raise SystemExit(f"preview server did not come up at {url}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", action="store_true", help="먼저 pnpm build 를 돌린다")
    ap.add_argument("--port", type=int, default=0, help="0 = 빈 포트를 고른다 (dev 서버가 4321 을 쓰고 있어도 충돌하지 않게)")
    ap.add_argument("--shot", default=str(ROOT / "build/demo/e2e.png"), help="스크린샷 경로")
    args = ap.parse_args()

    if args.build or not (WEB / "dist/index.html").exists():
        subprocess.run(["pnpm", "build"], cwd=WEB, check=True)
    if not args.port:
        import socket
        with socket.socket() as s:
            s.bind(("127.0.0.1", 0))
            args.port = s.getsockname()[1]

    man = json.loads((WEB / "public/decks/ko/manifest.json").read_text(encoding="utf8"))
    beats = [x for x in man["labels"]["sync-beat"] if not x.get("sub")]
    MOV = json.loads((ROOT / "out/bgm/_combined/movements.json").read_text(encoding="utf8"))
    ts = [b["t_sec"] for b in beats]

    def expect_page(t):
        i = bisect.bisect_right(ts, t) - 1
        return man["first_page"] if i < 0 else beats[i]["page"]

    def expect_section(t, bs):
        i = bisect.bisect_right([b["t_sec"] for b in bs], t) - 1
        return bs[max(i, 0)]["section"]

    # 다섯 악장을 고루 — 드보르자크 · 무음① · 브람스 · 무음② · 차이코프스키
    probes = [0.0, beats[0]["t_sec"], 100.0]
    for m in MOV["movements"]:
        probes += [m["t0"] + 0.5, m["t0"] + m["dur"] / 2]
    probes.append(MOV["total"] - 2.0)
    probes = sorted(set(round(t, 1) for t in probes))

    url = f"http://127.0.0.1:{args.port}/"
    # dist/ 는 정적 사이트다. `astro preview` 는 Astro 7 에서 단일 인스턴스(이미 떠 있으면 두 번째를 거부)라
    # 제안자가 폰 확인용으로 띄워 둔 preview 와 충돌하므로, e2e 는 자체 정적 서버(Range 지원 — <audio> 가
    # 실제 서버와 같은 조건을 보도록)로 dist 를 따로 띄운다.
    server = serve_static(WEB / "dist", args.port)
    failures = []
    try:
        wait_http(url)
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1400, "height": 900})
            errors = []
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
            page.goto(url)
            page.wait_for_function(
                "window.pathetique && document.getElementById('deck-ko').touying && document.getElementById('deck-ja').touying",
                timeout=30000,
            )
            for t in probes:
                exp = expect_page(t)
                page.evaluate(f"sequence.seek({t})")
                st = page.evaluate("sequence.state()")
                src = page.get_attribute("#deck-ko img", "src") or ""
                active = page.evaluate(
                    "[...document.querySelectorAll('#beats li.active')].map(li => Number(li.dataset.page))"
                )
                ok = st["page"] == exp and src.endswith(f"page-{exp:03d}.svg") and (
                    active == [exp] if exp != man["first_page"] else active == []
                )
                print(f"t={t:7.1f}s  expect page {exp:2d}  state {st['page']:2d}  img {src.rsplit('/', 1)[-1]:12s}  active {active}  {'OK' if ok else 'FAIL'}")
                if not ok:
                    failures.append(t)
            # --- 악장: 다섯 악장의 한가운데로 가면 그 악장이 잡히고, 음원 악장은 <audio> 의 src 가 바뀐다
            for mi, m in enumerate(MOV["movements"]):
                t = m["t0"] + m["dur"] / 2
                page.evaluate(f"sequence.seek({t})")
                st = page.evaluate("sequence.state()")
                src = page.evaluate("document.getElementById('audio').getAttribute('src') || ''")
                want_src = MOV["tracks"][m["track"]]["src"] if m["kind"] == "audio" else None
                ok = (st["movement"]["kind"] == m["kind"] and st["movement"]["track"] == m["track"]
                      and abs(st["movement"]["t0"] - m["t0"]) < 0.01
                      and (src == want_src if want_src else True))
                name = m["track"] or "무음(가안)"
                print(f"movement {mi} {name:<12} t={t:7.1f}  kind {st['movement']['kind']:<7} src {src.rsplit('/', 1)[-1]:<28} {'OK' if ok else 'FAIL'}")
                if not ok:
                    failures.append(f"mov{mi}")
            # 무음 악장에서는 <audio> 가 멈춰 있어야 한다
            sil = next(m for m in MOV["movements"] if m["kind"] != "audio")
            page.evaluate(f"sequence.seek({sil['t0'] + 1})")
            page.evaluate("sequence.play()")
            page.wait_for_timeout(500)
            st = page.evaluate("sequence.state()")
            paused = page.evaluate("document.getElementById('audio').paused")
            moved = st["t"] > sil["t0"] + 1.2
            page.evaluate("sequence.pause()")
            ok = paused and moved and st["playing"]
            print(f"silent clock     t={st['t']:7.1f}  audio paused {paused}  clock moved {moved}  {'OK' if ok else 'FAIL'}")
            if not ok:
                failures.append("silent-clock")
            # 주입한 시각이 <audio> 의 timeupdate 에 덮이지 않는가 (악장 첫머리로 튕기지 않는다)
            for t in (MOV["movements"][2]["t0"] + 200, MOV["movements"][4]["t0"] + 600):
                page.evaluate(f"sequence.seek({t})")
                page.wait_for_timeout(700)
                got = page.evaluate("sequence.state().t")
                ok = abs(got - t) < 1.5
                print(f"seek holds  t={t:7.1f} → {got:7.1f}  {'OK' if ok else 'FAIL'}")
                if not ok:
                    failures.append(f"hold{t:.0f}")

            # 전역 스크러버의 최대값 = 총 길이
            mx = page.evaluate("Number(document.getElementById('scrub').max)")
            ok = abs(mx - MOV["total"]) < 0.01
            print(f"scrub max {mx} vs total {MOV['total']}  {'OK' if ok else 'FAIL'}")
            if not ok:
                failures.append("scrub")

            # KO/JA 토글 — 같은 페이지, JA 덱의 img 도 같은 번호
            page.evaluate("sequence.setLang('ja')")
            st = page.evaluate("sequence.state()")
            src_ja = page.get_attribute("#deck-ja img", "src") or ""
            hidden_ko = page.evaluate("document.getElementById('deck-ko').classList.contains('is-hidden')")
            ok = st["lang"] == "ja" and src_ja.endswith(f"page-{st['page']:03d}.svg") and hidden_ko
            print(f"lang→ja  page {st['page']}  ja img {src_ja.rsplit('/', 1)[-1]}  ko hidden {hidden_ko}  {'OK' if ok else 'FAIL'}")
            if not ok:
                failures.append("lang")
            Path(args.shot).parent.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=args.shot)

            # --- 모바일: 세로 폰 (390×844, 터치) — 전문 펼침 · 버튼 이동 · 크게 보기(회전) · 가로 넘침 없음
            def no_overflow(pg):
                return pg.evaluate("document.documentElement.scrollWidth <= window.innerWidth && document.body.scrollHeight <= window.innerHeight + 1")

            mob = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
            mp = mob.new_page()
            mp.on("pageerror", lambda e: errors.append("mobile: " + str(e)))
            mp.on("console", lambda m: errors.append("mobile: " + m.text) if m.type == "error" else None)
            mp.goto(url)
            mp.wait_for_function("window.pathetique && document.getElementById('deck-ko').touying && document.getElementById('deck-ja').touying", timeout=30000)
            mp.evaluate("sequence.seek(300)")
            p0 = mp.evaluate("sequence.state().page")
            full = mp.evaluate("(document.querySelector('#beats li.active .x') || {}).textContent || ''")
            full_visible = mp.evaluate("(() => { const x = document.querySelector('#beats li.active .x'); return !!x && getComputedStyle(x).display !== 'none'; })()")
            mp.click("#next-beat")
            st1 = mp.evaluate("sequence.state()")
            p1 = st1["page"]
            mp.click("#prev-sec")  # ‹‹ 구간 = 앞 구간의 첫 비트(키보드 [ 와 같다)
            p2 = mp.evaluate("sequence.state().page")
            # ‹‹ 구간 = 앞 구간(= (seq, section) 묶음)의 첫 비트
            keys, firsts = [], {}
            for b in beats:
                k = (b["seq"], b["section"])
                if k not in firsts:
                    firsts[k] = b["page"]
                    keys.append(k)
            cur_k = (st1["beat"]["seq"], st1["beat"]["section"])
            sec_start = firsts[keys[max(keys.index(cur_k) - 1, 0)]]
            deck_before = mp.evaluate("document.getElementById('deck-ko').getBoundingClientRect().toJSON()")
            mp.click("#zoom")
            mp.wait_for_function("document.getElementById('stage').classList.contains('zoomed')")
            zoomed = mp.evaluate("sequence.state().zoomed")
            deck_after = mp.evaluate("document.getElementById('deck-ko').getBoundingClientRect().toJSON()")
            vw, vh = mp.evaluate("[window.innerWidth, window.innerHeight]")
            fits = -1 <= deck_after["left"] and deck_after["right"] <= vw + 1 and -1 <= deck_after["top"] and deck_after["bottom"] <= vh + 1
            grew = deck_after["width"] * deck_after["height"] > deck_before["width"] * deck_before["height"] * 1.5
            rotated = deck_after["height"] > deck_after["width"]  # 세로 화면: 90° 회전이라 세로가 길다
            play_visible = mp.evaluate("(() => { const b = document.getElementById('play'), r = b.getBoundingClientRect(); return getComputedStyle(b).display !== 'none' && r.width > 0 && r.bottom <= innerHeight + 1; })()")
            mp.screenshot(path=str(Path(args.shot).with_name("e2e-mobile-zoom.png")))
            mp.click("#unzoom")
            mp.wait_for_function("!document.getElementById('stage').classList.contains('zoomed')")
            unz = not mp.evaluate("sequence.state().zoomed")
            ovf = no_overflow(mp)
            ok = (len(full) > 44 and full_visible and p1 == p0 + 1 and p2 == sec_start
                  and zoomed and fits and grew and rotated and play_visible and unz and ovf)
            print(f"mobile portrait  text {len(full)} chars visible {full_visible}  next {p0}→{p1}  prev-sec →{p2} (start {sec_start})  "
                  f"zoom fits {fits} grew {grew} rotated {rotated} play-btn {play_visible} unzoom {unz}  no-overflow {ovf}  {'OK' if ok else 'FAIL'}")
            if not ok:
                failures.append("mobile-portrait")
            mp.screenshot(path=str(Path(args.shot).with_name("e2e-mobile.png")))

            # --- 모바일: 가로 폰 (844×390) — 덱과 목록이 한 화면에, 넘침 없음
            mp.set_viewport_size({"width": 844, "height": 390})
            mp.evaluate("sequence.seek(577.8)")
            deck = mp.evaluate("document.getElementById('deck-ko').getBoundingClientRect().toJSON()")
            lst = mp.evaluate("document.getElementById('beats').parentElement.getBoundingClientRect().toJSON()")
            aud = mp.evaluate("document.getElementById('audio').getBoundingClientRect().toJSON()")
            vw, vh = mp.evaluate("[window.innerWidth, window.innerHeight]")
            ok = (deck["bottom"] <= vh + 1 and deck["width"] > 200 and lst["width"] > 100 and lst["left"] > deck["right"] - 1
                  and aud["bottom"] <= vh + 1 and aud["top"] >= deck["bottom"] - 1 and no_overflow(mp))
            print(f"mobile landscape deck {deck['width']:.0f}×{deck['height']:.0f} list x={lst['left']:.0f} w={lst['width']:.0f} audio y={aud['top']:.0f}–{aud['bottom']:.0f} of {vw}×{vh}  {'OK' if ok else 'FAIL'}")
            if not ok:
                failures.append("mobile-landscape")
            mp.screenshot(path=str(Path(args.shot).with_name("e2e-mobile-landscape.png")))
            mob.close()
            browser.close()
            if errors:
                print("browser errors:", *errors, sep="\n  ")
                failures.append("console")
    finally:
        server.shutdown()

    print("e2e:", "OK" if not failures else f"FAILED {failures}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
