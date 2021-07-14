"""
Unofficial Apix API client implementation

https://wiki.apix.fi/display/IAD/Rest+API+for+external+usage

"""

import sys
import urllib.request, urllib.parse, urllib.error
import hashlib
import time


def SendInvoiceZIP(endpoint, transfer_id, transfer_key, software_name, software_version, invoice_data, **kwargs):
    """Send invoice file to Apix REST API"""

    # needed params:
    # endpoint (https://test-api.apix.fi/invoices, https://api.apix.fi/invoices)
    # transfer_id
    # transfer_key
    # software_name
    # software_version
    # invoice_data
    timestamp = time.strftime("%Y%m%d%H%m%S")

    h = hashlib.sha256()
    h.update("+".join([software_name, software_version, transfer_id, timestamp, transfer_key]).encode("utf-8"))
    digest = h.hexdigest()

    values = {"soft": software_name, "ver": software_version, "TraID": transfer_id, "t": timestamp, "d": "SHA-256:" + digest}

    url = "{endpoint}?{params}".format(endpoint=endpoint, params=urllib.parse.urlencode(values))

    #print(url)

    opener = urllib.request.build_opener(urllib.request.HTTPHandler)
    request = urllib.request.Request(url, data=invoice_data)
    request.add_header('Content-Type', "application/octet-stream")
    request.get_method = lambda: 'PUT'
    response = opener.open(request)

    raw_response = response.read()

    return (response.status, raw_response)


if __name__ == '__main__':
    raise Exception('Use as library')
