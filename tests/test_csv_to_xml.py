import unittest
from lxml import etree
from io import StringIO


class CsvtoXmlTestCase(unittest.TestCase):

    def original_csv_file(self):
        return StringIO("""bk, no, betaka, authno, cat
        nama, 1, ini buku bagus, 1, 3
        munawir, 2, kamus indo arab, 2, 4
        sidu, 3, kertas putih, 4, 3""")

    
