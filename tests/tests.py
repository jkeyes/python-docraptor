# Copyright (C) 2011 John Keyes
# http://jkeyes.mit-license.org/

import os
from os import path
from docraptor import DocRaptor
from docraptor import DocumentCreationFailure
from docraptor import DocumentStatusFailure
from docraptor import DocumentListingFailure
from docraptor import DocumentDownloadFailure
from docraptor import NoApiKeyProvidedError
from docraptor import NoContentError
import requests
from unittest import TestCase
from nose.tools import raises

TEST = "test.pdf"
TEST_NAME = "test_name.pdf"
FILES = [TEST, TEST_NAME]
DIRPATH = os.path.dirname(__file__)
FIXTURES = {}


def _clean():
    for fname in FILES:
        if path.exists(fname):
            os.unlink(fname)


class MockResponse(object):
    pass


def stub_http_response_with(filename, method=None, status=None):
    if status is None:
        status = 200
    try:
        # python 2
        with open(os.path.join(DIRPATH, 'fixtures', filename), "r") as f:
            content = f.read()
    except UnicodeDecodeError:
        # python 3
        with open(os.path.join(DIRPATH, 'fixtures', filename), "r", encoding="latin-1") as f:
            content = f.read()
    FIXTURES[filename] = content

    def stubbed(*args, **kwargs):
        resp = MockResponse()
        resp.status_code = status
        resp.content = content
        return resp
    setattr(requests, method, stubbed)


class DocRaptorApiKeyTest(TestCase):

    def setUp(self):
        os.environ.pop('DOCRAPTOR_API_KEY', None)
        self.test_key = "test key"

    @raises(NoApiKeyProvidedError)
    def test_api_keys(self):
        docraptor = DocRaptor()

    def test_env_api_key(self):
        os.environ['DOCRAPTOR_API_KEY'] = self.test_key
        docraptor = DocRaptor()
        assert docraptor.api_key == self.test_key

    def test_no_overwrite_env_api_key(self):
        os.environ['DOCRAPTOR_API_KEY'] = self.test_key
        docraptor = DocRaptor()

        os.environ['DOCRAPTOR_API_KEY'] = "blah"
        assert docraptor.api_key == self.test_key

    def test_param_api_keys(self):
        docraptor = DocRaptor(self.test_key)
        assert docraptor.api_key == self.test_key


class DocRaptorCreateTest(TestCase):
    def setUp(self):
        self.test_key = "test key"

    @raises(AttributeError)
    def test_bogus_arguments_bool(self):
        DocRaptor(self.test_key).create(True)

    @raises(ValueError)
    def test_bogus_arguments_none(self):
        DocRaptor(self.test_key).create(None)

    @raises(NoContentError)
    def test_no_content_empty(self):
        DocRaptor(self.test_key).create({})

    @raises(NoContentError)
    def test_no_content_attr(self):
        DocRaptor(self.test_key).create({'herped': 'the_derp'})

    @raises(NoContentError)
    def test_blank_content(self):
        DocRaptor(self.test_key).create({ 'content': ''})

    @raises(NoContentError)
    def test_blank_url(self):
        DocRaptor(self.test_key).create({'url': ''})

    @raises(requests.exceptions.Timeout)
    def test_timeout(self):
        os.environ['DOCRAPTOR_TIMEOUT'] = '0.0001'
        resp = DocRaptor(self.test_key).create({'document_content': "<html><body>Hey</body></html>" })


class DocRaptorDocumentContentTest(TestCase):
    def setUp(self):
        self.test_key = "test key"
        self.html_content = "<html><body>Hey</body></html>"

    def test_create_with_invalid_content(self):
        invalid_html = "<herp"
        stub_http_response_with("invalid_pdf", "post", 422)
        resp = DocRaptor(self.test_key).create({'document_content': invalid_html })
        assert FIXTURES["invalid_pdf"] == resp.content
        assert 422 == resp.status_code

    @raises(DocumentCreationFailure)
    def test_create_with_invalid_content_raises(self):
        invalid_html = "<herp"
        stub_http_response_with("invalid_pdf", "post", 422)
        resp = DocRaptor(self.test_key).create({'document_content': invalid_html, 'raise_exception_on_failure': True })

    def test_create_with_valid_content(self):
        stub_http_response_with("simple_pdf", "post")
        resp = DocRaptor(self.test_key).create({'document_content': self.html_content })
        assert FIXTURES["simple_pdf"] == resp.content
        assert 200 == resp.status_code


class DocRaptorListDocsTest(TestCase):
    def setUp(self):
        self.test_key = "test key"

    @raises(AttributeError)
    def test_bogus_arguments_bool(self):
        DocRaptor(self.test_key).list_docs(True)

    @raises(ValueError)
    def test_bogus_arguments_None(self):
        DocRaptor(self.test_key).list_docs(None)

    @raises(DocumentListingFailure)
    def test_invalid_list_docs_raises(self):
        stub_http_response_with("invalid_list_docs", "get", 400)
        resp = DocRaptor(self.test_key).list_docs({'raise_exception_on_failure': True})

    def test_list_docs(self):
        stub_http_response_with("simple_list_docs", "get")
        resp = DocRaptor(self.test_key).list_docs({})
        assert FIXTURES["simple_list_docs"] == resp.content


class DocRaptorStatusTest(TestCase):
    def setUp(self):
        self.test_key = "test key"

    def test_invalid_status(self):
        stub_http_response_with("invalid_status", "get", 403)
        resp = DocRaptor(self.test_key).status("test-id")
        assert FIXTURES["invalid_status"] == resp.content
        assert 403 == resp.status_code

    @raises(DocumentStatusFailure)
    def test_invalid_status_raises(self):
        stub_http_response_with("invalid_status", "get", 400)
        resp = DocRaptor(self.test_key).status("test-id", True)

    def atest_status(self):
        stub_http_response_with("simple_status", "get")
        resp = DocRaptor(self.test_key).status("test-id")
        assert "completed" == resp['status']


class DocRaptorDownloadTest(TestCase):
    def setUp(self):
        self.test_key = "test key"

    def test_invalid_download(self):
        stub_http_response_with("invalid_download", "get", 400)
        resp = DocRaptor(self.test_key).download("test-id")
        assert FIXTURES["invalid_download"] == resp.content
        assert 400 == resp.status_code

    @raises(DocumentDownloadFailure)
    def test_invalid_download_raises(self):
        stub_http_response_with("invalid_download", "get", 400)
        resp = DocRaptor(self.test_key).download("test-id", True)

    def test_download(self):
        stub_http_response_with("simple_download", "get")
        resp = DocRaptor(self.test_key).download("test-id")
        assert FIXTURES["simple_download"] == resp.content
