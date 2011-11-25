# Copyright (C) 2011 John Keyes
# http://jkeyes.mit-license.org/

"""
Simple wrapper for Doc Raptor API.
"""
import requests
from datetime import datetime

# endpoint URLs
HTTP_URL = 'http://docraptor.com/docs'
HTTPS_URL = 'https://docraptor.com/docs'

class DocRaptorError(Exception):
    """
    Raised whenever there is a document generation error.
    """
    pass

def pdf(api_key, html, params, output_file=None, ssl=False):
    """
    Generate a PDF document.
    """
    params['doc[document_type]'] = 'pdf'
    return doc(api_key, html, params, output_file, ssl)
    
def xls(api_key, html, params, output_file=None, ssl=False):
    """
    Generate an XLS document.
    """
    params['doc[document_type]'] = 'xls'
    return doc(api_key, html, params, output_file, ssl)
    
def doc(api_key, html, params, output_file=None, ssl=False):
    """
    If you want the output written to a file other than 
    the name you supply as a param, pass an output_file 
    (fileobj). To use the SSL endpoint, pass ssl=True.
    """
    params['user_credentials'] = api_key
    params['doc[document_content]'] = html
    url = HTTPS_URL if ssl else HTTP_URL
    response = requests.post(url, data=params)

    # errors, for now dump all of them into a single message
    if 'application/xml' in response.headers['content-type']:
        raise DocRaptorError(response.content)

    if output_file is None:
        output_file = open(params['doc[name]'], 'w')
    output_file.write(response.content)
    return response.content
