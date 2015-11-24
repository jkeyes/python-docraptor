# Copyright (C) 2011 John Keyes
# http://jkeyes.mit-license.org/

"""
Simple wrapper for Doc Raptor API.
"""
import json
import os
import re
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime

ENV = os.environ
API_KEY = "DOCRAPTOR_API_KEY"
URL = "DOCRAPTOR_URL"
DEFAULT_TIMEOUT = 80 #seconds
TIMEOUT = "DOCRAPTOR_TIMEOUT"

# endpoint URLs
HTTPS_URL = 'https://docraptor.com/'

class NoApiKeyProvidedError(RuntimeError):
    pass
    
class NoContentError(KeyError):
    pass

class DocRaptorRequestException(Exception):
    def __init__(self, message, status_code):
        super(DocRaptorRequestException, self).__init__(message)
        self.status_code = status_code

    def __str__(self):
        return "%s\nHTTP Status: %s\nReturned: %s" % (self.__class__.__name__, self.status_code, self.message)

class DocumentCreationFailure(DocRaptorRequestException):
    pass

class DocumentListingFailure(DocRaptorRequestException):
    pass

class DocumentStatusFailure(DocRaptorRequestException):
    pass

class DocumentDownloadFailure(DocRaptorRequestException):
    pass

class DocRaptor(object):

    def __init__(self, api_key=None):
        self.api_key = ENV.get(API_KEY) if api_key is None else api_key
        if not self.api_key:
            raise NoApiKeyProvidedError("No API key provided")
        self._url = ENV.get(URL, HTTPS_URL)
        self._timeout = float(ENV.get(TIMEOUT, DEFAULT_TIMEOUT))

    def create(self, options=None):
        if options is None:
            raise ValueError("Please pass in an options dict")
        
        if not _has_content(options):
            raise NoContentError("must supply 'document_content' or 'document_url'")

        default_options = {
            'name': 'default',
            'document_type': 'pdf',
            'test': False,
            'async': False,
            'raise_exception_on_failure': False
        }
        options = dict(list(default_options.items()) + list(options.items()))
        raise_exception_on_failure = options.pop('raise_exception_on_failure')
        query = { 'user_credentials': self.api_key }
        if options['async']:
            query['output'] = 'json'
        doc_options = _format_keys({'doc': options})
        
        resp = requests.post('%sdocs' % (self._url), data=doc_options, params=query, timeout=self._timeout)

        if raise_exception_on_failure and resp.status_code != 200:
            raise DocumentCreationFailure(resp.content, resp.status_code)
            
        if options['async']:
            return json.loads(resp.content.decode("utf-8"))
        else:
            return resp
        
    def list_docs(self, options=None):
        if options is None:
            raise ValueError("Please pass in an options dict")

        default_options = { 
            'page': 1,
            'per_page': 100,
            'raise_exception_on_failure': False,
            'user_credentials': self.api_key
        }
        options = dict(list(default_options.items()) + list(options.items()))
        raise_exception_on_failure = options.pop('raise_exception_on_failure')

        resp = requests.get('%sdocs' % (self._url), params=options, timeout=self._timeout)
        
        if raise_exception_on_failure and resp.status_code != 200:
            raise DocumentListingFailure(resp.content, resp.status_code)
        return resp
        
    def status(self, status_id, raise_exception_on_failure=False):
        query = { 
            'output': 'json',
            'user_credentials': self.api_key 
        }

        resp = requests.get('%sstatus/%s' % (self._url, status_id), params=query, timeout=self._timeout)

        if raise_exception_on_failure and resp.status_code != 200:
            raise DocumentStatusFailure(resp.content, resp.status_code)

        if resp.status_code == 200:
            as_json = json.loads(resp.content.decode("utf-8"))
            if as_json['status'] == 'completed':
                as_json['download_key'] = re.match('.*?\/download\/(.+)', as_json['download_url']).groups()[0]
            return as_json
        return resp
        
    def download(self, download_key, raise_exception_on_failure=False):
        query = { 
            'output': 'json',
            'user_credentials': self.api_key 
        }
        resp = requests.get('%sdownload/%s' % (self._url, download_key), params=query, timeout=self._timeout)

        if raise_exception_on_failure and resp.status_code != 200:
            raise DocumentDownloadFailure(resp.content, resp.status_code)
        return resp

def _has_content(options):
    content = options.get('document_content') or options.get('document_url')
    return bool(content)

def _format_keys(options, result=None, parent_key=None):
    if result is None:
        result = {}
    for k, v in list(options.items()):
        if parent_key:
            key = '%s[%s]' % (parent_key, k)
        else:
            key= k
        if isinstance(v, dict):
            _format_keys(v, result, key)
        elif v is False: result[key] = 'false'
        elif v is True: result[key] = 'true'
        else:
            result[key] = v
    return result
