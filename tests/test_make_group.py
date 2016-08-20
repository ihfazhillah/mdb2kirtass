import unittest
from lxml import etree
from lxml_asserts.testcase import LxmlTestCaseMixin
from io import StringIO

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

    def original_csv_bok(self):
        return StringIO("""id,name,lvl
1,shamela,3
2,book,4
3,buku,0""".strip())

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

    def test_kutub_shamela_found_twice(self):
        group = MakeGroup()
        tree = group.add_root(tree=self.original_group_etree())
        tree1 = group.add_root(tree=tree)
        tree2 = group.add_root(tree=tree1)
        expected = """
        <setting>
            <root Name='abc' id='1'>
                <Item Name='def' id='1'>
                    <bk />
                </Item>
            </root>
            <root Name='كتب الشاملة' id='sb' />
            <root Name='كتب الشاملة1' id='sb1'/>
            <root Name='كتب الشاملة2' id='sb2'/>
        </setting>
        """
        # self.fail(etree.tostring(tree2))
        self.assertXmlEqual(expected, tree2)

    def test_add_items(self):
        group = MakeGroup()
        tree = group.add_root(tree=self.original_group_etree())
        items = group.add_item(tree=tree, csvobject=self.original_csv_bok())
        expected = """
        <setting>
            <root Name='abc' id='1'>
                <Item Name='def' id='1'>
                    <bk />
                </Item>
            </root>
            <root Name='كتب الشاملة' id='sb' >
                <Item Name='shamela' id='1'/>
                <Item Name='book' id='2'/>
                <Item Name='buku' id='3'/>
            </root>
        </setting>
        """
        # self.fail(etree.tostring(items))
        self.assertXmlEqual(expected, items)
