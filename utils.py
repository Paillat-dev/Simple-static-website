import mistune
from bs4 import BeautifulSoup, Comment

bypass_tags = ["static", "template", "page-title", "title", "modified-date", "content"]

def markdown_parser(content):
    if content.startswith("<!--"):
        return content
    #keep the part after the first --- --- yaml block. BUT keep in mind that the content can contain --- --- too, so we need to split it only once and can't use split("---")!
    if content.startswith("---"):
        first_part = content.split("---")[1]
        #remove the first part from the content
        content = content.replace(f"---{first_part}---", "")
        return mistune.html(content)

def opener(file_path):
    # Open a file with the correct encoding and try except block
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        return content
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="latin-1") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return ""
    except Exception as e:
        print(f"Error: {e}")
        return ""

def tagger(content):
    if content.startswith("---"):
        tags = content.split("---")[1]
    elif content.startswith("<!--"):
        tags = content.split("<!--")[1]
        tags = tags.split("-->")[0]
    else:
        return {}
    tags = tags.split("\n")
    tags = [tag.split(":") for tag in tags] #there can be : in the value, but wie need to keep it whole! The only : we separate is the one between key and value, the other ones not!
    tags = {tag[0].strip(): ":".join(tag[1:]).strip() for tag in tags if len(tag) > 1} #join the value again, if there was a : in it
    for tag in tags:
        if tags[tag].startswith('"') and tags[tag].endswith('"'):
            tags[tag] = tags[tag][1:-1]
    return tags

def for_comment(content):
    #find html comments with bs4
    soup = BeautifulSoup(content, 'html.parser')
    comments = soup.find_all(string=lambda text:isinstance(text, Comment))
    print(comments)
    for comment in comments:
        comments[comments.index(comment)] = str(comment).strip()
    for_comments = [comment[4:] for comment in comments if comment.startswith("FOR ")]
    return for_comments