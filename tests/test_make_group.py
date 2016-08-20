import unittests
from lxml import etree
from lxml_asserts.testcase import LxmlTestCaseMixin


class MakeGroupTestCase(unittests.TestCase, LxmlTestCaseMixin):

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

    
