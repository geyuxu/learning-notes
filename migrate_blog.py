import os
import re
import shutil
import urllib.request
import urllib.parse
from pathlib import Path
import hashlib

SOURCE_DIR = Path('old_blog')
TARGET_NOTES_BASE = Path('NOTES/topics')
TARGET_NB_DIR = Path('LABS/notebooks')
ASSETS_DIR = Path('ASSETS')

# Ensure directories exist
ASSETS_DIR.mkdir(exist_ok=True)
TARGET_NB_DIR.mkdir(exist_ok=True)

def download_image(url):
    try:
        # Extract filename
        parsed = urllib.parse.urlparse(url)
        filename = os.path.basename(parsed.path)
        if not filename:
            filename = hashlib.md5(url.encode()).hexdigest() + '.png'
        
        # Handle potential collisions
        target_path = ASSETS_DIR / filename
        if target_path.exists():
            # Check if content is same? Or just rename.
            # Simple rename for now
            name, ext = os.path.splitext(filename)
            counter = 1
            while target_path.exists():
                target_path = ASSETS_DIR / f"{name}_{counter}{ext}"
                counter += 1
        
        print(f"Downloading {url} to {target_path}")
        # Use curl for reliability if urllib fails or just use urllib
        # urllib is fine for simple gets
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(target_path, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
            
        return target_path.name
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None

def process_markdown(content, file_path):
    # 1. Remove YAML frontmatter and extract metadata
    frontmatter_regex = r'^---\s*\n(.*?)\n---\s*\n'
    match = re.search(frontmatter_regex, content, re.DOTALL)
    
    metadata = {}
    if match:
        fm_content = match.group(1)
        # Simple parsing of key: value
        for line in fm_content.split('\n'):
            if ':' in line:
                key, val = line.split(':', 1)
                metadata[key.strip()] = val.strip().strip('"\'')
        
        # Remove frontmatter
        content = content[match.end():]
    
    # 2. Find and replace images
    # Markdown images: ![alt](url)
    # HTML images: <img src="url" ...>
    
    def replace_md_image(match):
        alt = match.group(1)
        url = match.group(2)
        if 'img.geyuxu.com' in url:
            new_filename = download_image(url)
            if new_filename:
                return f'![{alt}](/ASSETS/{new_filename})' # Use absolute path from root for VSCode/GitHub resolution? 
                # The user prompt used `ASSETS/sanity_check_plot.png` in README, which is relative to root.
                # In NOTES/topics/..., relative path would be ../../../ASSETS/...
                # But README says "![...](ASSETS/...)" works because README is at root.
                # For files in subdirs, we need relative paths or absolute from repo root if supported.
                # Standard markdown usually requires relative paths.
                # Let's use relative path from the note file to ASSETS.
                # Note depth: NOTES/topics/category/file.md -> depth 3.
                # So ../../../ASSETS/filename
                # But let's stick to what the user prompt implied or use absolute if the environment supports it.
                # The prompt example: `![Sanity check plot](ASSETS/sanity_check_plot.png)` in README.
                # For `NOTES/topics/numpy/01_numpy_basics.md`, if we want to link `ASSETS/img.png`, it should be `../../../ASSETS/img.png`.
                # I will calculate the relative path.
                return f'![{alt}](../../../ASSETS/{new_filename})'
        return match.group(0)

    content = re.sub(r'!\[(.*?)\]\((.*?)\)', replace_md_image, content)
    
    # HTML images
    def replace_html_image(match):
        tag = match.group(0)
        src_match = re.search(r'src=["\'](.*?)["\']', tag)
        if src_match:
            url = src_match.group(1)
            if 'img.geyuxu.com' in url:
                new_filename = download_image(url)
                if new_filename:
                    return tag.replace(url, f'../../../ASSETS/{new_filename}')
        return tag

    content = re.sub(r'<img\s+[^>]*?>', replace_html_image, content)

    # 3. Add Header
    title = metadata.get('title', file_path.stem.replace('_', ' ').title())
    date = metadata.get('date', metadata.get('pubDate', '2023-01-01'))
    tags = metadata.get('tags', 'blog')
    
    header = f"""# {title}
Last updated: {date}
Tags: {tags}
TL;DR:
- Migrated from old blog.
- Original title: {title}
- See notebook for details.

"""
    return header + content

def create_notebook(category, filename_stem):
    nb_name = f"R_{category}_{filename_stem}.ipynb".replace('-', '_')
    nb_path = TARGET_NB_DIR / nb_name
    
    # Simple JSON for notebook
    import json
    nb_content = {
     "cells": [
      {
       "cell_type": "markdown",
       "metadata": {},
       "source": [
        f"# {filename_stem}\n",
        "\n",
        "**Purpose**: Companion notebook for the migrated blog post.\n",
        "**Outputs**: \n",
        "- Demonstrations related to the topic.\n"
       ]
      },
      {
       "cell_type": "code",
       "execution_count": None,
       "metadata": {},
       "outputs": [],
       "source": [
        "import pandas as pd\n",
        "import numpy as np\n",
        "import matplotlib.pyplot as plt\n",
        "\n",
        "print('Setup complete.')"
       ]
      }
     ],
     "metadata": {
      "kernelspec": {
       "display_name": "Python 3",
       "language": "python",
       "name": "python3"
      },
      "language_info": {
       "codemirror_mode": {
        "name": "ipython",
        "version": 3
       },
       "file_extension": ".py",
       "mimetype": "text/x-python",
       "name": "python",
       "nbconvert_exporter": "python",
       "pygments_lexer": "ipython3",
       "version": "3.8.5"
      }
     },
     "nbformat": 4,
     "nbformat_minor": 4
    }
    
    with open(nb_path, 'w') as f:
        json.dump(nb_content, f, indent=1)
    
    return nb_name

def main():
    processed_files = []
    
    for root, dirs, files in os.walk(SOURCE_DIR):
        for file in files:
            if file.endswith('.md'):
                file_path = Path(root) / file
                # Skip hidden files
                if file.startswith('.'):
                    continue
                
                print(f"Processing {file_path}...")
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    new_content = process_markdown(content, file_path)
                    
                    # Determine target path
                    rel_path = file_path.relative_to(SOURCE_DIR)
                    target_path = TARGET_NOTES_BASE / rel_path
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    with open(target_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    # Create notebook
                    # Use the first directory as category
                    category = rel_path.parts[0] if len(rel_path.parts) > 1 else 'general'
                    nb_name = create_notebook(category, file_path.stem)
                    
                    processed_files.append({
                        'note_path': str(target_path),
                        'nb_path': str(TARGET_NB_DIR / nb_name),
                        'title': file_path.stem
                    })
                    
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

    # Output summary for updating other files
    print("\n--- Summary ---")
    for item in processed_files:
        print(f"Processed: {item['title']}")
        print(f"  Note: {item['note_path']}")
        print(f"  NB: {item['nb_path']}")

if __name__ == '__main__':
    main()
