// @ts-check
import { defineConfig } from "astro/config";
import touyingExporter from "touying-astro";

// 저장소 루트 기준 경로 — 이 앱은 web/pathetique-sync/ 에 있다.
const REPO = "../..";
const DEMO = `${REPO}/out/bgm/11_비창_1악장_시퀀스_대본/demo`;
const FONTS = ["/usr/share/fonts/noto-cjk", "/usr/share/fonts/nanum"];

export default defineConfig({
  output: "static",
  integrations: [
    touyingExporter({
      python: ".venv/bin/python", // fork(web/touying-exporter)가 editable 로 설치된 venv
      fontPaths: FONTS,
      decks: ["ko", "ja"].map((lang) => ({
        input: `${DEMO}/slides_${lang}.typ`,
        outDir: `public/decks/${lang}`,
        labels: ["sync-beat", "sync-meta"],
      })),
    }),
  ],
  // 폰 등 다른 기기에서 열려면 호스트명을 환경변수로 준다:
  //   ASTRO_ALLOWED_HOSTS=my-host.example.com pnpm dev --host
  server: {
    allowedHosts: ["localhost", ...(process.env.ASTRO_ALLOWED_HOSTS ?? "").split(",").filter(Boolean)],
  },
});
