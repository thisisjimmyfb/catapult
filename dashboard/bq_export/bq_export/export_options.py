# Copyright (c) 2020 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import datetime
import pytz

from apache_beam.options.pipeline_options import PipelineOptions


def _YesterdayUTC():
  return (datetime.datetime.utcnow() -
          datetime.timedelta(days=1)).strftime('%Y%m%d')


class BqExportOptions(PipelineOptions):

  @classmethod
  def _add_argparse_args(cls, parser):  # pylint: disable=invalid-name
    parser.add_argument(
        '--end_date',
        help=('Last day of data to export in YYYYMMDD format.  '
              'No value means yesterday.  Timezone is always UTC.'),
        default=_YesterdayUTC())
    parser.add_argument(
        '--num_days', help='Number of days data to export', type=int, default=1)

  def _EndAsDatetime(self):
    # pylint: disable=access-member-before-definition
    return datetime.datetime.strptime(
        self.end_date, '%Y%m%d').replace(tzinfo=pytz.UTC)

  def StartTime(self):
    # pylint: disable=access-member-before-definition
    return self.EndTime() - datetime.timedelta(days=self.num_days)

  def EndTime(self):
    # We want to include all the timestamps during the given day, so return a
    # timestamp at midnight of the _following_ day.
    return self._EndAsDatetime() + datetime.timedelta(days=1)
