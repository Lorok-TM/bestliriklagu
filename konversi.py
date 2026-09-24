import os
import re
import yaml

folder_path = "src/content/posts" 

print(f"Mulai konversi dinamis ing folder: {folder_path}")

for filename in os.listdir(folder_path):
    if filename.endswith(".md"):
        file_path = os.path.join(folder_path, filename)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Goleki bagean frontmatter
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
        if match:
            frontmatter_raw = match.group(1)
            body = match.group(2)
            
            try:
                # Maca data frontmatter nganggo PyYAML
                data = yaml.safe_load(frontmatter_raw) or {}
                
                # Cek yen file iki WIS format anyar (wis duwe author/slug), skip wae supaya ora error
                if 'author' in data and 'slug' in data and 'pubDatetime' in data:
                    print(f"Dilewati (wis format Astro Paper): {filename}")
                    continue
                
                # Jupuk data lawas
                title = data.get('title', filename.replace('.md', ''))
                
                # Jupuk tanggal (saka 'date' utawa 'pubDatetime')
                date_val = data.get('date') or data.get('pubDatetime') or '2026-09-24T00:00:00Z'
                if isinstance(date_val, str) and len(date_val) == 10:
                    date_val = f"{date_val}T00:00:00Z"
                
                # DINAMIS: Ngowahi categories dadi tags
                # Yen ana 'categories' ing file lawas, jupuk isine. Yen ora ana, nembe golek 'tags'.
                categories = data.get('categories') or data.get('tags') or []
                
                # Pastikake wujude list/array
                if isinstance(categories, list):
                    tags = categories
                else:
                    tags = [categories]
                
                # Reresik spasi utawa tanda kutip ing njero tag
                tags = [str(t).strip().strip('"').strip("'") for t in tags if t]
                if not tags:
                    tags = ["uncategorized"]
                
                # Nggawe slug otomatis saka jeneng berkas
                slug_val = os.path.splitext(filename)[0].lower().replace(" ", "-")
                slug_clean = re.sub(r'[^a-z0-9\-]', '', slug_val)
                
                # Struktur frontmatter anyar kanggo Astro Paper
                new_data = {
                    'author': 'Admin',
                    'pubDatetime': date_val,
                    'title': title,
                    'slug': slug_clean,
                    'featured': False,
                    'draft': False,
                    'tags': tags,
                    'description': f"Lirik lagu {title}."
                }
                
                # Nggawe teks frontmatter anyar
                new_frontmatter = yaml.dump(new_data, sort_keys=False, allow_unicode=True)
                new_content = f"---\n{new_frontmatter}---\n{body}"
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Sukses konversi dinamis: {filename} -> Tags: {tags}")
                
            except Exception as e:
                print(f"Gagal maca frontmatter ing {filename}: {e}")

print("Konversi rampung kabeh!")
