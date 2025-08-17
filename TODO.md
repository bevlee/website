# Blog Generation System TODO

## Python Script Requirements

### Directory Structure

```
blogs/
├── 2024/
│   ├── Running_10km.md
│   └── another_post.md
└── 2023/
    └── old_post.md

html/
├── 2024/
│   ├── Running_10km.html
│   └── another_post.html
└── 2023/
    └── old_post.html
```

### Script Functionality (`generate_blog.py`)

1. **Scan blogs/ directory**

   - Find all year directories (2024, 2023, etc.)
   - Find all `.md` files in each year directory

2. **Convert markdown to HTML**

   - Create corresponding directory structure in `html/`
   - Use pandoc to convert each `.md` file to `.html`
   - Command: `pandoc blogs/YEAR/file.md -o html/YEAR/file.html`

3. **Extract metadata**

   - Parse each generated HTML file
   - Extract title from `<h2>` tag
   - Store: filename, title, year

4. **Generate index.html**
   - Group posts by year only
   - Sort years descending (newest first)
   - Create simple HTML structure:

     ```html
     <h1>Bevan's Blog</h1>

     <h2>2024</h2>
     <ul>
       <li><a href="html/2024/running_10km.html">Running 10km</a></li>
       <li><a href="html/2024/another_post.html">Another Post</a></li>
     </ul>

     <h2>2023</h2>
     <ul>
       <li><a href="html/2023/old_post.html">Old Post</a></li>
     </ul>
     ```

### Usage

```bash
python generate_blog.py
```

### Dependencies

- Python 3.x
- pandoc (for markdown conversion)
- BeautifulSoup4 (for HTML parsing): `pip install beautifulsoup4`

### Current Manual Process

1. Move existing blog files to year structure in `blogs/`
2. Move `html/running_10km.html` to `html/2024/running_10km.html`
3. Run the script to generate the new index.html

## Future Enhancements

- [ ] Add RSS feed generation
- [ ] Include publish dates in HTML output
- [ ] Add simple CSS themes
- [ ] Watch mode for automatic regeneration
- [ ] Syntax highlighting for code blocks
- [ ] SEO meta tags generation

---

## 11ty Alternative Setup

### Directory Structure

```
blogs/
├── 2024/
│   ├── Running_10km.md
│   └── another_post.md
└── 2023/
    └── old_post.md

_site/           (11ty output directory)
├── 2024/
│   ├── Running_10km/
│   └── another_post/
└── 2023/
    └── old_post/
```

### Setup Steps

1. **Install 11ty**

   ```bash
   npm init -y
   npm install @11ty/eleventy
   ```

2. **Create .eleventy.js config**

   ```js
   module.exports = function (eleventyConfig) {
     return {
       dir: {
         input: "blogs",
         output: "_site",
       },
     };
   };
   ```

3. **Add frontmatter to markdown files**

   ```markdown
   ---
   title: Running 10km
   year: 2024
   ---

   ## Running 10km

   Content here...
   ```

4. **Create index template** (`blogs/index.njk`)
   ```html
   ---
   layout: false
   permalink: /index.html
   ---

   <!DOCTYPE html>
   <html>
     <head>
       <title>Bevan's Blog</title>
     </head>
     <body>
       <h1>Bevan's Blog</h1>

       {%- for year, posts in collections.all | groupby("data.year") | reverse
       %}
       <h2>{{ year }}</h2>
       <ul>
         {%- for post in posts | reverse %}
         <li><a href="{{ post.url }}">{{ post.data.title }}</a></li>
         {%- endfor %}
       </ul>
       {%- endfor %}
     </body>
   </html>
   ```

### Usage

```bash
# Development with live reload
npx eleventy --serve

# Build for production
npx eleventy
```

### Benefits over Python script

- ✅ Built-in markdown processing
- ✅ Live reload during development
- ✅ Automatic URL generation
- ✅ Template inheritance
- ✅ Collections and filtering built-in
- ✅ Plugin ecosystem

### Trade-offs

- ❌ Requires Node.js ecosystem
- ❌ Learning curve for templates
- ❌ More complex than simple Python script
