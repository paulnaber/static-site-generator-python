import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
)
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

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")], matches
        )

    def test_extract_multiple_markdown_images(self):
        matches = extract_markdown_images(
            "![one](https://example.com/one.png) and "
            "![two](https://example.com/two.jpg)"
        )
        self.assertListEqual(
            [
                ("one", "https://example.com/one.png"),
                ("two", "https://example.com/two.jpg"),
            ],
            matches,
        )

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) "
            "and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_links_do_not_include_images(self):
        matches = extract_markdown_links(
            "![image](https://example.com/image.png) [link](https://example.com)"
        )
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_extract_empty_alt_and_anchor_text(self):
        self.assertListEqual(
            [("", "https://example.com/image.png")],
            extract_markdown_images("![](https://example.com/image.png)"),
        )
        self.assertListEqual(
            [("", "https://example.com")],
            extract_markdown_links("[](https://example.com)"),
        )


if __name__ == "__main__":
    unittest.main()