import os
import shutil
import sys

from block_markdown import markdown_to_html_node


def copy_static(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("no h1 header found")


def generate_page(from_path, template_path, dest_path, basepath):
    print(
        f"Generating page from `{from_path}` to `{dest_path}` "
        f"using `{template_path}`"
    )

    with open(from_path) as markdown_file:
        markdown = markdown_file.read()
    with open(template_path) as template_file:
        template = template_file.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    page = template.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", html)
    page = page.replace('href="/', f'href="{basepath}')
    page = page.replace('src="/', f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as destination_file:
        destination_file.write(page)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for entry in os.listdir(dir_path_content):
        content_path = os.path.join(dir_path_content, entry)
        destination_path = os.path.join(dest_dir_path, entry)

        if os.path.isfile(content_path) and entry.endswith(".md"):
            destination_path = destination_path[:-3] + ".html"
            generate_page(content_path, template_path, destination_path, basepath)
        elif os.path.isdir(content_path):
            generate_pages_recursive(
                content_path, template_path, destination_path, basepath
            )


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_static("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()