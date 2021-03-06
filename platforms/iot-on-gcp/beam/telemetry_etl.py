from __future__ import absolute_import

import argparse
import logging
import json
from sets import Set

import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText

from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.options.pipeline_options import StandardOptions
from apache_beam.io import BigQueryDisposition

import time
import calendar
import strict_rfc3339


# TODO
'''
telemetry_etl.py", line 28, in process
null_resource.beam-staging (local-exec):   File "/usr/local/lib/python2.7/dist-packages/strict_rfc3339.py", line 83, in rfc3339_to_timestamp
null_resource.beam-staging (local-exec):     if not validate_rfc3339(datestring):
null_resource.beam-staging (local-exec):   File "/usr/local/lib/python2.7/dist-packages/strict_rfc3339.py", line 42, in validate_rfc3339
null_resource.beam-staging (local-exec):     m = rfc3339_regex.match(datestring)
null_resource.beam-staging (local-exec): TypeError: expected string or buffer [while running 'generatedPtransform-1953']
'''
# TODO
# BQ schema change from timestamp to int


# Set event timestamp from json body
class AddTimestampToDict(beam.DoFn):
    def process(self, element):
        logging.debug('AddTimestampToDict: %s %r' % (type(element), element))
        return [beam.window.TimestampedValue(
            element,
            strict_rfc3339.rfc3339_to_timestamp(element['timestamp']))]


# Emit as KV with the clientid as key
class AddKeyToDict(beam.DoFn):
    def process(self, element):
        logging.debug('AddKeyToDict: %s %r' % (type(element), element))
        return [(element['device'], element)]


# BigQuery table schemas
class Schema(object):
    @staticmethod
    def get_warehouse_schema():
        schema_str = ('timestamp:TIMESTAMP, '
                      'device:STRING, '
                      'temperature:FLOAT ')
        return schema_str

# Aggregate for each metric in the window
class CountAverages(beam.DoFn):
    def process(self, element):
        logging.info('CountAverages start: %s %r' % (type(element), element))
        stat_names = ["temperature"]

        avg_e = {}
        aggr = {}
        for k in stat_names:
            aggr[k] = (0, 0)

        avg_e['device'] = element[0]
        avg_e['timestamp'] = strict_rfc3339.now_to_rfc3339_localoffset()

        # Emit sum and count for each metric
        for elem_map in element[1]:
            for key in stat_names:
                if key in elem_map:
                    value = elem_map[key]
                    aggr[key] = (aggr[key][0] + value, aggr[key][1] + 1)

        # Calculate average and set in return map
        for key, value in aggr.iteritems():
            if value[1] == 0:
                avg_e[key] = 0
            else:
                avg_e[key] = value[0] / value[1]
        logging.info('CountAverages end: {}'.format(avg_e))

        return [avg_e]


def run(argv=None):
    """Build and run the pipeline."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--stream',
        type=str,
        help='Pub/Sub topic to read from')
    parser.add_argument(
        '--sink',
        help=(
            'Output BigQuery table for windowed averages specified as: '
            'PROJECT:DATASET.TABLE or DATASET.TABLE.'))

    args, pipeline_args = parser.parse_known_args(argv)

    options = PipelineOptions(pipeline_args)
    options.view_as(SetupOptions).save_main_session = True
    options.view_as(StandardOptions).streaming = True

    p = beam.Pipeline(options=options)

    records = (p | 'Read from PubSub' >> beam.io.ReadFromPubSub(
        topic=args.stream) | 'Parse JSON to Dict' >> beam.Map(
            json.loads))

    
    """
            # Write to the warehouse table
    records | 'Write to BigQuery' >> beam.io.WriteToBigQuery(
        args.sink,
        schema=Schema.get_warehouse_schema(),
        create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
        write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND)

    """

    # Compute average in a sliding window and write to BQ average table
    (records | 'Add timestamp' >> beam.ParDo(AddTimestampToDict()) |
     'Window' >> beam.WindowInto(beam.window.SlidingWindows(
         10, 1, offset=0)) |
     'Dict to KeyValue' >> beam.ParDo(AddKeyToDict()) |
     'Group by Key' >> beam.GroupByKey() |
     'Average' >> beam.ParDo(CountAverages()) |
     'Write Avg to BigQuery' >> beam.io.WriteToBigQuery(
         args.sink,
         schema=Schema.get_warehouse_schema(),
         create_disposition=BigQueryDisposition.CREATE_IF_NEEDED,
         write_disposition=BigQueryDisposition.WRITE_APPEND))

    result = p.run()
    result.wait_until_finish()


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
