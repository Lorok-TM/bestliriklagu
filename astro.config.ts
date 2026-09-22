
import {
  defineConfig,
  envField,
  fontProviders,
  svgoOptimizer,
} from "astro/config";
import tailwindcss from "@tailwindcss/vite";
import mdx from "@astrojs/mdx";
import sitemap from "@astrojs/sitemap";
import { unified } from "@astrojs/markdown-remark";
import remarkToc from "remark-toc";
import remarkCollapse from "remark-collapse";
import rehypeCallouts from "rehype-callouts";
import {
  transformerNotationDiff,
  transformerNotationHighlight,
  transformerNotationWordHighlight,
} from "@shikijs/transformers";
import { transformerFileName } from "./src/utils/transformers/fileName";
import config from "./astro-paper.config";

import { readFileSync, writeFileSync, readdirSync } from "fs";
import { join } from "path";
import { fileURLToPath } from "url";

function htmlPureMinifier(): any {
  return {
    name: "html-pure-minifier",
    hooks: {
      "astro:build:done": async ({ dir }: any) => {
        const distDir = fileURLToPath(dir);
        const getFiles = (dirPath: string): string[] => {
          const entries = readdirSync(dirPath, { withFileTypes: true });
          return entries.flatMap(entry => {
            const res = join(dirPath, entry.name);
            return entry.isDirectory() ? getFiles(res) : res;
          });
        };

        const files = getFiles(distDir).filter(f => f.endsWith(".html"));

        for (const file of files) {
          let html = readFileSync(file, "utf-8");

          // 🔥 Regex murni kanggo ngrapetno post .md & tetep lolos W3C Validator
          html = html
            .replace(/>\s+</g, "><")      
            .replace(/\s{2,}/g, " ")       
            .replace(/\n/g, "")            
            .replace(/<!--[\s\S]*?-->/g, ""); 

          writeFileSync(file, html);
        }
        console.log("🚀 HTML post .md wis rapet pet!");
      },
    },
  };
}

export default defineConfig({
  site: config.site.url,
  compressHTML: false,
  integrations: [
    mdx(),
    sitemap({
      filter: page =>
        config.features?.showArchives !== false || !page.endsWith("/archives/"),
    }),
    htmlPureMinifier(),
  ],
  i18n: {
    locales: ["en"],
    defaultLocale: "en",
    routing: {
      prefixDefaultLocale: false,
    },
  },
  markdown: {
    processor: unified({
      remarkPlugins: [
        remarkToc,
        [remarkCollapse, { test: "Table of contents" }],
      ],
      rehypePlugins: [rehypeCallouts],
    }),
    shikiConfig: {
      themes: { light: "min-light", dark: "night-owl" },
      defaultColor: false,
      wrap: false,
      transformers: [
        transformerFileName({ style: "v2", hideDot: false }),
        transformerNotationHighlight(),
        transformerNotationWordHighlight(),
        transformerNotationDiff({ matchAlgorithm: "v3" }),
      ],
    },
  },
  vite: {
    plugins: [tailwindcss()],
  },
  fonts: [
    {
      name: "Google Sans Code",
      cssVariable: "--font-google-sans-code",
      provider: fontProviders.google(),
      fallbacks: ["monospace"],
      weights: [300, 400, 500, 600, 700],
      styles: ["normal", "italic"],
      formats: ["woff", "ttf"],
    },
  ],
  env: {
    schema: {
      PUBLIC_GOOGLE_SITE_VERIFICATION: envField.string({
        access: "public",
        context: "client",
        optional: true,
      }),
    },
  },
  experimental: {
    svgOptimizer: svgoOptimizer(),
  },
});
