import unittest
from lxml import etree
from lxml_asserts.testcase import LxmlTestCaseMixin


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
        return etree.Element(self.original_group_string())

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
