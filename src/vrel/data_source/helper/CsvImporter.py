import csv
from vrel.entity.Relation import Parameter, Relation
from vrel.interface.SomeDataSource import SomeDataSource


class CsvImporter:
    def import_table_from_file(self, table_name: str, file_path: str, data_source: SomeDataSource):
        with open(file_path) as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            line = 0
            headers = []
            for row in reader:
                if len(row) == 0:
                    continue
                line += 1
                if line == 1:
                    headers = row
                else:
                    values = []
                    for header, element in zip(headers, row):
                        values.append(element)

                    relation = Relation(table_name, [Parameter(header, header) for i, header in enumerate(headers)])
                    data_source.insert(relation, headers, values)
