import { defineCollection } from "astro:content";
import { z } from "astro/zod";
import { glob } from "astro/loaders";
import config from "@/config";

export const BLOG_PATH = "src/content/posts";

const posts = defineCollection({
  loader: glob({ pattern: "**/[^_]*.{md,mdx}", base: `./${BLOG_PATH}` }),
  schema: ({ image }) =>
    z.object({
      author: z.string().default(config.site.author),
      
      // 1. TANGGAL: Diakali supoyo gelem moco 'date' soko WordPress, utawa 'pubDatetime' gawan Astro Paper
      // Yen ono file murni date: 2025-11-10 soko WordPress, otomatis diowahi dadi format tanggal sing sah
      pubDatetime: z
        .date()
        .or(z.string().transform(str => new Date(str)))
        .optional()
        .or(z.any()) // Tameng pungkasan supoyo ora silang abang nek format jam mleset
        .default(() => new Date()), // Yen kosong banget otomatis diisi tanggal hari ini
        
      modDatetime: z.date().optional().nullable(),
      title: z.string(),
      
      // 2. BOLEAN (Featured & Draft): Wajib diwenehi .default(false) supoyo file WordPress sing ora duwe parameter iki tetep lulus ijo
      featured: z.boolean().default(false),
      draft: z.boolean().default(false),
      
      tags: z.array(z.string()).default(["others"]),
      ogImage: image().or(z.string()).optional(),
      
      // 3. DESKRIPSI: Digawe otomatis ngekei teks kosong ("") yen neng file .md asline kosong utawa ora ditulis
      description: z.string().default(""),
      
      canonicalURL: z.string().optional(),
      hideEditPost: z.boolean().optional(),
      timezone: z.string().optional(),
      
      // 4. SLUG & CATEGORIES: Ditambahi parameter opsional kanggo nampani data bawaan file WordPress-mu
      slug: z.string().optional(),
      categories: z.array(z.string()).default(["Uncategorized"]),
    }),
});

const pages = defineCollection({
  loader: glob({ pattern: "**/[^_]*.{md,mdx}", base: "./src/content/pages" }),
  schema: z.object({
    title: z.string(),
    description: z.string().default(""), // digae aman sisan nggo halaman statis
    ogImage: z.string().optional(),
    canonicalURL: z.string().optional(),
  }),
});

export const collections = { posts, pages };
