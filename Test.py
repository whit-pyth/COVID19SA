import logging
import argparse
import os
import sys
import apache_beam as beam

from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io import ReadFromText
from datetime import datetime

