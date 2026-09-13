from enum import Enum


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
        if block:
            blocks.append(block)
    return blocks


def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")

    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    for number_of_hashes in range(1, 7):
        heading_start = "#" * number_of_hashes + " "
        if lines[0].startswith(heading_start):
            return BlockType.HEADING

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    ordered_list = True
    for index, line in enumerate(lines, start=1):
        if not line.startswith(f"{index}. "):
            ordered_list = False
            break
    if ordered_list:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH