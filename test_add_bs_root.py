import unittest
from lxml import etree
from io import StringIO

from add_root import add_root

class AddRootBsTestCase(unittest.TestCase):

    original_group_string = """
        <setting>
            <root Name='abc' id='1'>
                <Item Name='def' id='1'>
                    <bk />
                </Item>
            </root>
        </setting>
        """.strip()

    def test_add_root(self):
        changed = add_root(StringIO(self.original_group_string), {'name':'new', 'id':'123'})
        self.assertIn(b'new', etree.tostring(changed))


if __name__ == '__main__':
    unittest.main()
