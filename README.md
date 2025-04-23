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
3. From root run `python3 generate_post.py example.md output.html` to clean up the HTML file. This will generate a new file `output.html` with the cleaned up HTML.
4. Add the new post inside the `<div class="article-list">` in `index.html` file, with the correct date and title
5. Double check the correctness of the HTML:
    - Check the links
    - Check the images
    - Check the Latex formatting
