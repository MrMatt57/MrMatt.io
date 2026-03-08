"""Rename gallery page bundles from timestamp-based names to descriptive slugs."""
import os

GALLERY = "C:/dev/MrMatt.io/content/photography"

renames = []
for batch in ['_slugs_batch1.txt', '_slugs_batch2.txt', '_slugs_batch3.txt']:
    path = os.path.join(GALLERY, batch)
    if not os.path.exists(path):
        continue
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 3:
                continue
            old_dir, slug, date_info = parts
            date = old_dir[:10] if date_info == 'SAME' else date_info
            new_dir = f'{date}-{slug}'
            renames.append((old_dir, new_dir, date))

# Deduplicate
seen = {}
final_renames = []
for old_dir, new_dir, date in renames:
    if new_dir in seen:
        new_dir = f'{new_dir}-2'
        print(f'  DEDUP: -> {new_dir}')
    seen[new_dir] = old_dir
    final_renames.append((old_dir, new_dir))

renamed = 0
for old_dir, new_dir in final_renames:
    if old_dir == new_dir:
        continue
    old_path = os.path.join(GALLERY, old_dir)
    new_path = os.path.join(GALLERY, new_dir)
    if not os.path.exists(old_path):
        print(f'  MISSING: {old_dir}')
        continue
    if os.path.exists(new_path):
        print(f'  EXISTS: {new_dir}')
        continue
    os.rename(old_path, new_path)
    renamed += 1
    print(f'  {old_dir} -> {new_dir}')

print(f'\nRenamed {renamed} directories')
