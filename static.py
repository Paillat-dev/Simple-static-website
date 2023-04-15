import os
import shutil
from utils import markdown_parser, opener, tagger, bypass_tags, for_comment

source_dir = "."
destination_dir = "_site"
templates_dir = "_templates"
backup_dir = "_site_old"
images_urls = f"{templates_dir}/imgurls.txt"
extensions = [".html", ".md"]
website_name = "My Website"
scripts_dir = "_scripts"

if os.path.exists(destination_dir):
    #remove it
    os.rmdir(destination_dir)

# Create the destination directory if it doesn't exist
os.makedirs(destination_dir, mode=0o777, exist_ok=True) # mode=0o777 is for Windows, and means that the directory is fully accessible

# Define a function to check if a file is static
def is_static(file_path):
    content = opener(file_path)
    tags = tagger(content)
    print(tags)
    if "static" in tags and tags["static"] == "true":
        return True, tags.get("template")
    return False, None

# Walk through the source directory and copy all files to the destination directory
def copy_files(source_dir, destination_dir):
    for root, dirs, files in os.walk(source_dir):
        dirs[:] = [d for d in dirs if not d.startswith("_")]
        for file_name in files:
            if os.path.splitext(file_name)[1] in extensions:
                source_path = os.path.join(root, file_name)
                destination_path = os.path.join(destination_dir, os.path.relpath(source_path, source_dir))
                os.makedirs(os.path.dirname(destination_path), exist_ok=True)
                shutil.copy2(source_path, destination_path)

def process_files(destination_dir):
    for root, dirs, files in os.walk(destination_dir):
        for file_name in files:
            if os.path.splitext(file_name)[len(os.path.splitext(file_name)) - 1] in extensions:
                if file_name.endswith(".html"): print(f"Processing {file_name}...")
                file_path = os.path.join(root, file_name)
                is_static_file, template = is_static(file_path)
                if is_static_file:
                    content = opener(file_path)
                    tags = tagger(content)
                    html_content = markdown_parser(content)
                    template_content = opener(f"{templates_dir}/{tags['template']}.html")
                    final_content = template_content.replace("<!-- content -->", html_content)
                    title = ""
                    for tag in tags:
                        if not tag in bypass_tags: final_content = final_content.replace(f"<!-- {tag} -->", tags[tag])
                        if tag == "title":
                            title = tags[tag]
                    final_content = final_content.replace("<!-- page-title -->", f"{file_name.split('.')[0]} - {website_name}" if not title else f"{title} - {website_name}")
                    for comment in for_comment(final_content):
                        for line in comment.splitlines():
                            locales = locals()
                            globales = globals()
                            print("executing this:", line)
                            exec(line, globales, locales)
                            final_content = locales["final_content"]
                    with open(file_path.split(".")[0] + ".html", "w", encoding="utf-8") as file:
                        file.write(final_content)
                    if file_path.endswith(".md"): os.remove(file_path)
# we run the functions if name == main
if __name__ == "__main__":
    copy_files(source_dir, destination_dir)
    process_files(destination_dir)