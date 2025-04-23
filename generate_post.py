#!/usr/bin/env python3
"""
generate_post.py

Usage:
    python generate_post.py example.md output.html
"""

import sys
import re
import yaml

def parse_markdown(path):
    text = open(path, 'r', encoding='utf-8').read()
    # Split YAML front-matter
    fm_pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    m = re.match(fm_pattern, text, flags=re.S)
    if m:
        fm = yaml.safe_load(m.group(1))
        body_md = m.group(2)
    else:
        fm = {}
        body_md = text

    # **Sanitize**: remove any literal stray </p> lines in the markdown
    body_md = re.sub(r'(?m)^\s*</p>\s*$', '', body_md)

    return fm, body_md

def generate_latex_html():
    """Generate a simple HTML structure with LaTeX examples."""
    return """<p>Your article content goes here. Replace this with the actual text for your blog post.</p>
<p>Add additional paragraphs, images, lists, or other HTML elements as required by your content.</p>

<h3>LaTeX Example</h3>
<p>Here's an example of inline LaTeX: $E = mc^2$ and another one: $\\alpha + \\beta = \\gamma$.</p>

<p>And here's a display equation:</p>
$$\\int_{a}^{b} f(x) \\, dx = F(b) - F(a)$$"""

def main(md_path, out_path):
    # Parse the markdown file (we're not using the content, just keeping the function for future use)
    parse_markdown(md_path)
    
    # Generate the LaTeX HTML content
    html_content = generate_latex_html()
    
    # Write the output file
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Generated LaTeX HTML: {out_path}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python generate_post.py <markdown.md> <output.html>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
