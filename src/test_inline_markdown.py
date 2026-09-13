import unittest

from inline_markdown import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_splits_code(self):
        nodes = split_nodes_delimiter(
            [TextNode("This is text with a `code block` word", TextType.TEXT)],
            "`",
            TextType.CODE,
        )
        self.assertEqual(
            nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_splits_bold_and_italic(self):
        bold_nodes = split_nodes_delimiter(
            [TextNode("A **bold** word", TextType.TEXT)], "**", TextType.BOLD
        )
        italic_nodes = split_nodes_delimiter(
            [TextNode("An _italic_ word", TextType.TEXT)], "_", TextType.ITALIC
        )
        self.assertEqual(
            bold_nodes,
            [
                TextNode("A ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
        )
        self.assertEqual(
            italic_nodes,
            [
                TextNode("An ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_preserves_non_text_nodes(self):
        bold_node = TextNode("already bold", TextType.BOLD)
        nodes = split_nodes_delimiter(
            [bold_node, TextNode("plain", TextType.TEXT)], "`", TextType.CODE
        )
        self.assertIs(nodes[0], bold_node)
        self.assertEqual(nodes[1], TextNode("plain", TextType.TEXT))

    def test_supports_multiple_delimited_sections(self):
        nodes = split_nodes_delimiter(
            [TextNode("`one` and `two`", TextType.TEXT)], "`", TextType.CODE
        )
        self.assertEqual(
            nodes,
            [
                TextNode("one", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("two", TextType.CODE),
            ],
        )

    def test_raises_for_missing_closing_delimiter(self):
        with self.assertRaises(Exception):
            split_nodes_delimiter(
                [TextNode("missing ` delimiter", TextType.TEXT)],
                "`",
                TextType.CODE,
            )

    def test_empty_segments_are_omitted(self):
        nodes = split_nodes_delimiter(
            [TextNode("**bold**", TextType.TEXT)], "**", TextType.BOLD
        )
        self.assertEqual(nodes, [TextNode("bold", TextType.BOLD)])


if __name__ == "__main__":
    unittest.main()