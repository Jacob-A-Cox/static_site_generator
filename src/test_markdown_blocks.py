import unittest

from markdown_blocks import(
    markdown_to_blocks,
    block_to_block_type,
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_quote,
    block_type_unordered_list,
    block_type_ordered_list,
)

class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        text_to_block = """
# I want to block out this text.

So I'll test and test and test.
The testing regiment is as follows:

1. We write the tests.
2. ...
3. Profit.
"""
        new_blocks = markdown_to_blocks(text_to_block)
        self.assertListEqual(
            [
                "# I want to block out this text.",
                "So I'll test and test and test.\nThe testing regiment is as follows:",
                "1. We write the tests.\n2. ...\n3. Profit."
            ],
            new_blocks,
        )

    def test_markdown_to_blocks_newlines(self):
        text_to_block = """
# I want to test excessive newlines.




So I'll test and test and test.
The testing regiment is as follows:




1. We write the tests.
2. ...
3. Profit.
"""
        new_blocks = markdown_to_blocks(text_to_block)
        self.assertListEqual(
            [
                "# I want to test excessive newlines.",
                "So I'll test and test and test.\nThe testing regiment is as follows:",
                "1. We write the tests.\n2. ...\n3. Profit."
            ],
            new_blocks,
        )

    def test_block_to_block_type(self):
        #test headers
        h1 = "# This shall be a heading."
        h2 = "### This shall also be a heading."
        h1_test = block_to_block_type(h1)
        h2_test = block_to_block_type(h2)
        self.assertEqual(block_type_heading, h1_test)
        self.assertEqual(block_type_heading, h2_test)

        #test code
        code_1 = "```This is a block of code```"
        code_2 = """```This is a longer block of code
hopefully you don't need this much
but it always helps to test```"""
        code_1_test = block_to_block_type(code_1)
        code_2_test = block_to_block_type(code_2)
        self.assertEqual(block_type_code, code_1_test,)
        self.assertEqual(block_type_code, code_2_test)

        #test quotes
        quote_1 = ">A single quoted line"
        quote_2 = """>A multiline quote
>That appears on multiple lines"""
        quote_1_test = block_to_block_type(quote_1)
        quote_2_test = block_to_block_type(quote_2)
        self.assertEqual(block_type_quote, quote_1_test)
        self.assertEqual(block_type_quote, quote_2_test)

        #test unordered lists
        uo_list_1 = "* A single item in a list"
        uo_list_2 = "- Another item in a dashed list"
        uo_list_3 = """* All the single items (all the single items)
* Put your hands up (up)
* Up in the air (air)"""
        uo_list_1_test = block_to_block_type(uo_list_1)
        uo_list_2_test = block_to_block_type(uo_list_2)
        uo_list_3_test = block_to_block_type(uo_list_3)
        self.assertEqual(block_type_unordered_list, uo_list_1_test)
        self.assertEqual(block_type_unordered_list, uo_list_2_test)
        self.assertEqual(block_type_unordered_list, uo_list_3_test)

        #test ordered lists
        o_list_1 = "1. Groceries"
        o_list_2 = """1. Steal all the underpants
2. ...
3. Profit!"""
        o_list_1_test = block_to_block_type(o_list_1)
        o_list_2_test = block_to_block_type(o_list_2)
        self.assertEqual(block_type_ordered_list, o_list_1_test,)
        self.assertEqual(block_type_ordered_list, o_list_2_test)

        #test paragraph
        p1 = "This is the only correctly formatted paragraph."
        p1_test = block_to_block_type(p1)
        self.assertEqual(block_type_paragraph, p1_test)

        #test incorrect formats return paragraph
        #incorrect headers
        p_h1 = "#Headers require a space between the hash and text."
        p_h1_test = block_to_block_type(p_h1)
        self.assertEqual(block_type_paragraph, p_h1_test)

        #incorrect code
        p_code_1 = "```This is an incorrectly formatted code block."
        p_code_2 = "This is another incorrectly formatted code block.``"
        p_code_3 = "``Another one!``"
        p_code_4 = "A final incorrectly formatted code block.```"
        p_code_1_test = block_to_block_type(p_code_1)
        p_code_2_test = block_to_block_type(p_code_2)
        p_code_3_test = block_to_block_type(p_code_3)
        p_code_4_test = block_to_block_type(p_code_4)
        self.assertEqual(block_type_paragraph, p_code_1_test)
        self.assertEqual(block_type_paragraph, p_code_2_test)
        self.assertEqual(block_type_paragraph, p_code_3_test)
        self.assertEqual(block_type_paragraph, p_code_4_test)
        
        #incorrect quotes
        p_quote_1 = """>This quote
Will not be correctly formatted"""
        p_quote_2 = """Neither will this quote
>Be correctly formatted"""
        p_quote_1_test = block_to_block_type(p_quote_1)
        p_quote_2_test = block_to_block_type(p_quote_2)
        self.assertEqual(block_type_paragraph, p_quote_1_test,)
        self.assertEqual(block_type_paragraph, p_quote_2_test)
        
        #incorrect unordered lists
        p_uo_1 = "*First, a test of the spacing on unordered lists"
        p_uo_2 = """* Next, we'll test
 if every line needs an asterix."""
        p_uo_1_test = block_to_block_type(p_uo_1)
        p_uo_2_test = block_to_block_type(p_uo_2)
        self.assertEqual(block_type_paragraph, p_uo_1_test,)
        self.assertEqual(block_type_paragraph, p_uo_2_test)

        #incorrect ordered lists
        p_o_1 = "1.There must be a space."
        p_o_2 = """1. Must
1. increment
1. numbers"""
        p_o_3 = """1. on
 every
3. line"""
        p_o_1_test = block_to_block_type(p_o_1)
        p_o_2_test = block_to_block_type(p_o_2)
        p_o_3_test = block_to_block_type(p_o_3)
        self.assertEqual(block_type_paragraph, p_o_1_test,)
        self.assertEqual(block_type_paragraph, p_o_2_test)
        self.assertEqual(block_type_paragraph, p_o_3_test)



if __name__ == "__main__":
    unittest.main()