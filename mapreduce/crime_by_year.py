from mrjob.job import MRJob
import csv
import io

class CrimeByYear(MRJob):

    def mapper(self, _, line):
        try:
            reader = csv.reader(io.StringIO(line))
            row = next(reader)
            if row[0] == 'ID':
                return
            year = row[17].strip()
            if year.isdigit():
                yield year, 1
        except:
            pass

    def reducer(self, key, values):
        yield key, sum(values)

if __name__ == '__main__':
    CrimeByYear.run()