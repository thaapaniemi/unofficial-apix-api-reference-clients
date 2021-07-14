#!/usr/bin/env python3
"""Unofficial Apix API CLI client for making API requests manually"""

import sys
import argparse
import apix_public_api

parser = argparse.ArgumentParser(description='Unofficial Apix API client implementation')
parser.add_argument('-method', "-m", action='store', required=True, help="API method", default="SendInvoiceZIP", choices=["SendInvoiceZIP"])

parser.add_argument('-software_name', '-s', required=True, nargs='?', help='software_name')
parser.add_argument("-software_version", '-v', required=True, nargs='?', help='software_version')
parser.add_argument("-transfer_id", '-i', required=True, nargs='?', help='transfer_id')
parser.add_argument("-transfer_key", '-k', required=True, nargs='?', help='transfer_key')
parser.add_argument("-file", '-f', required=True, nargs='?', help='Payload')

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-endpoint', '-u', nargs='?', help='API endpoint')
group.add_argument('-environment', '-e', action='store', help="API environment", default="SendInvoiceZIP", choices=["test", "prod"])


def main():
    args = parser.parse_args()

    if args.method == "SendInvoiceZIP":
        endpoint = None
        if args.endpoint:
            endpoint = args.endpoint
        elif args.environment == "prod":
            endpoint = "https://api.apix.fi/invoices"
        elif args.environment == "test":
            endpoint = "https://test-api.apix.fi/invoices"

        data = None
        with open(args.file, "rb") as fh:
            data = fh.read()

        (status_code, response_str) = apix_public_api.SendInvoiceZIP(endpoint, args.transfer_id, args.transfer_key, args.software_name, args.software_version, data)
        response_str = response_str.decode("utf-8", errors="replace")

        if status_code != 200:
            raise Exception("Unknown HTTP error: [{status_code}] {response_str}".format(status_code=status_code, response_str=response_str))

        # This is quick-and-dirty solution, real solution would be a use xml parser to get data
        if response_str.find("<Status>OK</Status>") >= 0:
            print("Invoice sent successfully:\n{response_str}\n".format(response_str=response_str))
            sys.exit(0)
        else:
            print("Invoice was rejected (attach api response for possible questions for Apix):\n{response_str}\n".format(response_str=response_str))
            sys.exit(1)

    else:
        raise Exception("Unknown API method: {method}".format(args.method))


if __name__ == '__main__':
    main()