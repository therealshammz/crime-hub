from mrjob.job import MRJob
import csv
import io

class ArrestRate(MRJob):

    def mapper(self, _, line):
        try:
            reader = csv.reader(io.StringIO(line))
            row = next(reader)
            if row[0] == 'ID':
                return
            primary_type = row[5].strip()
            arrest = 1 if row[8].strip().lower() == 'true' else 0
            if primary_type:
                yield primary_type, (1, arrest)
        except:
            pass

    def reducer(self, key, values):
        total, arrests = 0, 0
        for count, arrest in values:
            total += count
            arrests += arrest
        rate = round((arrests / total) * 100, 2) if total > 0 else 0
        yield key, {'total': total, 'arrests': arrests, 'arrest_rate_%': rate}

if __name__ == '__main__':
    ArrestRate.run()