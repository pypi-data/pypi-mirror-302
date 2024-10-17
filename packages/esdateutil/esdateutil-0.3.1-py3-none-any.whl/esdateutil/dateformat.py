#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utilities for handling Elasticsearch date strings and date math in Python.

Copyright (c) 2024, Matthew Murr
License: MIT (see LICENSE for details)
https://git.sr.ht/~murr/esdateutil
"""

# ES Implementation:
# - https://github.com/elastic/elasticsearch/blob/main/server/src/main/java/org/elasticsearch/common/time/DateFormatter.java
# - https://github.com/elastic/elasticsearch/blob/main/server/src/main/java/org/elasticsearch/common/time/DateFormatters.java
# ES Tests: https://github.com/elastic/elasticsearch/blob/main/server/src/test/java/org/elasticsearch/common/time/DateFormattersTests.java

#non-strict datetime equivalent:
#import java.time.LocalDate;
#import java.time.format.DateTimeFormatter;
#import java.time.format.DateTimeFormatterBuilder;
#import java.time.temporal.ChronoField;
#import java.time.format.ResolverStyle;
#import java.util.Locale;
#
#public class MyClass {
#  public static void main(String args[]) {
#    String text = "20154327";
#    DateTimeFormatter fmt = new DateTimeFormatterBuilder().appendValue(ChronoField.YEAR).parseDefaulting(ChronoField.MONTH_OF_YEAR, 1).parseDefaulting(ChronoField.DAY_OF_MONTH, 1).toFormatter(Locale.ROOT).withResolverStyle(ResolverStyle.STRICT);
#    LocalDate parsedDate = LocalDate.parse(text, fmt);
#    System.out.println(parsedDate.toString());
#  }
#}

# TODO For rounding up and down. These need to be funcs to deal with max day of month
#DATETIME_ROUND_DOWN = datetime(year=1970, month=1, day=1, hour=0, minute=0, second=0, microsecond=0, tzinfo=None)
#DATETIME_ROUND_UP =  datetime(year=1970, month=12, day=31, hour=24, minute=59, second=59, microsecond=999999, tzinfo=None)
#DATETIME_DEFAULT = DATETIME_ROUND_DOWN

import logging
from datetime import datetime, timedelta, timezone

LOG = logging.getLogger(__name__)

DATE_FORMATS = {}
def dateformat_fn(fn):
    DATE_FORMATS[fn.__name__] = fn
    return fn

# DateFormat Object APIs
class DateFormat:
    def __init__(self, fmt=None, separator="||"):
        """
        Initialises self.

        Takes an optional fmt and separator string.

        fmt can be a string of format strings separated by separator, or a list
        of format strings and/or functions that take a date string, tzinfo, and
        position integer and returns a datetime.

        A format string can be one of the formats defined in
        dateformat.DATE_FORMATS or a Python strptime format string.
        """
        self.fmt_fns = []
        self.fmt_names = []

        if not fmt:
            self.fmt_fns = [strict_date_optional_time, epoch_millis]
            self.fmt_names = ["strict_date_optional_time", "epoch_millis"]
            return

        if type(fmt) is str:
            fmt = fmt.split(separator)

        try:
            for elem in fmt:
                if type(elem) is str:
                    # TODO timezone handling. s can contain TZ information depending on
                    # format, check for none if format string and write to datetime
                    #lambda s, tzinfo, pos: datetime.strptime(s, fmt).replace(tzinfo=tzinfo)
                    fn = DATE_FORMATS.get(elem, lambda s, pos: datetime.strptime(s, elem))
                    self.fmt_fns.append(fn)
                    self.fmt_names.append(elem)
                elif callable(elem):
                    self.fmt_fns.append(elem)
                    self.fmt_names.append(elem.__name__)
                else:
                    raise TypeError("Bad type {} of element {}".format(type(elem), elem))
        except TypeError:
            raise TypeError("DateFormat cannot init - expected fmt to be string separated by separator ({}) or list of functions and/or strings. Instead got {}".format(fmt))

    def __repr__(self):
        return "DateFormat({})".format('||'.join(self.fmt_names))

    # def parse(self, s, tzinfo=None, pos=0):
    def parse(self, s, pos=0):
        failed = []
        for fmt_fn in self.fmt_fns:
            try:
                # TODO Function order of tzinfo and pos consistent across everything, even if not important
                #return fmt_fn(s, tzinfo=tzinfo, pos=pos)
                return fmt_fn(s, pos=pos)
            except ValueError as e:
                failed.append(e)
        # If we don't return, unable to parse.
        raise ValueError("Unable to parse date string {}: {}".format(s, failed))

# Internal Parse Functions
def _parse_num(s, strict_len=None, pos=0):
    if strict_len is not None and strict_len <= 0:
        raise ValueError("_parse_num: strict_len must be gte 0 or None. Received {}".format(strict_len))

    start = pos
    s_len = len(s)
    while pos < s_len and s[pos] >= '0' and s[pos] <= '9':
        pos += 1
        if strict_len is not None and strict_len < pos - start:
            raise ValueError("Exceeded strict length when parsing number in {} at [{},{}). Expected strict length of {}".format(s, start, pos, strict_len))
    if strict_len is not None and strict_len > pos - start:
        raise ValueError("Did not meet strict length when parsing number in {} at [{},{}). Expected strict length of {}, got {}".format(s, start, pos, strict_len, pos-start))

    num = int(s[start:pos])
    return pos, num

def _parse_fractional_num(s, fraction_len, pos=0):
    if fraction_len is None or fraction_len <= 0:
        raise ValueError("_parse_fractional_num: fraction_len must be gte 0 or None. Received {}".format(fraction_len))

    start = pos
    s_len = len(s)
    while pos < s_len and s[pos] >= '0' and s[pos] <= '9':
        pos += 1
        if pos - start > 9:
            raise ValueError("Exceeded maximum length (9) of a fractional second when parsing {} at [{},{}).".format(s, start, pos))

    if fraction_len < pos - start:
        end = start + fraction_len
    else:
        end = pos

    num = int(s[start:end]) * (10 ** (end - start))
    return pos, num

def _parse_t_timezone_offset_or_none(s, pos):
    s_len = len(s)
    tz_sign = 0
    if s[pos] == 'Z':
        pos += 1
        if s_len > pos:
            raise ValueError("Parsed timezone offset in {} but unparsed chars remain".format(s))
        return pos, timezone.utc
    elif s[pos] == '+':
        tz_sign = 1
    elif s[pos] == '-':
        tz_sign = -1
    else:
        return pos, None
    pos += 1

    strict_len = 2 # TODO TZ offset must always be 0 padded, strict does not affect
    pos, tz_hours = _parse_num(s, strict_len, pos)
    if tz_hours < 0 or tz_hours >= 24:
        raise ValueError("Timezone hours must be in [0,24) for string {}, got {}".format(s, tz_hours))
    if s_len <= pos:
        return pos, timezone(tz_sign * timedelta(hours=tz_hours))

    if s[pos] != ':':
        raise ValueError("Invalid character when parsing timezone at position {} in string {}: '{}'".format(pos, s, s[pos]))
    pos += 1

    strict_len = 2
    pos, tz_minutes = _parse_num(s, strict_len, pos)
    if tz_minutes < 0 or tz_hours >= 60:
        raise ValueError("Timezone minutes must be in [0,60) for string {}, got {}".format(s, tz_minutes))
    if s_len <= pos:
        return pos, timezone(tz_sign * timedelta(hours=tz_hours, minutes=tz_minutes))

    # TZ offset must always be at the end of the string.
    raise ValueError("Parsed timezone offset in {} but unparsed chars remain".format(s))

def _parse_date(s, *, strict=False, pos=0):
    strict_len = strict * 4 or None
    pos, year = _parse_num(s, strict_len, pos)
    s_len = len(s)
    if s_len <= pos:
        return pos, year, 1, 1

    if s[pos] != '-':
        raise ValueError("Unparsed characters when parsing date in {} at {}. Expected char '-', got '{}'".format(s, pos, s[pos]))
    pos += 1

    strict_len = strict * 2 or None
    pos, month = _parse_num(s, strict_len, pos)
    if s_len <= pos:
        return pos, year, month, 1

    if s[pos] != '-':
        raise ValueError("Unparsed characters when parsing date in {} at {}. Expected char '-', got '{}'".format(s, pos, s[pos]))
    pos += 1

    strict_len = strict * 2 or None
    pos, day = _parse_num(s, strict_len, pos)

    return pos, year, month, day

def parse_date(s, *, strict=False, pos=0):
    pos, year, month, day = _parse_date(s, strict=strict, pos=pos)
    if len(s) == pos:
        return datetime(year, month, day)

    raise ValueError("Unparsed characters when parsing date in {} at {}. Expected end of string, got '{}'".format(s, pos, s[pos]))

# TODO t_time and strict_t_time, time and strict_time, and their no_millis variants
def _parse_t_time(s, *, strict=False, pos=0, fraction_len=3):
    if s[pos] != 'T':
        raise ValueError("t_time must begin with T")
    pos += 1

    strict_len = strict * 2 or None
    pos, hour = _parse_num(s, strict_len, pos)
    s_len = len(s)
    if s_len <= pos:
        return pos, hour, 0, 0, 0, None

    # TODO from this point you can have a timezone offset after any value if it
    # is strict. If it is not strict, for some reason you need at least minutes.
    # TODO We could open a PR against ES for this lol
    pos, tzinfo = _parse_t_timezone_offset_or_none(s, pos)
    if tzinfo and strict:
        return pos, hour, 0, 0, 0, tzinfo
    elif tzinfo:
        raise ValueError("Elasticsearch has a cool bug where strict_date_optional_time allows a timezone offset after the hour value of a time, but date_optional_time does not. String: {}".format(s))

    if s[pos] != ':':
        raise ValueError("Unparsed characters when parsing time in {} at {}. Expected char ':', got '{}'".format(s, pos, s[pos]))
    pos += 1

    strict_len = strict * 2 or None
    pos, minute = _parse_num(s, strict_len, pos)
    if s_len <= pos:
        return pos, hour, minute, 0, 0, None

    pos, tzinfo = _parse_t_timezone_offset_or_none(s, pos)
    if tzinfo:
        return pos, hour, minute, 0, 0, tzinfo

    if s[pos] != ':':
        raise ValueError("Unparsed characters when parsing time in {} at {}. Expected char ':', got '{}'".format(s, pos, s[pos]))
    pos += 1

    strict_len = strict * 2 or None
    pos, second = _parse_num(s, strict_len, pos)
    if s_len <= pos:
        return pos, hour, minute, second, 0, None

    pos, tzinfo = _parse_t_timezone_offset_or_none(s, pos)
    if tzinfo:
        return pos, hour, minute, second, 0, tzinfo

    # NOTE ES doesn't document this but the behaviour of fractional seconds is
    # to allow any format of them but only take the top N digits when
    # calculating the value.
    if s[pos] != '.':
        raise ValueError("Unparsed characters when parsing time in {} at {}. Expected char '.', got '{}'".format(s, pos, s[pos]))
    pos += 1

    strict_len = None
    pos, micros = _parse_fractional_num(s, fraction_len, pos)
    if s_len <= pos:
        return pos, hour, minute, second, micros, None

    pos, tzinfo = _parse_t_timezone_offset_or_none(s, pos)
    if tzinfo:
        return pos, hour, minute, second, micros, tzinfo

# TODO Allow tzinfo arg in parse_date, parse_t_time, and parse_date_optional_time.
# TODO Also ignore in date string option, to choose what timestamp can be where both specified
def parse_date_optional_time(s, *, strict=False, pos=0, fraction_len=3):
    pos, year, month, day = _parse_date(s, strict=strict, pos=pos)
    s_len = len(s)
    if pos == s_len:
        return datetime(year, month, day)

    pos, hour, minute, second, micros, tzinfo = _parse_t_time(s, strict=strict, pos=pos, fraction_len=fraction_len)
    if pos >= s_len:
        return datetime(year, month, day, hour, minute, second, micros, tzinfo=tzinfo)

    raise ValueError("Unparsed characters when parsing date optional time in {} at {}. Expected end of string, got '{}'".format(s, pos, s[pos]))

# Dateformat Named Funcs
@dateformat_fn
def strict_date(s, pos=0):
    return parse_date(s, strict=True, pos=pos)

@dateformat_fn
def date(s, pos=0):
    return parse_date(s, strict=False, pos=pos)

@dateformat_fn
def strict_date_optional_time(s, *, pos=0):
    return parse_date_optional_time(s, strict=True, pos=pos)

@dateformat_fn
def date_optional_time(s, *, pos=0):
    return parse_date_optional_time(s, strict=False, pos=pos)

@dateformat_fn
def strict_date_optional_time_nanos(s, *, pos=0):
    LOG.warning("As Python has microsecond precision in datetime objects, it can't handle all nanosecond precision timestamps. Therefore, we only handle the first 6 digits of a fractional time in strict_date_optional_time_nanos")
    return parse_date_optional_time(s, strict=True, pos=pos, fraction_len=6)

@dateformat_fn
def epoch_millis(s, *, pos=0, tzinfo=None):
    epoch_s = s[pos:pos+13]
    epoch = int(epoch_s)/1000
    return datetime.fromtimestamp(epoch, tz=tzinfo)

@dateformat_fn
def epoch_second(s, *, pos=0, tzinfo=None):
    epoch_s = s[pos:pos+10]
    epoch = int(epoch_s)
    return datetime.fromtimestamp(epoch, tz=tzinfo)

if __name__ == "__main__":
    print(DATE_FORMATS)
    parser = None
    for strict in True, False:
        parser = DateFormat("{}date_optional_time".format('strict_' if strict else ''))
        print("Parser:", parser)
        for s in ["2024", "2024-04", "2024-04-11", "2024-04-11T14", "2024-04-11T14:02", "2024-04-11T14:02:29", "2024-04-11T14:02:29.123", "2024-04-11T14:02:29.123456", "2024-04-11T14:02:29.123456789Z",  "2024-04-11T14:02:29.1234+05:30", "2024-04-11T14:02:29Z", "2024-04-11T14:02+01:00",  "2024-04-11T14Z"]:
            print(s)
            #print(parse_date_optional_time(s, strict=strict))
            print(parser.parse(s))
