from lxml import etree
import csv

class CsvtoXml(object):
    """Class untuk mengubah file csv ke file xml
    berdasarkan nama kolom....


    csv_file : file csv, atau yang semisal dengan file (dengan StringIO)?
    """

    def __init__(self, csv_file):
        self.csv_file = csv_file


    def _dict_csv(self):
        """Fungsi untuk mengubah file csv ke objek DictCsvReader"""
        return csv.DictReader(self.csv_file)

    def _make_xml_original(self, root='item', parent=None):
        item = etree.Element(root)
        for row in self._dict_csv():
            if not parent:
                for col in row:
                    t = etree.SubElement(item, col)
                    t.text = row[col]
            else:
                p = etree.SubElement(item, parent)
                for col in row:
                    t = etree.SubElement(p, col)
                    t.text = row[col]

        return item
