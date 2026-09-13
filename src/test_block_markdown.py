import unittest

from block_markdown import markdown_to_blocks


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


if __name__ == "__main__":
    unittest.main()