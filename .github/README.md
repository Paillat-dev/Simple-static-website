# Simple static site generator

This is a simple static site generator written in Python. It was created for those who found Jekyll too complicated and just want a simple solution to generate static sites.

## Usage

The `static.py` file is the main file that will generate the static site. You can configure the variables in this file to customize your site:

- `source_dir`: the directory where your source files are located
- `destination_dir`: the directory where your generated files will be placed
- `templates_dir`: the directory where your template files are located
- `backup_dir`: the directory where your old generated files will be placed (if you choose to backup)
- `images_urls`: a file that contains all the image URLs used in your templates
- `extensions`: a list of file extensions to include in the generation process
- `website_name`: the name of your website
- `scripts_dir`: the directory where your custom Python scripts are located (if you have any)

To generate your site, simply run `python static.py` from the command line. Your generated site will be located in the `destination_dir` that you specified.

## File Structure

The generator looks for files in the `source_dir`. The files can be in either HTML or Markdown format. If you want to use Markdown, make sure to include the YAML front matter at the beginning of your file. You can also include tags in the front matter to customize your page, such as `title` or `modified-date`.

If you want to include a page as a non processed page (not processed as a Markdown or html file), include the tag `static:false` in the front matter. If you wan it to be prcessed you WILL need to add the `static:true` tag. You can also include the tag `template:any template` to specify which template to use for the static page. This will look for a file in the `templates_dir` with the name `any_template.html`.

Your templates should have a `<!-- content -->` html comment where the content of your pages will be placed. You can also include other tags in your templates, such as `<!-- title -->` or `<!-- modified-date -->`, which will be replaced with the corresponding tag value from your page.

## Custom Code in Templates

You can include custom Python code in your templates by using an HTML comment with the prefix `FOR`. The only variable that can be updated in the code is `final_content`, which represents the content of the page. You can import your custom code from a file to avoid having a lot of code in your template. See an example in the `examples` directory.

## Code Explanation

The generator is composed of two files: `static.py` and `utils.py`.

`static.py` is the main file that generates the static site. It first checks if the destination directory exists and removes it if it does. It then creates the destination directory and starts copying files from the source directory to the destination directory.

The `is_static` function checks if a file is static by looking for the `static:true` tag in the front matter. If the file is static, it also returns the template to use for the page.

The `copy_files` function recursively walks through the source directory and copies all files to the destination directory, while ignoring directories that start with an underscore.

The `process_files` function recursively walks through the destination directory and processes all files with the extensions specified in the `extensions` variable. If the file is a static page, it replaces the `<!-- content -->` tag in the template with the content of the page. It also replaces other tags in the template with the corresponding tag value from the page. Finally, it executes any custom Python code in the template that is enclosed in an HTML comment with the prefix `FOR`.

`utils.py` contains helper functions used by `static.py`. The `markdown_parser` function parses Markdown content using the `mistune` library and a custom renderer. If the content starts with YAML front matter, it removes it before parsing the Markdown. If the content starts with an HTML comment, it returns the content as is.

The `opener` function opens a file with the correct encoding, handling UnicodeDecodeErrors and FileNotFoundError exceptions.

The `tagger` function extracts tags from the front matter of a file and returns them as a dictionary. It also handles tags with values that contain colons.

The `for_comment` function extracts HTML comments from a page that start with the prefix `FOR` and returns them as a list.

## Conclusion

This simple static site generator is not meant to be beautiful or feature-rich, but it gets the job done. It allows you to quickly generate static sites from Markdown or HTML files with customizable templates and tags. Feel free to modify and improve the code to fit your needs, and to pull request!