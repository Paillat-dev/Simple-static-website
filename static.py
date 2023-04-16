import os
import shutil
from utils import markdown_parser, opener, tagger, bypass_tags, for_comment
from bs4 import BeautifulSoup, Comment

source_dir = "."
destination_dir = "_site"
templates_dir = "_templates"
backup_dir = "_site_old"
images_urls = f"{templates_dir}/imgurls.txt"
extensions = [".html", ".md"]
website_name = "My Website"
scripts_dir = "_scripts"
ignore_files = ["static.py", "utils.py", "config.py", "README.md", "LICENSE", "requirements.txt", "CNAME", ".htaccess", ".gitignore", ".git"]

if os.path.exists(destination_dir):
    os.rmdir(destination_dir)

# Create the destination directory if it doesn't exist
os.makedirs(destination_dir, exist_ok=True)

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
    # Get a list of all subdirectories in the source directory
    subdirs = next(os.walk(source_dir))[1]

    # Copy all non-ignored subdirectories and their contents to the destination directory
    for subdir in subdirs:
        if not subdir.startswith("_") and subdir not in ignore_files:
            subdir_path = os.path.join(source_dir, subdir)
            if os.path.isdir(subdir_path):
                shutil.copytree(subdir_path, os.path.join(destination_dir, subdir))

    # Copy all non-ignored files in the source directory to the destination directory
    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)
        if os.path.isfile(file_path) and not filename.startswith("_") and filename not in ignore_files:
            shutil.copy2(file_path, os.path.join(destination_dir, filename))

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
                    soup = BeautifulSoup(final_content, "html.parser")
                    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
                    for comment in comments:
                        comment.extract()
                    final_content = str(soup.prettify())
                    with open(file_path.split(".")[0] + ".html", "w", encoding="utf-8") as file:
                        file.write(final_content)
                    if file_path.endswith(".md"): os.remove(file_path)
# we run the functions if name == main
if __name__ == "__main__":
    copy_files(source_dir, destination_dir)
    process_files(destination_dir)