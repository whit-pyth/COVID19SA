import logging
import csv
import argparse
import os
import sys
import apache_beam as beam

from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io import ReadFromText
from datetime import datetime

# Print it! see the data...
class Printer(beam.DoFn):
    def process(selfself,element):
        print(element)

# Return type for element(s)
class TypeOf(beam.DoFn):
    def process(self,element):
        print(type(element))

# Parse, clean and transform CSV; quote all, strip, assign data type, convert list to dict...
def parse_clean_transform_file(element):
    for line in csv.reader([element], quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True):
        d = {'case_type': (line[0]).strip(), 'cases': int(line[1]), 'difference': int(line[2]),
             'date': datetime.strptime((line[3]), '%m/%d/%Y').strftime('%Y-%m-%d %H:%M:%S'),
             'country_region': (line[4]).strip(), 'province_state': (line[5]).strip() or 'N/A',
             'admin2': (line[6]).strip() or 'N/A', 'combined_key': (line[7]).strip() or 'N/A',
             'fips': (line[8]).strip() or 'N/A', 'lat': float(line[9] or 0.0), 'long': float(line[10] or 0.0)}
        return d

def run(argv=None):

    # Initiate the pipeline
    p = beam.Pipeline(options=PipelineOptions())

    data_from_source = (p
                        | 'Read File' >> ReadFromText('input/COVID-19-Cases.csv', skip_header_lines=1)
                        | 'Parse, clean and transform CSV' >> beam.Map(parse_clean_transform_file)
                        | 'Print data' >> beam.ParDo(Printer())
                        )


    # table_schema = 'case_type:STRING, cases:INTEGER, difference:INTEGER, date:TIMESTAMP, country_region:STRING, ' \
    #                'province_state:STRING, admin2:STRING, combined_key:STRING, fips:STRING, lat:FLOAT, long:FLOAT'
    # table_spec = 'my-storage-209112:covid19_2.cases2'


    # # Persist to BigQuery
    # # WriteToBigQuery accepts the data as list of JSON objects
    # data_from_source | 'Write' >> beam.io.WriteToBigQuery(
    #     table_spec,
    #     schema=table_schema,
    #     create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
    #     write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
    #     batch_size=int(1000)
    # )


    p.run().wait_until_finish()


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
