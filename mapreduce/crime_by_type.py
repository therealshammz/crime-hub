from mrjob.job import MRJob
import csv
import io

class CrimeByType(MRJob):

    def mapper(self, _, line):
        try:
            reader = csv.reader(io.StringIO(line))
            row = next(reader)
            if row[0] == 'ID':  # skip header
                return
            primary_type = row[5].strip()
            if primary_type:
                yield primary_type, 1
        except:
            pass

    def reducer(self, key, values):
        yield key, sum(values)

if __name__ == '__main__':
    CrimeByType.run()