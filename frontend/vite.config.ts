// vite.config.ts
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import AutoImport from "unplugin-auto-import/vite";
import Components from "unplugin-vue-components/vite";
import { ElementPlusResolver } from "unplugin-vue-components/resolvers";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    AutoImport({
      // 目标文件
      imports: ["vue"],
      resolvers: [ElementPlusResolver()],
      dts: true,
    }),
    Components({
      dirs: ["src/components", "src/views"],
      resolvers: [ElementPlusResolver()],
      dts: true,
    }),
  ],
});
