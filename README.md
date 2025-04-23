# Machina iO website

```bash
open index.html
```

### How to add a blogpost

```
pip install markdown2 pyyaml
```

1. Write the blogpost in markdown format and add it inside the posts folder. For example, `posts/example.md`. Make sure that all your latex format are inside `$` or `$$` for inline and block latex respectively. 
2. Run `python3 generate_post.py posts/example.md posts/output.html` to generate a HTML file with proper latex formatting.
3. Duplicate the `post_template.html` file and rename it to `your_title.html`. Inside the file modify the `<div class="post-title">` and `<div class="post-date">`. 
4. Copy the content of `output.html` into the `<div class="content">` class of `your_title.html`.
5. Add the new post inside the `<div class="article-list">` in `index.html` file, with the correct date and title
6. Double check the correctness of the newly added blogpost:
    - Check the links
    - Check the images (these are not automatically imported from HackMD)
    - Check the Latex formatting
7. Delete the `output.html` file and the original markdown file.
