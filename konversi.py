import os
import re

folder_path = "src/content/posts" 

print(f"Mulai konversi meksa kapital murni ing folder: {folder_path}")

for filename in os.listdir(folder_path):
    if filename.endswith(".md"):
        file_path = os.path.join(folder_path, filename)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Goleki bagean frontmatter nganggo Regex murni (luwih aman tinimbang PyYAML)
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
        if match:
            frontmatter_raw = match.group(1)
            body = match.group(2)
            
            # Goleki baris categories utawa tags
            cat_match = re.search(r'categories:\s*\n((?:\s*-\s*.*\n?)*)', frontmatter_raw)
            tag_match = re.search(r'tags:\s*\n((?:\s*-\s*.*\n?)*)', frontmatter_raw)
            
            target_match = cat_match if cat_match else tag_match
            
            if target_match:
                lines = target_match.group(1).strip().split('\n')
                new_tags = []
                for line in lines:
                    if '-' in line:
                        # Jupuk reged-reged tag lawas
                        val = line.split('-', 1)[1].strip().strip('"').strip("'")
                        if val:
                            # Ngerubah dadi kapital awal kata (Title Case) lan ngilangke strip (-)
                            clean_val = val.replace("-", " ").title()
                            new_tags.append(f'  - "{clean_val}"')
                
                # Susun struktur tags anyar
                tags_block = "tags:\n" + "\n".join(new_tags)
                
                # Buang blok categories utawa tags sing lawas saka frontmatter
                fm_clean = frontmatter_raw
                if cat_match:
                    fm_clean = fm_clean.replace(cat_match.group(0), "")
                if tag_match:
                    fm_clean = fm_clean.replace(tag_match.group(0), "")
                
                # Jupuk data title lan date asli
                title_find = re.search(r'^title:\s*(.*)', fm_clean, re.MULTILINE)
                date_find = re.search(r'^(date|pubDatetime):\s*(.*)', fm_clean, re.MULTILINE)
                
                title_val = title_find.group(1).strip().strip('"').strip("'") if title_find else filename.replace('.md', '')
                date_val = date_find.group(2).strip() if date_find else '2026-09-24T00:00:00Z'
                
                if len(date_val) == 10:
                    date_val = f"{date_val}T00:00:00Z"
                
                slug_val = os.path.splitext(filename).lower().replace(" ", "-")
                slug_clean = re.sub(r'[^a-z0-9\-]', '', slug_val)
                
                # Bangun frontmatter anyar sing wis di-meksa Kapital murni
                new_fm = f"""author: Admin
pubDatetime: {date_val}
title: "{title_val}"
slug: "{slug_clean}"
featured: false
draft: false
{tags_block}
description: "Lirik lagu {title_val}." """
                
                new_content = f"---\n{new_fm}\n---\n{body}"
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Sukses Meksa Kapital: {filename}")

print("Selesai! Kabeh tags saiki wis dadi Huruf Gedhe permanen ing berkas .md.")
