import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_link, split_nodes_image, text_to_textnodes

class TestSplitNode(unittest.TestCase):
    def test_split_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT)])

    def test_split_bold_block(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("bold", TextType.BOLD), TextNode(" word", TextType.TEXT)])

    def test_split_italic_block(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("This is text with an ", TextType.TEXT), TextNode("italic", TextType.ITALIC), TextNode(" word", TextType.TEXT)])

    def test_unmatched_delimiter(self):
        with self.assertRaises(Exception):
            node = TextNode("This is a text with **unmatched delimiter", TextType.TEXT)
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_extract_markdown_images_single(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_markdown_links_ignores_images(self):
        matches = extract_markdown_links(
        "This has a ![picture](https://example.com/pic.png) but no real link"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![image](https://example.com)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("image", "https://example.com")], matches)

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_markdown_images_no_image(self):
        matches = extract_markdown_images(
            "This is plain text with no links or images"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links_no_link(self):
        matches = extract_markdown_links(
            "This is plain text with no links"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links_with_image(self):
        matches = extract_markdown_links(
            "This is text with ![url](https://example.com)"
        )
        self.assertListEqual([], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to google](https://google.com) and another [to youtube](https://youtube.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to google", TextType.LINK, "https://google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://youtube.com"),
            ],
            new_nodes,
        )

    def test_split_links_no_links(self):
        node = TextNode(
            "This is text with no links",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with no links", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_link_at_the_beginning_and_at_the_end(self):
        node = TextNode(
            "[to google](https://google.com) with a link at the beginning and at the end [to youtube](https://youtube.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("to google", TextType.LINK, "https://google.com"),
                TextNode(" with a link at the beginning and at the end ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://youtube.com"),
            ],
            new_nodes,
        )

    def test_split_links_consecutive_links_no_text(self):
        node = TextNode(
            "[to google](https://google.com)[to youtube](https://youtube.com)",
            TextType.LINK,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("[to google](https://google.com)[to youtube](https://youtube.com)",TextType.LINK,)
            ],
            new_nodes,
        )

    def test_split_links_conseccutive_links_with_text(self):
        node = TextNode(
            "[to google](https://google.com)[to youtube](https://youtube.com) text with consecutive links",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("to google", TextType.LINK, "https://google.com"),
                TextNode("to youtube", TextType.LINK, "https://youtube.com"),
                TextNode(" text with consecutive links", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_links_multiple_nodes(self):
        nodes = [
            TextNode("Text with [link](https://boot.dev)", TextType.TEXT),
            TextNode("Plain text without links", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode("Plain text without links", TextType.TEXT),
            ],
            new_nodes,
        )     

        def test_text_to_textnodes(self):
            text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
            nodes = text_to_textnodes(text)
            self.assertListEqual(
                [
                    TextNode("This is ", TextType.TEXT),
                    TextNode("text", TextType.BOLD),
                    TextNode(" with an ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" word and a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" and an ", TextType.TEXT),
                    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" and a ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://boot.dev"),
                ],
                nodes,
            )
    
        def test_text_to_textnodes_plain(self):
            text = "This is plain text"
            nodes = text_to_textnodes(text)
            self.assertListEqual(
                [
                    TextNode("This is plain text", TextType.TEXT),
                ],
                nodes,
            )
    
        def test_text_to_textnodes_bold(self):
            text = "**This is bold text**"
            nodes = text_to_textnodes(text)
            self.assertListEqual(
                [
                    TextNode("This is bold text", TextType.BOLD),
                ],
                nodes,
            )
    
        def test_text_to_textnodes_only_image(self):
            text = "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
            nodes = text_to_textnodes(text)
            self.assertListEqual(
                [
                    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                ],
                nodes,
               )
    
        def test_text_to_textnodes_only_link(self):
            text = "[link](https://boot.dev)"
            nodes = text_to_textnodes(text)
            self.assertListEqual(
                [
                    TextNode("link", TextType.LINK, "https://boot.dev"),
                ],
                nodes,
            )
    
        def test_text_to_textnodes_multiple_links(self):
            text = "[link](https://boot.dev)[link](https://youtube.com)"
            nodes = text_to_textnodes(text)
            self.assertListEqual(
                [
                    TextNode("link", TextType.LINK, "https://boot.dev"),
                    TextNode("link", TextType.LINK, "https://youtube.com"),
                ],
                nodes,
            )
    
        def test_text_to_textnodes_adjacent_formatting(self):
            text = "**bold text**_italic text_"
            nodes = text_to_textnodes(text)
            self.assertListEqual(
                [
                    TextNode("bold text", TextType.BOLD),
                    TextNode("italic text", TextType.ITALIC),
                ],
                nodes,
            )
if __name__ == "__main__":
    unittest.main()