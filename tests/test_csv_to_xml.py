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
