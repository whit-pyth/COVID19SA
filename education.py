import logging
import csv
import argparse
import os
import sys
import apache_beam as beam

from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io import ReadFromText
from datetime import datetime

class Printer(beam.DoFn):
    def process(self,element):
        print(element)

class TypeOf(beam.DoFn):
    def process(self,element):
        print(type(element))

def parse_clean_transform_file(element):
    for line in csv.reader([element], quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True):
        if line[3].strip() != 'Hong Kong Special Administrative Region' and \
                line[3].strip() != 'Macao Special Administrative Region':
            d = {'date': datetime.strptime((line[0]), '%d/%m/%Y').strftime('%Y-%m-%d %H:%M:%S'),
                 'iso': (line[1]).strip(), 'country_1': (line[2]).strip(), 'scale': (line[3]).strip(),
                 'note': (line[4]).strip()}
            return d


def run(argv=None):

    # Initiate the pipeline
    p = beam.Pipeline(options=PipelineOptions())

    data_from_source = (p
                        | 'Read File' >> ReadFromText('input/covid_impact_education.csv', skip_header_lines=1)
                        | 'Parse, clean and transform CSV' >> beam.Map(parse_clean_transform_file)
                        #| 'Splitter using beam.Map' >> beam.Map(lambda record:(record.split(',')))
                        #| 'Splitter using beam.Map' >> beam.Map(lambda record:(record.split(','))[0])
                        | 'Print the data' >> beam.ParDo(Printer())
                        )

    table_schema = 'date:TIMESTAMP, iso:STRING, country:STRING, scale:STRING, note:STRING'
    table_spec = 'my-storage-209112:covid19_2.education'

    # Persist to BigQuery
    # WriteToBigQuery accepts the data as list of JSON objects
    data_from_source | 'Write' >> beam.io.WriteToBigQuery(
        table_spec,
        schema=table_schema,
        create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
        write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
        batch_size=int(1000)
    )

    p.run().wait_until_finish()


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
