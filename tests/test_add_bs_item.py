import unittest
from lxml import etree
from io import StringIO

from mdb2kirtass.add_item import add_item

class AddItemBSTestCase(unittest.TestCase):

    def original_group_string(self):
        return """
        <setting>
            <root Name='abc' id='1'>
                <Item Name='def' id='1'>
                    <bk />
                </Item>
            </root>
        </setting>
        """.strip()

    def test_add_item_by_root_id(self):
        changed = add_item(tree=StringIO(self.original_group_string()),
                            root_id=1, item_name='islam', item_id='12')
        self.assertIn(b'islam', etree.tostring(changed))
        self.assertIn(b'12', etree.tostring(changed))
