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

def load_blogpost_template():
    """
    Load blogpost HTML template from file
    """
    template_path = Path("blog_template.html")
    if not template_path.exists():
        print("Error: blog_template.html not found")
        sys.exit(1)
    
    return template_path.read_text()

def extract_title_from_html(html_content):
    """
    Extract title from HTML content using BeautifulSoup
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    h2_tag = soup.find('h2')
    return h2_tag.get_text().strip() if h2_tag else "Untitled"

def create_blog_template(content, title, back_link="../index.html"):
    """
    Create HTML using blogpost template file
    """
    template = load_blogpost_template()
    return template.format(
        title=title,
        content=content,
        back_link=back_link
    )

def process_single_blog_file(year, md_file, year_dir):
    """
    Process a single blog file: convert markdown to HTML and extract metadata
    Returns: dict with blog post data or None if error
    """
    md_path = f"blogs/{year}/{md_file}"
    html_filename = md_file.replace('.md', '.html')
    
    try:
        # Convert markdown to HTML using pandoc
        result = subprocess.run([
            'pandoc', md_path, '--to=html'
        ], capture_output=True, text=True, check=True)
        
        content = result.stdout
        
        # Extract title using BeautifulSoup
        title = extract_title_from_html(content)
        
        # Create full HTML with template
        full_html = create_blog_template(content, title, "../../index.html")
        
        # Write to HTML file
        html_path = year_dir / html_filename
        html_path.write_text(full_html)
        
        print(f"Processed: {md_path} -> {html_path}")
        
        # Return blog post metadata
        return {
            'filename': html_filename,
            'title': title,
            'year': year,
            'path': f"html/{year}/{html_filename}"
        }
        
    except subprocess.CalledProcessError as e:
        print(f"Error converting {md_path}: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: pandoc not found. Please install pandoc.")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing {md_path}: {e}")
        return None

def process_blog_files(blog_structure):
    """
    Process all blog files in one pass: convert and extract metadata
    Returns: list of blog post data
    """
    blog_posts = []
    
    for year, md_files in blog_structure.items():
        year_dir = Path(f"html/{year}")
        year_dir.mkdir(parents=True, exist_ok=True)
        
        for md_file in md_files:
            post_data = process_single_blog_file(year, md_file, year_dir)
            if post_data:
                blog_posts.append(post_data)
    
    return blog_posts

def load_index_template():
    """
    Load index HTML template from file
    """
    template_path = Path("index_template.html")
    if not template_path.exists():
        print("Error: index_template.html not found")
        sys.exit(1)
    
    return template_path.read_text()

def generate_index_html(blog_posts):
    """
    Generate index.html file with posts grouped by year
    """
    # Group posts by year
    posts_by_year = {}
    for post in blog_posts:
        year = post['year']
        if year not in posts_by_year:
            posts_by_year[year] = []
        posts_by_year[year].append(post)
    
    # Build content section
    content = ""
    
    # Sort years descending (newest first)
    for year in sorted(posts_by_year.keys(), reverse=True):
        content += f'    <h2>{year}</h2>\n'
        content += '    <ul>\n'
        
        # Sort posts within year (can add date sorting later)
        for post in posts_by_year[year]:
            content += f'        <li><a href="{post["path"]}">{post["title"]}</a></li>\n'
        
        content += '    </ul>\n\n'
    
    # Load template and fill in content
    template = load_index_template()
    html_content = template.format(content=content)
    
    # Write to index.html
    index_path = Path("index.html")
    index_path.write_text(html_content)
    
    print(f"Generated index.html with {len(blog_posts)} posts")

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
    
    print("\nProcessing blog files...")
    blog_posts = process_blog_files(blog_structure)
    
    print(f"\nProcessed {len(blog_posts)} posts:")
    for post in blog_posts:
        print(f"  - {post['title']} ({post['year']})")
    
    print("\nGenerating index.html...")
    generate_index_html(blog_posts)
    
    print("\n✅ Blog generation completed successfully!")
    sys.exit(0)

if __name__ == "__main__":
    main()