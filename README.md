# Bevan's Blog

A simple static blog generator built with Python and pandoc.

## How it Works

This website is a **static site generator** that converts markdown blog posts into HTML pages.

### Directory Structure

```
blogs/
├── 2024/
│   ├── Running_10km.md
│   └── another_post.md
└── 2023/
    └── old_post.md

html/                    (generated)
├── 2024/
│   ├── Running_10km.html
│   └── another_post.html
└── 2023/
    └── old_post.html

index.html              (generated)
```

### Build Process

1. **Organize**: Place markdown files in `blogs/YEAR/` directories
2. **Run**: Execute `uv run python generate_blog.py`
3. **Deploy**: Serve the generated HTML files

### What the Script Does

```bash
python generate_blog.py
```

1. **Scans** `blogs/` directory for year folders and `.md` files
2. **Converts** each markdown file to HTML using pandoc
3. **Applies** HTML templates with consistent styling and navigation
4. **Extracts** blog post titles and metadata
5. **Generates** `index.html` with posts grouped by year (newest first)

### Templates

- **`blog_template.html`**: Template for individual blog posts
  - Includes "← Back to Blog" navigation
- **`index_template.html`**: Template for the main blog index
  - Lists all posts grouped by year

### Dependencies

- **Python 3.13+** with uv package manager
- **pandoc** for markdown to HTML conversion
- **BeautifulSoup4** for HTML parsing

### Setup

```bash
# 1. Install uv (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.local/bin/env  # Add to PATH

# 2. Install Python dependencies
uv sync

# 3. Install pandoc (macOS)
brew install pandoc
# or Ubuntu
wget https://github.com/jgm/pandoc/releases/download/3.7.0.2/pandoc-3.7.0.2-1-amd64.deb
sudo dpkg -i pandoc-3.7.0.2-1-amd64.deb

# 4. Generate the blog
uv run python generate_blog.py
```

### Features

- ✅ **Simple**: Just markdown files in year folders
- ✅ **Clean**: Minimal HTML/CSS, no JavaScript
- ✅ **Organized**: Automatic chronological grouping
- ✅ **Templates**: Easy to modify styling
- ✅ **Navigation**: Back links between pages

### Deployment

Generated files (`html/` and `index.html`) are ignored by git and built on the server:

1. Push markdown source files to repository
2. Run build script on server: `python generate_blog.py`
3. Copy generated files to nginx web directory:
   ```bash
   sudo cp -r html/ /var/www/html/
   sudo cp index.html /var/www/html/
   ```
4. Nginx serves the static HTML files
