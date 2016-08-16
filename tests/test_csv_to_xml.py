import unittest
from lxml import etree
from io import StringIO
from lxml_asserts.testcase import LxmlTestCaseMixin

from mdb2kirtass.csv_to_xml import CsvtoXml


class CsvtoXmlTestCase(unittest.TestCase, LxmlTestCaseMixin):

    def original_csv_file(self):
        return StringIO("""bk,no,betaka,authno,cat
nama,1,ini buku bagus,1,3
munawir,2,kamus indo arab,2,4
sidu,3,kertas putih,4,3""".strip())


    def test_dapatkan_satu_baris_pertama(self):
        data = dict(bk='nama', no='1',
                    betaka='ini buku bagus', authno='1', cat='3')
        hasil = CsvtoXml(self.original_csv_file())
        self.assertEqual(data, list(hasil._dict_csv())[0])

    def test_buat_xml_file_dengan_tag_header_text_isi(self):
        """header csv adalah tag, dan isi adalah text tanpa
        ada perubahan nama"""
        hasil = CsvtoXml(self.original_csv_file())
        expected = """<item><bk>nama</bk><no>1</no><betaka>ini buku bagus</betaka><authno>1</authno><cat>3</cat>
        <bk>munawir</bk><no>2</no><betaka>kamus indo arab</betaka><authno>2</authno><cat>4</cat>
        <bk>sidu</bk><no>3</no><betaka>kertas putih</betaka><authno>4</authno><cat>3</cat>
        </item>"""
        self.assertXmlEqual(expected,
                    hasil._make_xml_original())

    def test_buat_xml_objek_dengan_tag_header_setiap_row_dengan_parent(self):
        """header csv adalah tag, setiap baris ada tag parent, dengan root
        adalah item, tanpa ada perubahan nama"""
        hasil = CsvtoXml(self.original_csv_file())._make_xml_original(parent='book')
        expected = """<item>
        <book><bk>nama</bk><no>1</no><betaka>ini buku bagus</betaka><authno>1</authno><cat>3</cat></book>
        <book><bk>munawir</bk><no>2</no><betaka>kamus indo arab</betaka><authno>2</authno><cat>4</cat></book>
        <book><bk>sidu</bk><no>3</no><betaka>kertas putih</betaka><authno>4</authno><cat>3</cat></book>
        </item>"""
        self.assertXmlEqual(expected, hasil)

    def test_buat_xml_objek_dengan_custom_root(self):
        """root selain item...."""
        hasil = CsvtoXml(self.original_csv_file())._make_xml_original(root='custom',
                                                                    parent='book')
        expected = """<custom>
        <book><bk>nama</bk><no>1</no><betaka>ini buku bagus</betaka><authno>1</authno><cat>3</cat></book>
        <book><bk>munawir</bk><no>2</no><betaka>kamus indo arab</betaka><authno>2</authno><cat>4</cat></book>
        <book><bk>sidu</bk><no>3</no><betaka>kertas putih</betaka><authno>4</authno><cat>3</cat></book>
        </custom>"""
        self.assertXmlEqual(expected, hasil)

    def test_buat_xml_objek_tapi_colom_tag_diubah_satu(self):
        hasil = CsvtoXml(self.original_csv_file())._make_xml_original(parent='book',
                col_name=[('bk', 'b')])
        expected = """<item>
        <book><b>nama</b><no>1</no><betaka>ini buku bagus</betaka><authno>1</authno><cat>3</cat></book>
        <book><b>munawir</b><no>2</no><betaka>kamus indo arab</betaka><authno>2</authno><cat>4</cat></book>
        <book><b>sidu</b><no>3</no><betaka>kertas putih</betaka><authno>4</authno><cat>3</cat></book>
        </item>"""
        self.assertXmlEqual(expected, hasil)

    def test_buat_xml_objek_tapi_colom_tag_diubah_satu_dengan_tanpa_parent(self):
        hasil = CsvtoXml(self.original_csv_file())._make_xml_original(col_name=[('bk', 'b')])
        expected = """<item>
        <b>nama</b><no>1</no><betaka>ini buku bagus</betaka><authno>1</authno><cat>3</cat>
        <b>munawir</b><no>2</no><betaka>kamus indo arab</betaka><authno>2</authno><cat>4</cat>
        <b>sidu</b><no>3</no><betaka>kertas putih</betaka><authno>4</authno><cat>3</cat>
        </item>"""
        self.assertXmlEqual(expected, hasil)
