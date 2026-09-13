import re

from textnode import TextNode, TextType


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def _split_nodes_by_markdown(old_nodes, extractor, text_type, prefix):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text
        matches = extractor(remaining_text)
        for label, url in matches:
            markdown = f"{prefix}[{label}]({url})"
            sections = remaining_text.split(markdown, 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(label, text_type, url))
            remaining_text = sections[1]
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_nodes_by_markdown(
        old_nodes, extract_markdown_images, TextType.IMAGE, "!"
    )


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_nodes_by_markdown(
        old_nodes, extract_markdown_links, TextType.LINK, ""
    )


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