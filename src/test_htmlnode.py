import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_multiple_props(self):
        node = HTMLNode(
            "a",
            "Boot.dev",
            props={"href": "https://www.boot.dev", "target": "_blank"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.boot.dev" target="_blank"',
        )

    def test_props_to_html_without_props(self):
        self.assertEqual(HTMLNode("p", "Some text").props_to_html(), "")
        self.assertEqual(HTMLNode("p", "Some text", props={}).props_to_html(), "")

    def test_to_html_is_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            HTMLNode("p", "Some text").to_html()

    def test_repr_contains_node_data(self):
        node = HTMLNode("p", "Some text", props={"class": "intro"})
        self.assertEqual(
            repr(node),
            "HTMLNode(p, Some text, None, {'class': 'intro'})",
        )


if __name__ == "__main__":
    unittest.main()