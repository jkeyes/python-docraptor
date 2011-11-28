# Copyright (C) 2011 John Keyes
# http://jkeyes.mit-license.org/

import os
from os import path
from . import pdf
from . import xls
from unittest import TestCase

TEST = "test.pdf"
TEST_NAME = "test_name.pdf"
FILES = [TEST, TEST_NAME]

KEY = os.environ.get('DOCRAPTOR_KEY', None)

def _clean():
    for fname in FILES:
        if path.exists(fname):
            os.unlink(fname)

class PDFTest(TestCase):

    def setUp(self):
        _clean()

    def tearDown(self):
        _clean()

    def test_pdf(self):
        assert not path.exists(TEST)
        pdf(KEY,
            { 'doc[test]': 'true',
              'doc[name]': TEST,
              'doc[document_content]': "<html><body><h1>Test</h1></body></html>"})
        assert path.exists("test.pdf")

    def test_ssl(self):
        assert not path.exists(TEST)
        pdf(KEY,
            { 'doc[test]': 'true',
              'doc[name]': TEST,
              'doc[document_content]':"<html><body><h1>Test</h1></body></html>"},
            ssl=True)
        assert path.exists("test.pdf")

    def test_name(self):
        assert not path.exists(TEST)
        assert not path.exists(TEST_NAME)
        tnf = open("test_name.pdf", "w")
        pdf(KEY,
            { 'doc[test]': 'true',
              'doc[name]': "test.pdf",
              'doc[document_content]':"<html><body><h1>Test</h1></body></html>"},
            output_file=tnf,
            ssl=True)
        assert not path.exists(TEST)
        assert path.exists(TEST_NAME)

    def test_content_or_url_required(self):
        try:
            pdf(KEY,
                'doc[test]': "true",
                'doc[name]': "test"
                )
        except DocRaptorError, e:
            assert e.message == "Must provide a document url or document content"
