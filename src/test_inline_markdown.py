import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
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

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) "
            "and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode(
                    "image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"
                ),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) "
            "and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_without_matches(self):
        node = TextNode("plain text", TextType.TEXT)
        self.assertListEqual([node], split_nodes_image([node]))
        self.assertListEqual([node], split_nodes_link([node]))

    def test_split_nodes_preserves_non_text_nodes(self):
        node = TextNode("already bold", TextType.BOLD)
        self.assertIs(split_nodes_image([node])[0], node)
        self.assertIs(split_nodes_link([node])[0], node)

    def test_split_image_at_text_boundaries(self):
        self.assertEqual(
            split_nodes_image(
                [TextNode("![alt](https://example.com/image.png)", TextType.TEXT)]
            ),
            [TextNode("alt", TextType.IMAGE, "https://example.com/image.png")],
        )

    def test_text_to_textnodes_with_all_inline_types(self):
        nodes = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` "
            "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image",
                    TextType.IMAGE,
                    "https://i.imgur.com/fJRm4Vk.jpeg",
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_text_to_textnodes_with_plain_text(self):
        node = TextNode("plain text", TextType.TEXT)
        self.assertListEqual([node], text_to_textnodes("plain text"))

    def test_text_to_textnodes_with_multiple_formats(self):
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("more bold", TextType.BOLD),
            ],
            text_to_textnodes("**bold** and **more bold**"),
        )


if __name__ == "__main__":
    unittest.main()