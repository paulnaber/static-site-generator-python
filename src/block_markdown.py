from enum import Enum

from parentnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = []
    for block in markdown.split("\n\n"):
        block = block.strip()
        # Ignore empty blocks.
        if block:
            blocks.append(block)
    return blocks


def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")

    # A block with three backticks is a code block.
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    for number_of_hashes in range(1, 7):
        heading_start = "#" * number_of_hashes + " "
        # One to six hash characters mark a heading.
        if lines[0].startswith(heading_start):
            return BlockType.HEADING

    # Every line must start with a greater-than sign.
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Every line must start with a dash and a space.
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    ordered_list = True
    for index, line in enumerate(lines, start=1):
        # Ordered lists must start at 1 and use consecutive numbers.
        if not line.startswith(f"{index}. "):
            ordered_list = False
            break
    # If every line matches, this is an ordered list.
    if ordered_list:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown: str) -> ParentNode:
    block_nodes = []

    for block in markdown_to_blocks(markdown):
        block_type = block_to_block_type(block)
        lines = block.split("\n")

        # Keep code block contents without inline Markdown parsing.
        if block_type == BlockType.CODE:
            code = block[4:-3]
            code_node = text_node_to_html_node(
                TextNode(code, TextType.TEXT)
            )
            block_nodes.append(ParentNode("pre", [ParentNode("code", [code_node])]))
        # Render headings as h1 through h6 based on the hash count.
        elif block_type == BlockType.HEADING:
            hashes = 0
            while lines[0][hashes] == "#":
                hashes += 1
            text = block[hashes + 1:]
            children = [
                text_node_to_html_node(node)
                for node in text_to_textnodes(text)
            ]
            block_nodes.append(ParentNode(f"h{hashes}", children))
        # Remove quote markers and render the block as a blockquote.
        elif block_type == BlockType.QUOTE:
            text = " ".join(line[1:].lstrip() for line in lines)
            children = [
                text_node_to_html_node(node)
                for node in text_to_textnodes(text)
            ]
            block_nodes.append(ParentNode("blockquote", children))
        # Render unordered lists as ul elements with li children.
        elif block_type == BlockType.UNORDERED_LIST:
            items = []
            for line in lines:
                text = line[2:]
                children = [
                    text_node_to_html_node(node)
                    for node in text_to_textnodes(text)
                ]
                items.append(ParentNode("li", children))
            block_nodes.append(ParentNode("ul", items))
        # Render ordered lists as ol elements with li children.
        elif block_type == BlockType.ORDERED_LIST:
            items = []
            for line in lines:
                text = line.split(". ", 1)[1]
                children = [
                    text_node_to_html_node(node)
                    for node in text_to_textnodes(text)
                ]
                items.append(ParentNode("li", children))
            block_nodes.append(ParentNode("ol", items))
        else:
            text = " ".join(lines)
            children = [
                text_node_to_html_node(node)
                for node in text_to_textnodes(text)
            ]
            block_nodes.append(ParentNode("p", children))

    return ParentNode("div", block_nodes)