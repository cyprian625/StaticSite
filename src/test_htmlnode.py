import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode 

class TestHTMLNode(unittest.TestCase):
    def test_empty(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_one_property(self):
        node = HTMLNode(props = {"src":"image.png"})
        self.assertEqual(node.props_to_html(), ' src="image.png"')

    def test_two_properties(self):
        node = HTMLNode(props = {"href":"https://example.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com" target="_blank"')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_with_properties(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_missing_value(self):
        node = LeafNode("a", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_no_children(self):
        parent_node = ParentNode("b", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_empty_children_list(self):
        parent_node = ParentNode("b", [])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_two_children_at_on_level(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node, grandchild_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>child</span><b>grandchild</b></div>",
        )

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "greeting"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="greeting"><span>child</span></div>'
        )
if __name__ == "__main__":
    unittest.main()
