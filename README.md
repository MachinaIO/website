# Machina iO website

```bash
open index.html
```

### How to add a blogpost

```
pip install markdown2 pyyaml
```

1. Write the blogpost on HackMD
2. From HackMD, download the file to markdown inside the posts folder. For example, `posts/example.md`.
3. From root run `python3 generate_post.py posts/example.md posts/output.html` to clean up the HTML file. This will generate a new file `posts/output.html` with the cleaned up HTML.
4. Copy and paste the `blog_template.html` file to `posts/example.html`, choose your date and tile and copy and paste the content of `posts/output.html` inside `<div class="content">` 
5. Add the new post inside the `<div class="article-list">` in `index.html` file, with the correct date and title
