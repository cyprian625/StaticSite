import unittest 
from markdown_blocks import markdown_to_blocks, BlockType, block_to_block_type, markdown_to_html_node, extract_title

class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
        blocks,
        [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here",
        ],
    )

    def test_block_to_block_type_paragraph(self):
        block = "This is paragraph"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    def test_block_to_block_type_heading(self):
        block = "### This is heading block"
        self.assertEqual(BlockType.HEADING, block_to_block_type(block))

    def test_block_to_block_type_code(self):
        block = "```\nThis is code block\n```"
        self.assertEqual(BlockType.CODE, block_to_block_type(block))

    def test_block_to_block_type_quote(self):
        block = "> This is quote block"
        self.assertEqual(BlockType.QUOTE, block_to_block_type(block))

    def test_block_to_block_type_unordered_list(self):
        block = "- this\n- is\n- unordered\n- list"
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(block))

    def test_block_to_block_type_ordered_list(self):
        block = "1. this\n2. is\n3. ordered\n4. list"
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(block))

    def test_block_to_block_type_header_without_space(self):
        block = "##This is not heading block"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    def test_block_to_block_type_unordered_ordered_list(self):
        block = "1. this\n2. isn't\n4. ordered\n5. list"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = """
# this is a heading

### this is also a heading

####### and this is not a heading
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is a heading</h1><h3>this is also a heading</h3><p>####### and this is not a heading</p></div>"
        )

    def test_unordered_list(self):
        md = """
- this
- is
- unordered
- list
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>this</li><li>is</li><li>unordered</li><li>list</li></ul></div>"
        )

    def test_ordered_list(self):
        md = """
1. this
2. is
3. ordered
4. list
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>this</li><li>is</li><li>ordered</li><li>list</li></ol></div>"
        )

    def test_blockquotes(self):
        md = """
> this 
> is
> quote
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>this is quote</blockquote></div>"
        )

    def test_inline_markdown_inside_list(self):
        md = """
- **bold**
- _italic_
- `code`
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li><b>bold</b></li><li><i>italic</i></li><li><code>code</code></li></ul></div>"
        )

    def test_multiple_blocks(self):
        md = """
# heading

```
code block
```

- unordered
- list

1. ordered
2. list

> quote block

paragraph
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>heading</h1><pre><code>code block\n</code></pre><ul><li>unordered</li><li>list</li></ul><ol><li>ordered</li><li>list</li></ol><blockquote>quote block</blockquote><p>paragraph</p></div>"
        )
if __name__ == "__main__":

    def test_extract_title_normal_h1(self):
        md = "# heading"
        self.assertEqual(
            extract_title(md),
            "heading"
        )

    def test_extract_title_h1_in_second_line(self):
        md = """
paragraph

# heading
"""
        self.assertEqual(
            extract_title(md),
            "heading"
        )
    
    def test_extract_title_no_h1(self):
        md = "paragraph"
        with self.assertRaises(Exception):
            extract_title(md)

    def test_extract_title_with_whitespace(self):
        md = "#  heading "
        self.assertEqual(
            extract_title(md),
            "heading"
        )

    unittest.main()
