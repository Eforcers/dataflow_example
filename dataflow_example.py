# sudo pip install google-cloud-dataflow
# google-api-python-client
# https://beam.apache.org/documentation/programming-guide/
# https://github.com/apache/beam/blob/master/sdks/python/apache_beam/examples/complete/game/hourly_team_score.py

import sys
import os
sys.path.insert(1, os.path.join(os.path.dirname(__file__), 'lib'))

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import GoogleCloudOptions
from apache_beam.options.pipeline_options import StandardOptions

options = PipelineOptions()
google_cloud_options = options.view_as(GoogleCloudOptions)
google_cloud_options.project = '<project-name>'#project-name
google_cloud_options.job_name = 'myjob14'#job name
google_cloud_options.staging_location = 'gs://<bucket>/staging' #replace <bucket> for bucket name
google_cloud_options.temp_location = 'gs://<bucket>/temp'#replace <bucket> for bucket name
options.view_as(StandardOptions).runner = 'DataflowRunner'


def count(word):
    return [len(word)]


class Count2(beam.PTransform):
  def expand(self, pcoll):
    # transform logic goes here
    salida = (pcoll | "count 22" >> beam.ParDo(count))
    return (pcoll | "count 23" >> beam.ParDo(count))


def suma(val):
    return sum(val)

p = beam.Pipeline(options=options)

words = "asdf asdf asdf asdf asdf asdf"
lines = p | 'create words' >> beam.Create(words.split(" "))

result = lines | 'count words' >> beam.ParDo(count) \
 | 'sum' >> beam.CombineGlobally(suma) \
 | 'save' >> beam.io.WriteToText('gs://cp001/salida.txt')

result = lines | 'count words2' >> Count2() \
 | 'sum2' >> beam.CombineGlobally(suma) \
 | 'save2' >> beam.io.WriteToText('gs://cp001/salida2.txt')


p.run()
