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

# endpoint URLs
HTTP_URL = 'http://docraptor.com/'
HTTPS_URL = 'https://docraptor.com/'

class NoApiKeyProvidedError(RuntimeError):
    pass
    
class NoContentError(KeyError):
    pass

class DocRaptorRequestException(StandardError):
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
        self.api_key = api_key if api_key is not None else os.environ.get('DOCRAPTOR_API_KEY', None)
        if not self.api_key:
            raise NoApiKeyProvidedError("No API key provided")

    def create(self, options=None):
        if options is None:
            raise ValueError("Please pass in an options dict")
        if not (bool(options.get('document_content', False) or options.get('document_url', False))):

            raise NoContentError("must supply 'document_content' or 'document_url'")

        default_options = {
            'name': 'default',
            'document_type': 'pdf',
            'test': False,
            'async': False,
            'raise_exception_on_failure': False
        }
        options = dict(default_options.items() + options.items())
        raise_exception_on_failure = options.pop('raise_exception_on_failure')
        query = { 'user_credentials': self.api_key }
        if options['async']:
            query['output'] = 'json'
        doc_options = _format_keys({'doc': options})
        
        url = os.environ.get("DOCRAPTOR_URL", HTTPS_URL)
        resp = requests.post('%sdocs' % (url), data=doc_options, params=query)

        if raise_exception_on_failure and resp.status_code != 200:
            raise DocumentCreationFailure(resp.content, resp.status_code)
            
        if options['async']:
            as_json = json.loads(resp.content)
            self.status_id = as_json['status_id']
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
        options = dict(default_options.items() + options.items())
        raise_exception_on_failure = options.pop('raise_exception_on_failure')
        url = os.environ.get("DOCRAPTOR_URL", HTTPS_URL)
        resp = requests.get('%sdocs' % (url), params=options)
        
        if raise_exception_on_failure and resp.status_code != 200:
            raise DocumentListingFailure(resp.content, resp.status_code)
        return resp
        
    def status(self, status_id, raise_exception_on_failure=False):
        query = { 
            'output': 'json',
            'user_credentials': self.api_key 
        }
        url = os.environ.get("DOCRAPTOR_URL", HTTPS_URL)
        resp = requests.get('%sstatus/#%s' % (url, status_id), params=query)
        if raise_exception_on_failure and resp.status_code != 200:
            raise DocumentStatusFailure(resp.content, resp.status_code)

        if resp.status_code == 200:
            as_json = json.loads(resp.content) #'{ "status": "completed", "download_url": "/blah/download/jkskskdldkd/" }') #resp.content)
            if as_json['status'] == 'completed':
                as_json['download_key'] = re.match('/.*?\/download\/(.+)/', as_json['download_url']).groups()[0]
            return as_json
        return resp
        
    def download(self, download_key, raise_exception_on_failure=False):
        query = { 
            'output': 'json',
            'user_credentials': self.api_key 
        }
        url = os.environ.get("DOCRAPTOR_URL", HTTPS_URL)
        resp = requests.get('%s/download/%s' % (url, download_key), params=query)
        if raise_exception_on_failure and resp.status_code != 200:
            raise DocumentDownloadFailure(resp.content, resp.status_code)
        return resp
        
def _format_keys(options, result=None, parent_key=None):
    if result is None:
        result = {}
    for k, v in options.items():
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
