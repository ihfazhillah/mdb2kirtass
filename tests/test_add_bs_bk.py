import unittest
from lxml import etree
from io import StringIO

from mdb2kirtass.add_bk import add_bk


class AddBSBKTestCase(unittest.TestCase):

    def original_group_string (self):
        return """
        <setting>
            <root Name='abc' id='1'>
                <Item Name='def' id='1'>
                    <bk />
                </Item>
            </root>
        </setting>
        """.strip()

    def test_add_bk (self):
        changed = add_bk(tree=StringIO(self.original_group_string()),
                         item_id='1', name='ini buku',
                         aut='saya', betaka='ini buku saya ihfazh',
                         bkid='bs_123')

        self.assertIn(b'saya', etree.tostring(changed))
        self.assertIn(b'ini buku', etree.tostring(changed))
        self.assertIn(b'ini buku saya', etree.tostring(changed))
        self.assertIn(b'bs_123', etree.tostring(changed))
        self.assertEqual(changed.find('.//bk[@id="bs_123"]').getparent(
                                                            ).attrib['id'],'1')
