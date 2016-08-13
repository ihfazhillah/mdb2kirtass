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
