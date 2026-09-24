import os
import re
import yaml

folder_path = "src/content/posts" 

print(f"Mulai konversi kapital murni ing folder: {folder_path}")

for filename in os.listdir(folder_path):
    if filename.endswith(".md"):
        file_path = os.path.join(folder_path, filename)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
        if match:
            frontmatter_raw = match.group(1)
            body = match.group(2)
            
            try:
                data = yaml.safe_load(frontmatter_raw) or {}
                
                # Jupuk categories lawas
                categories = data.get('categories') or data.get('tags') or []
                if not isinstance(categories, list):
                    categories = [categories]
                
                # PROSES UTAMA: Nggawe HTML murni dadi Huruf Gedhe ing saben awal kata liwat Python
                # Tuladha: "dangdut-koplo" dadi "Dangdut Koplo"
                tags_kapital = []
                for cat in categories:
                    if cat:
                        clean_cat = str(cat).replace("-", " ")
                        # Nggawe saben awal kata dadi kapital (Title Case)
                        title_cat = clean_cat.title() 
                        tags_kapital.append(title_cat)
                
                if not tags_kapital:
                    tags_kapital = ["Uncategorized"]
                
                # Cek yen data tags-e wis bener-bener format kapital, skip wae
                if 'author' in data and 'slug' in data and data.get('tags') == tags_kapital:
                    continue
                
                title = data.get('title', filename.replace('.md', ''))
                date_val = data.get('date') or data.get('pubDatetime') or '2026-09-24T00:00:00Z'
                if isinstance(date_val, str) and len(date_val) == 10:
                    date_val = f"{date_val}T00:00:00Z"
                
                slug_val = os.path.splitext(filename).lower().replace(" ", "-")
                slug_clean = re.sub(r'[^a-z0-9\-]', '', slug_val)
                
                new_data = {
                    'author': 'Admin',
                    'pubDatetime': date_val,
                    'title': title,
                    'slug': slug_clean,
                    'featured': False,
                    'draft': False,
                    'tags': tags_kapital, # Mlebu kene wis wujud huruf kapital murni
                    'description': f"Lirik lagu {title}."
                }
                
                new_frontmatter = yaml.dump(new_data, sort_keys=False, allow_unicode=True)
                new_content = f"---\n{new_frontmatter}---\n{body}"
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Sukses ngerubah HTML Kapital: {filename} -> {tags_kapital}")
                
            except Exception as e:
                print(f"Gagal maca frontmatter ing {filename}: {e}")

print("Konversi rampung kabeh!")
