import unittest
from lxml import etree
from lxml_asserts.testcase import LxmlTestCaseMixin

from mdb2kirtass.group import MakeGroup


class MakeGroupTestCase(unittest.TestCase, LxmlTestCaseMixin):

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

    def original_group_etree(self):
        return etree.fromstring(self.original_group_string())

    def test_kutub_shamela_not_found(self):
        group = MakeGroup()
        add_root  = group.add_root(tree=self.original_group_etree())
        expected = """
        <setting>
            <root Name='abc' id='1'>
                <Item Name='def' id='1'>
                    <bk />
                </Item>
            </root>
            <root Name='كتب الشاملة' id='sb' />
        </setting>
        """
        self.assertXmlEqual(expected, add_root)

    def test_kutub_shamela_found_once(self):
        group = MakeGroup()
        tree = group.add_root(tree=self.original_group_etree())
        tree2 = group.add_root(tree=tree)
        expected = """
        <setting>
            <root Name='abc' id='1'>
                <Item Name='def' id='1'>
                    <bk />
                </Item>
            </root>
            <root Name='كتب الشاملة' id='sb' />
            <root Name='كتب الشاملة1' id='sb1'/>
        </setting>
        """
        self.assertXmlEqual(expected, tree2)
