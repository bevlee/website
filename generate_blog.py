#!/usr/bin/env python3
"""
Blog generation script - Step 1: Scan blogs/ directory
"""

import os
import sys
import subprocess
from pathlib import Path
from bs4 import BeautifulSoup

def scan_blogs_directory():
    """
    Scan the blogs/ directory and find all year directories and markdown files.
    Returns a dictionary with year -> list of markdown files structure.
    """
    blogs_dir = Path("blogs")
    
    if not blogs_dir.exists():
        print("Error: blogs/ directory not found")
        sys.exit(1)
    
    blog_structure = {}
    
    # Find all year directories
    for year_dir in blogs_dir.iterdir():
        if year_dir.is_dir() and year_dir.name.isdigit():
            year = year_dir.name
            md_files = []
            
            # Find all .md files in this year directory
            for md_file in year_dir.glob("*.md"):
                md_files.append(md_file.name)
            
            if md_files:
                blog_structure[year] = md_files
    
    return blog_structure

def load_template():
    """
    Load HTML template from file
    """
    template_path = Path("blog_template.html")
    if not template_path.exists():
        print("Error: blog_template.html not found")
        sys.exit(1)
    
    return template_path.read_text()

def create_blog_template(content, title, back_link="../index.html"):
    """
    Create HTML using template file
    """
    template = load_template()
    return template.format(
        title=title,
        content=content,
        back_link=back_link
    )

def convert_markdown_to_html(blog_structure):
    """
    Convert markdown files to HTML using pandoc and templates
    """
    for year, md_files in blog_structure.items():
        year_dir = Path(f"html/{year}")
        year_dir.mkdir(parents=True, exist_ok=True)
        
        for md_file in md_files:
            md_path = f"blogs/{year}/{md_file}"
            html_filename = md_file.replace('.md', '.html')
            
            # Use pandoc to convert markdown to HTML body content only
            try:
                result = subprocess.run([
                    'pandoc', md_path, '--to=html'
                ], capture_output=True, text=True, check=True)
                
                content = result.stdout
                
                # Extract title from first h2 tag (simple approach)
                title = "Blog Post"
                if "<h2" in content:
                    start = content.find("<h2")
                    if start != -1:
                        end = content.find("</h2>", start)
                        if end != -1:
                            title_tag = content[start:end+5]
                            # Extract text between tags
                            title_start = title_tag.find(">") + 1
                            title = title_tag[title_start:title_tag.rfind("<")]
                
                # Create full HTML with template
                full_html = create_blog_template(content, title, "../../index.html")
                
                # Write to HTML file
                html_path = year_dir / html_filename
                html_path.write_text(full_html)
                
                print(f"Converted: {md_path} -> {html_path}")
                
            except subprocess.CalledProcessError as e:
                print(f"Error converting {md_path}: {e}")
                sys.exit(1)
            except FileNotFoundError:
                print("Error: pandoc not found. Please install pandoc.")
                sys.exit(1)

def extract_metadata_from_html(blog_structure):
    """
    Extract metadata from generated HTML files
    Returns: list of dicts with filename, title, year
    """
    blog_posts = []
    
    for year, md_files in blog_structure.items():
        for md_file in md_files:
            html_filename = md_file.replace('.md', '.html')
            html_path = Path(f"html/{year}/{html_filename}")
            
            if not html_path.exists():
                print(f"Warning: {html_path} not found, skipping...")
                continue
            
            try:
                # Read and parse HTML
                html_content = html_path.read_text()
                soup = BeautifulSoup(html_content, 'html.parser')
                
                # Extract title from first h2 tag
                h2_tag = soup.find('h2')
                title = h2_tag.get_text() if h2_tag else "Untitled"
                
                blog_posts.append({
                    'filename': html_filename,
                    'title': title,
                    'year': year,
                    'path': f"html/{year}/{html_filename}"
                })
                
                print(f"Extracted metadata: {title} ({year})")
                
            except Exception as e:
                print(f"Error reading {html_path}: {e}")
                continue
    
    return blog_posts

def main():
    """Main function to scan and convert blog posts"""
    print("Scanning blogs/ directory...")
    
    blog_structure = scan_blogs_directory()
    
    if not blog_structure:
        print("No blog posts found!")
        sys.exit(1)
    
    print("\nFound blog structure:")
    for year in sorted(blog_structure.keys(), reverse=True):
        print(f"\n{year}:")
        for md_file in blog_structure[year]:
            print(f"  - {md_file}")
    
    print(f"\nTotal years: {len(blog_structure)}")
    total_posts = sum(len(files) for files in blog_structure.values())
    print(f"Total posts: {total_posts}")
    
    print("\nConverting markdown to HTML...")
    convert_markdown_to_html(blog_structure)
    
    print("\nExtracting metadata from HTML files...")
    blog_posts = extract_metadata_from_html(blog_structure)
    
    print(f"\nExtracted metadata for {len(blog_posts)} posts:")
    for post in blog_posts:
        print(f"  - {post['title']} ({post['year']})")
    
    print("\n✅ Conversion completed successfully!")
    sys.exit(0)

if __name__ == "__main__":
    main()