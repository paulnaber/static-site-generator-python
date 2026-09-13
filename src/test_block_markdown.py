import unittest

from block_markdown import BlockType, block_to_block_type, markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\n"
                "This is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_removes_empty_blocks(self):
        self.assertEqual(
            markdown_to_blocks("\n\nFirst block\n\n\n\nSecond block\n\n"),
            ["First block", "Second block"],
        )

    def test_strips_block_whitespace(self):
        self.assertEqual(
            markdown_to_blocks("  first block  \n\n\tsecond block\t"),
            ["first block", "second block"],
        )

    def test_empty_markdown(self):
        self.assertEqual(markdown_to_blocks("\n\n"), [])

    def test_block_to_block_type_paragraph(self):
        self.assertEqual(
            block_to_block_type("This is a paragraph."), BlockType.PARAGRAPH
        )

    def test_block_to_block_type_headings(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(
            block_to_block_type("###### Heading"), BlockType.HEADING
        )
        self.assertEqual(
            block_to_block_type("####### Too many hashes"), BlockType.PARAGRAPH
        )

    def test_block_to_block_type_code(self):
        self.assertEqual(
            block_to_block_type("```\nprint('hello')\n```"), BlockType.CODE
        )
        self.assertEqual(block_to_block_type("```not a code block"), BlockType.PARAGRAPH)

    def test_block_to_block_type_quote(self):
        self.assertEqual(
            block_to_block_type("> first line\n>second line"), BlockType.QUOTE
        )
        self.assertEqual(
            block_to_block_type("> quote\nnot a quote"), BlockType.PARAGRAPH
        )

    def test_block_to_block_type_unordered_list(self):
        self.assertEqual(
            block_to_block_type("- first\n- second"), BlockType.UNORDERED_LIST
        )
        self.assertEqual(
            block_to_block_type("- first\n* second"), BlockType.PARAGRAPH
        )

    def test_block_to_block_type_ordered_list(self):
        self.assertEqual(
            block_to_block_type("1. first\n2. second"), BlockType.ORDERED_LIST
        )
        self.assertEqual(
            block_to_block_type("1. first\n3. third"), BlockType.PARAGRAPH
        )
        self.assertEqual(
            block_to_block_type("2. second\n3. third"), BlockType.PARAGRAPH
        )


if __name__ == "__main__":
    unittest.main()