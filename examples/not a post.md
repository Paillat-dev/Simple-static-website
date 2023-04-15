---
static: true
template: post
title: informations
---
# Informations
This file will be rendered because it has a `static: true` front matter. But it will not be added to the blog index because it has no `type: post` front matter.

You can also run custom code in the template in python, like the example in the `blog_index_read_me.html` file.

First, you need to define an html comment with the python code you want to run, but beginning with "FOR".
You can run any python code you want, but the only variable that can be updated is "final_content". To do that you can replace f"<!-- FOR {comment} -->" 
with any python code you want, but you need to update final_content with the new content.

I recommend you to import your code from a file, in order to avoid having a lot of code in the template and having closing tags in the middle of the code.