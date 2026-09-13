import re

from textnode import TextNode, TextType


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    if not delimiter:
        raise ValueError("delimiter cannot be empty")

    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise Exception("invalid markdown: missing closing delimiter")

        for index, section in enumerate(sections):
            if not section:
                continue
            node_type = text_type if index % 2 == 1 else TextType.TEXT
            new_nodes.append(TextNode(section, node_type))

    return new_nodes