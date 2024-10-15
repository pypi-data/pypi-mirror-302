# -*- coding: utf-8 -*-
import csv
from codecs import iterencode
from decimal import Decimal, InvalidOperation
from itertools import chain

import six
from ckan.plugins.toolkit import asbool
from dateutil.parser import isoparser, parser
from dateutil.parser import ParserError

from tabulator import helpers
from tabulator.parser import Parser

from ckan.plugins.toolkit import config

CSV_SAMPLE_LINES = 100


class XloaderCSVParser(Parser):
    """Extends tabulator CSVParser to detect datetime and numeric values.
    """

    # Public

    options = [
        'delimiter',
        'doublequote',
        'escapechar',
        'quotechar',
        'quoting',
        'skipinitialspace',
        'lineterminator'
    ]

    def __init__(self, loader, force_parse=False, **options):
        super(XloaderCSVParser, self).__init__(loader, force_parse, **options)
        # Set attributes
        self.__loader = loader
        self.__options = options
        self.__force_parse = force_parse
        self.__extended_rows = None
        self.__encoding = None
        self.__dialect = None
        self.__chars = None

    @property
    def closed(self):
        return self.__chars is None or self.__chars.closed

    def open(self, source, encoding=None):
        # Close the character stream, if necessary, before reloading it.
        self.close()
        self.__chars = self.__loader.load(source, encoding=encoding)
        self.__encoding = getattr(self.__chars, 'encoding', encoding)
        if self.__encoding:
            self.__encoding.lower()
        self.reset()

    def close(self):
        if not self.closed:
            self.__chars.close()

    def reset(self):
        helpers.reset_stream(self.__chars)
        self.__extended_rows = self.__iter_extended_rows()

    @property
    def encoding(self):
        return self.__encoding

    @property
    def dialect(self):
        if self.__dialect:
            dialect = {
                'delimiter': self.__dialect.delimiter,
                'doubleQuote': self.__dialect.doublequote,
                'lineTerminator': self.__dialect.lineterminator,
                'quoteChar': self.__dialect.quotechar,
                'skipInitialSpace': self.__dialect.skipinitialspace,
            }
            if self.__dialect.escapechar is not None:
                dialect['escapeChar'] = self.__dialect.escapechar
            return dialect

    @property
    def extended_rows(self):
        return self.__extended_rows

    # Private

    def __iter_extended_rows(self):

        def type_value(value):
            """Returns numeric values as Decimal(). Uses dateutil to parse
            date values. Otherwise, returns values as it receives them
            (strings).
            """
            if value in ('', None):
                return ''

            try:
                return Decimal(value)
            except InvalidOperation:
                pass

            try:
                i = isoparser()
                return i.isoparse(value)
            except ValueError:
                pass

            try:
                p = parser()
                yearfirst = asbool(config.get(
                    'ckanext.xloader.parse_dates_yearfirst', False))
                dayfirst = asbool(config.get(
                    'ckanext.xloader.parse_dates_dayfirst', False))
                return p.parse(value, yearfirst=yearfirst, dayfirst=dayfirst)
            except ParserError:
                pass

            return value

        sample, dialect = self.__prepare_dialect(self.__chars)
        items = csv.reader(chain(sample, self.__chars), dialect=dialect)
        for row_number, item in enumerate(items, start=1):
            values = []
            for value in item:
                value = type_value(value)
                values.append(value)
            yield row_number, None, list(values)

    def __prepare_dialect(self, stream):

        # Get sample
        sample = []
        while True:
            try:
                sample.append(next(stream))
            except StopIteration:
                break
            if len(sample) >= CSV_SAMPLE_LINES:
                break

        # Get dialect
        try:
            separator = ''
            delimiter = self.__options.get('delimiter', ',\t;|')
            dialect = csv.Sniffer().sniff(separator.join(sample), delimiter)
            if not dialect.escapechar:
                dialect.doublequote = True
        except csv.Error:
            class dialect(csv.excel):
                pass
        for key, value in self.__options.items():
            setattr(dialect, key, value)
        # https://github.com/frictionlessdata/FrictionlessDarwinCore/issues/1
        if getattr(dialect, 'quotechar', None) == '':
            setattr(dialect, 'quoting', csv.QUOTE_NONE)

        self.__dialect = dialect
        return sample, dialect
