import unittest
from lxml import etree
from io import StringIO

from mdb2kirtass.csv_to_xml import CsvtoXml


class CsvtoXmlTestCase(unittest.TestCase):

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
        expected = """<item><bk>nama</bk><no>1</no><betaka>ini buku bagus</betaka><authno>1</authno><cat>1</cat>
        <bk>munawir</bk><no>2</no><betaka>kamus indo arab</betaka><authno>2</authno><cat>4</cat>
        <bk>sidu</bk><no>3</no><betaka>kertas putih</betaka><authno>4</authno><cat>3</cat>
        </item>"""
        expected_xml = etree.fromstring(expected)
        self.assertEqual(etree.tostring(expected_xml),
                        etree.tostring(hasil._make_xml_original()))

    def test_get_headers(self):
        """Mendapatkan header csv"""
        hasil = CsvtoXml(self.original_csv_file())
        self.assertEqual(hasil._get_header(), ['bk', 'no', 'betaka', 'authno', 'cat'])
