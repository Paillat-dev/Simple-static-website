---
static: true
template: po
author: Some Author
title: Some Title
description: Some Description
image: https://www.example.com/image.png
type: post
---
# This is a post
This file will be rendered because it has a `static: true` front matter. And it will be added to the blog index because it has a `type: post` front matter. 

The title of the post will be the title defined in the front matter. If there is no title defined in the front matter, the title will be the name of the file without the extension. 

The description of the post will be the description defined in the front matter. If there is no description defined in the front matter, the description will be an empty string. 

The image of the post will be the image defined in the front matter. If there is no image defined in the front matter, the image will be an empty string. 

The author of the post will be the author defined in the front matter. If there is no author defined in the front matter, the author will be an empty string.