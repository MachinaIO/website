# Machina iO website

```bash
open index.html
```

### How to add a blogpost

```
pip install markdown2 pyyaml
```

1. Write the blogpost on HackMD
2. From HackMD, download the file to markdown. For example, `example.md`.
3. Run `python3 generate_post.py example.md output.html` to clean up the HTML file. This will generate a new file `output.html` with the cleaned up HTML.
4. Duplicate the `blogpost_template.md` file and rename it to `title.md`, modify the `post-title` and `post-date`. 
5. Copy the content of `output.html` into the `<div class="content">` class of `title.md`.
6. Add the new post inside the `<div class="article-list">` in `index.html` file, with the correct date and title
7. Double check the correctness of the HTML:
    - Check the links
    - Check the images (these are not automatically imported from HackMD)
    - Check the Latex formatting
