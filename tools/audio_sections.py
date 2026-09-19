#!/usr/bin/env python3
"""음원의 구간 경계를 파형에서 잡는다 — 시퀀스 대본의 큐 표를 만들기 위한 도구.

〈비창〉 1악장 대본(out/bgm/11_…)이 쓴 방법을 그대로 도구로 옮긴 것이다:
0.05초 해상도의 RMS 음량 곡선 + 온셋 밀도를 보고, **총휴지**(아주 낮은 음량이
일정 시간 이어지는 자리) 뒤에 오는 첫 소리를 구간 경계로 삼는다.

    python3 tools/audio_sections.py "<파일>"                # 요약 + 총휴지 + 정점
    python3 tools/audio_sections.py "<파일>" --map 5        # 5초 간격 음량 지도
    python3 tools/audio_sections.py "<파일>" --json out.json

ffmpeg 로 디코드하므로 m4a/mp3/flac/wav 어느 쪽이든 된다. numpy 가 필요하다.
음원 자체는 저장소에 넣지 않는다(CLAUDE.md · .gitignore) — 이 도구는 읽기만 한다.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys

import numpy as np

# 기본은 음원의 원래 표본화 주파수를 그대로 쓴다(--sr 로 바꿀 수 있다).
# AAC·MP3 는 32비트 float(fltp)으로 디코드되므로 f32le 로 받으면 정밀도 손실이 없다.
# 리샘플하면 온셋 검출에서 위쪽 대역이 날아가므로, 기본값은 리샘플하지 않는 것이다.
SR = 44100
HOP = 0.05          # 초 — 〈비창〉 대본과 같은 해상도
SILENCE_DB = -60.0  # 총휴지 판정 기준
MIN_SILENCE = 0.30  # 초 — 이보다 짧으면 쉼으로 세지 않는다


def probe_rate(path: str) -> int:
    cmd = ["ffprobe", "-v", "error", "-select_streams", "a:0",
           "-show_entries", "stream=sample_rate", "-of", "csv=p=0", path]
    p = subprocess.run(cmd, capture_output=True)
    try:
        return int(p.stdout.decode().strip().splitlines()[0])
    except Exception:
        return SR


def decode(path: str, sr: int) -> np.ndarray:
    """ffmpeg 로 모노 float32 PCM 을 받는다(원래 레이트 그대로가 기본)."""
    cmd = ["ffmpeg", "-v", "error", "-i", path,
           "-f", "f32le", "-ac", "1", "-ar", str(sr), "-"]
    p = subprocess.run(cmd, capture_output=True)
    if p.returncode != 0:
        sys.stderr.write(p.stderr.decode("utf8", "replace"))
        raise SystemExit("ffmpeg 디코드 실패: " + path)
    return np.frombuffer(p.stdout, dtype=np.float32)


def rms_db(x: np.ndarray, hop: float = HOP) -> tuple[np.ndarray, np.ndarray]:
    n = max(1, int(SR * hop))
    frames = len(x) // n
    if frames == 0:
        raise SystemExit("음원이 너무 짧다")
    blocks = x[: frames * n].reshape(frames, n)
    rms = np.sqrt(np.mean(blocks.astype(np.float64) ** 2, axis=1))
    db = 20.0 * np.log10(np.maximum(rms, 1e-10))
    t = np.arange(frames) * hop
    return t, db


def spectral_flux(x: np.ndarray, hop: float = HOP) -> tuple[np.ndarray, np.ndarray]:
    """온셋 밀도용 — 프레임 사이 스펙트럼의 양(+)의 변화량 합."""
    n = max(1, int(SR * hop))
    # 창은 최소한 한 홉을 덮어야 한다 — 그러지 않으면 홉 사이가 비어 온셋을 놓친다.
    win = 1 << max(10, int(np.ceil(np.log2(n))))
    frames = len(x) // n
    win_fn = np.hanning(win)
    mags = []
    for i in range(frames):
        s = i * n
        seg = x[s: s + win]
        if len(seg) < win:
            seg = np.pad(seg, (0, win - len(seg)))
        mags.append(np.abs(np.fft.rfft(seg * win_fn)))
    mags = np.asarray(mags)
    if len(mags) < 2:
        return np.zeros(0), np.zeros(0)
    diff = np.diff(mags, axis=0)
    flux = np.sum(np.maximum(diff, 0.0), axis=1)
    return np.arange(1, frames) * hop, flux


def find_silences(t: np.ndarray, db: np.ndarray,
                  thr: float = SILENCE_DB, minlen: float = MIN_SILENCE) -> list[tuple[float, float]]:
    quiet = db < thr
    out: list[tuple[float, float]] = []
    i = 0
    while i < len(quiet):
        if not quiet[i]:
            i += 1
            continue
        j = i
        while j < len(quiet) and quiet[j]:
            j += 1
        start, end = t[i], t[j - 1] + HOP
        if end - start >= minlen:
            out.append((float(start), float(end)))
        i = j
    return out


def mmss(sec: float) -> str:
    # 0.1초로 먼저 반올림한 뒤에 분을 뗀다 — 그러지 않으면 59.95초가 "1:60.0"이 된다.
    tenths = int(round(sec * 10))
    m, rem = divmod(tenths, 600)
    return f"{m}:{rem / 10:04.1f}"


def peaks(t: np.ndarray, db: np.ndarray, window: float = 4.0, top: int = 12) -> list[tuple[float, float]]:
    """국소 최대 — 서로 window 초 이상 떨어진 것만."""
    order = np.argsort(db)[::-1]
    picked: list[tuple[float, float]] = []
    for idx in order:
        ti = float(t[idx])
        if all(abs(ti - p) >= window for p, _ in picked):
            picked.append((ti, float(db[idx])))
        if len(picked) >= top:
            break
    return sorted(picked)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path")
    ap.add_argument("--sr", type=int, default=0,
                    help="표본화 주파수. 기본은 음원의 원래 값(리샘플하지 않는다)")
    ap.add_argument("--map", type=float, default=0.0,
                    help="이 간격(초)으로 음량 지도를 찍는다")
    ap.add_argument("--silence-db", type=float, default=SILENCE_DB)
    ap.add_argument("--min-silence", type=float, default=MIN_SILENCE)
    ap.add_argument("--json", help="결과를 이 경로에 JSON 으로 쓴다")
    args = ap.parse_args()

    global SR
    SR = args.sr if args.sr else probe_rate(args.path)

    x = decode(args.path, SR)
    dur = len(x) / SR
    t, db = rms_db(x)
    ft, flux = spectral_flux(x)

    sil = find_silences(t, db, args.silence_db, args.min_silence)
    pk = peaks(t, db)

    print(f"길이        {mmss(dur)}  ({dur:.3f}초)")
    print(f"표본화      {SR} Hz · 모노 float32 (디코드 정밀도 그대로)")
    print(f"해상도      {HOP}초 · 프레임 {len(db)}개")
    print(f"음량        최대 {db.max():.1f} dB · 중앙값 {np.median(db):.1f} dB · 최소 {db.min():.1f} dB")
    print()

    print(f"총휴지 ({args.silence_db:.0f} dB 미만이 {args.min_silence}초 이상)")
    if not sil:
        print("  없음 — 이 음원에는 완전한 쉼이 없다. 경계는 음량 골짜기로 잡아야 한다.")
    for a, b in sil:
        print(f"  {mmss(a)} – {mmss(b)}   ({b - a:.2f}초)   그 다음 첫 소리 {mmss(b)}")
    print()

    print("음량 정점 (서로 4초 이상 떨어진 국소 최대)")
    for ti, d in pk:
        print(f"  {mmss(ti)}   {d:6.1f} dB")
    print()

    if len(flux):
        # 온셋 밀도 — 1초 단위로 flux 합을 낸다
        sec = (ft // 1.0).astype(int)
        dens = np.bincount(sec, weights=flux)
        hi = np.argsort(dens)[::-1][:10]
        print("온셋 밀도가 높은 1초 구간 (음이 가장 많이 바뀌는 자리)")
        for s in sorted(hi):
            print(f"  {mmss(float(s))}   {dens[s]:.0f}")
        print()

    if args.map:
        print(f"음량 지도 ({args.map:.0f}초 간격, 한 칸 3 dB)")
        step = max(1, int(args.map / HOP))
        lo = max(db.min(), -75.0)
        for i in range(0, len(db), step):
            seg = db[i: i + step]
            d = float(seg.max())
            bars = int(max(0, (d - lo) / 3.0))
            print(f"  {mmss(float(t[i])):>7}  {d:6.1f}  {'█' * bars}")
        print()

    if args.json:
        payload = {
            "path": args.path,
            "duration_sec": round(dur, 3),
            "hop_sec": HOP,
            "silence_db": args.silence_db,
            "silences": [{"start": round(a, 2), "end": round(b, 2), "len": round(b - a, 2)} for a, b in sil],
            "peaks": [{"t": round(ti, 2), "db": round(d, 1)} for ti, d in pk],
        }
        with open(args.json, "w", encoding="utf8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=1)
        print(f"JSON → {args.json}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
