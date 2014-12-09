import types
import socket
import unittest
import datetime
import uuid

import taskcluster.utils as subject
import mock

import base


# https://docs.python.org/2/library/datetime.html#tzinfo-objects
class UTC(datetime.tzinfo):
  """UTC"""

  def utcoffset(self, dt):
      return datetime.timedelta(0)

  def tzname(self, dt):
      return 'UTC'

  def dst(self, dt):
      return datetime.timedelta(0)

utc = UTC()

class StringDateTests(base.TCTest):
  def test_naive(self):
    dateObj = datetime.datetime(
      year=2000,
      month=1,
      day=1,
      hour=1,
      minute=1,
      second=1
    )
    expected = '2000-01-01T01:01:01Z'
    actual = subject.stringDate(dateObj)
    self.assertEqual(expected, actual)

  def test_aware(self):
    dateObj = datetime.datetime(
      year=2000,
      month=1,
      day=1,
      hour=1,
      minute=1,
      second=1,
      tzinfo=utc
    )
    expected = '2000-01-01T01:01:01Z'
    actual = subject.stringDate(dateObj)
    self.assertEqual(expected, actual)


class DumpJsonTests(base.TCTest):
  def test_has_no_spaces(self):
    expected = '{"test":"works","doesit":"yes"}'
    actual = subject.dumpJson({'test': 'works', 'doesit': 'yes'})
    self.assertEqual(expected, actual)

  def test_serializes_naive_date(self):
    dateObj = datetime.datetime(
      year=2000,
      month=1,
      day=1,
      hour=1,
      minute=1,
      second=1
    )
    expected = '{"date": "2000-01-01T01:01:01Z"}'
    actual = subject.dumpJson({'date': dateObj})

  def test_serializes_aware_date(self):
    dateObj = datetime.datetime(
      year=2000,
      month=1,
      day=1,
      hour=1,
      minute=1,
      second=1,
      tzinfo=utc
    )
    expected = '{"date": "2000-01-01T01:01:01Z"}'
    actual = subject.dumpJson({'date': dateObj})


class TestBase64Utils(base.TCTest):
  def test_encode_string_for_b64_header(self):
    # Really long strings trigger newlines every 72 ch
    expected = 'YWJjZGVm' * 500
    actual = subject.encodeStringForB64Header('abcdef' * 500)
    self.assertEqual(expected, actual)

  def test_makeb64urlsafe(self):
    expected = '-_'
    actual = subject.makeB64UrlSafe('+/')
    self.assertEqual(expected, actual)

  def test_makeb64urlunsafe(self):
    expected = '+/'
    actual = subject.makeB64UrlUnsafe('-_')
    self.assertEqual(expected, actual)

class TestSlugId(base.TCTest):
  def test_slug_id(self):
    with mock.patch('uuid.uuid4') as p:
      p.return_value = uuid.UUID('bed97923-7616-4ec8-85ed-4b695f67ac2e')
      expected = 'vtl5I3YWTsiF7UtpX2esLg'
      actual = subject.slugId()
      self.assertEqual(expected, actual)
