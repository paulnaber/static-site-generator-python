import os
import shutil

from block_markdown import markdown_to_html_node


def copy_static_to_public(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("no h1 header found")


def generate_page(from_path, template_path, dest_path):
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

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as destination_file:
        destination_file.write(page)


def main():
    copy_static_to_public("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()