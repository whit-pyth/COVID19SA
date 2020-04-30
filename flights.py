from __future__ import absolute_import
import logging
import argparse
import os
import sys
import apache_beam as beam

from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io import ReadFromText
from datetime import datetime
from apache_beam.options.pipeline_options import PipelineOptions, GoogleCloudOptions, SetupOptions


class Printer(beam.DoFn):
    def process(selfself, element):
        print(element)

class TypeOf(beam.DoFn):
    def process(self,element):
        print(type(element))

class ParseCleanTransformCSV(beam.DoFn):
    def process(self,element):
        date, seven_day_moving_average, number_of_flights = element.split(',')
        date = date.strip('"')
        date = datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')
        return [{'date': date,
                 'seven_day_moving_average': int(seven_day_moving_average),
                 'number_of_flights': int(number_of_flights)}]


def run(argv=None):

    # Initiate the pipeline
    p = beam.Pipeline(options=PipelineOptions())

    data_from_source = (p
                        | 'Read File' >> ReadFromText('input/total-number-of-flights.csv', skip_header_lines=1)
                        | 'Parse clean and transform CSV' >> beam.ParDo(ParseCleanTransformCSV())
                        #| 'Print data' >> beam.ParDo(Printer())
                        )


    table_schema = 'date:TIMESTAMP, seven_day_moving_average:INTEGER, number_of_flights:INTEGER'

    #table_spec = 'my-storage-209112:covid19_2.flights'
    table_spec = 'sa-pipeline-bakeoff:covid19.flights_sf'

    # Persist to BigQuery
    # WriteToBigQuery accepts the data as list of JSON objects
    data_from_source | 'Write' >> beam.io.WriteToBigQuery(
        table_spec,
        schema=table_schema,
        create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
        write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
        batch_size=int(100)
    )


    p.run().wait_until_finish()


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
