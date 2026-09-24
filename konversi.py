import os
import re
import yaml

# Ganti folder_path yen berkas .md sampeyan ana ing folder khusus, misale 'src/content/blog'
folder_path = "src/content/blog" 

# Yen berkas .md ana ing folder utama/root, ganti dadi: folder_path = "."

print(f"Mulai konversi ing folder: {folder_path}")

for filename in os.listdir(folder_path):
    if filename.endswith(".md"):
        file_path = os.path.join(folder_path, filename)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Goleki bagean frontmatter (ing antarane --- lan ---)
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
        if match:
            frontmatter_raw = match.group(1)
            body = match.group(2)
            
            try:
                # Maca data frontmatter lawas nganggo PyYAML
                data = yaml.safe_load(frontmatter_raw) or {}
                
                # Jupuk data lawas utawa setel nilai standar
                title = data.get('title', filename.replace('.md', ''))
                date_val = data.get('date', '2026-09-24T00:00:00Z')
                
                # Format tanggal supaya aman kanggo Astro Paper
                if isinstance(date_val, str) and len(date_val) == 10:
                    date_val = f"{date_val}T00:00:00Z"
                
                # Ngowahi categories dadi tags
                categories = data.get('categories', [])
                tags = categories if isinstance(categories, list) else [categories]
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
                    'description': f"Postingan ngenani {title}."
                }
                
                # Nggawe teks frontmatter anyar
                new_frontmatter = yaml.dump(new_data, sort_keys=False, allow_unicode=True)
                new_content = f"---\n{new_frontmatter}---\n{body}"
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Sukses konversi: {filename}")
                
            except Exception as e:
                print(f"Gagal maca frontmatter ing {filename}: {e}")

print("Konversi rampung kabeh!")
