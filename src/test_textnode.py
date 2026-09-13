import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_equal_when_url_differs(self):
        node = TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("Boot.dev", TextType.LINK, "https://example.com")
        self.assertNotEqual(node, node2)

    def test_not_equal_when_text_differs(self):
        node = TextNode("First text", TextType.TEXT)
        node2 = TextNode("Second text", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_not_equal_when_text_type_differs(self):
        node = TextNode("Same text", TextType.BOLD)
        node2 = TextNode("Same text", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        html_node = text_node_to_html_node(TextNode("bold", TextType.BOLD))
        self.assertEqual(html_node.to_html(), "<b>bold</b>")

    def test_italic(self):
        html_node = text_node_to_html_node(TextNode("italic", TextType.ITALIC))
        self.assertEqual(html_node.to_html(), "<i>italic</i>")

    def test_code(self):
        html_node = text_node_to_html_node(TextNode("code", TextType.CODE))
        self.assertEqual(html_node.to_html(), "<code>code</code>")

    def test_link(self):
        html_node = text_node_to_html_node(
            TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev")
        )
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})
        self.assertEqual(html_node.to_html(), '<a href="https://www.boot.dev">Boot.dev</a>')

    def test_image(self):
        html_node = text_node_to_html_node(
            TextNode("Boots", TextType.IMAGE, "https://example.com/boots.png")
        )
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://example.com/boots.png", "alt": "Boots"},
        )

    def test_invalid_text_type(self):
        node = TextNode("unknown", "unknown")
        with self.assertRaises(Exception):
            text_node_to_html_node(node)


if __name__ == "__main__":
    unittest.main()