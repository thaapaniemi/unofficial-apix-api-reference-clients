#!/usr/bin/env python3
"""Unofficial Apix API CLI client for making API requests manually"""

import sys
import argparse

import requests
import apix_public_api

parser = argparse.ArgumentParser(
    description='Unofficial Apix API client implementation')
parser.add_argument('-method', "-m", action='store', required=True,
                    help="API method", choices=["SendInvoiceZIP","DeliveryMethod","AddressQuery","SendPrintZIP","SendPayslip"])

parser.add_argument('-software_name', '-s', required=True,
                    nargs='?', help='software_name')
parser.add_argument("-software_version", '-v', required=True,
                    nargs='?', help='software_version')
parser.add_argument("-transfer_id", '-i', required=True,
                    nargs='?', help='transfer_id')
parser.add_argument("-transfer_key", '-k', required=True,
                    nargs='?', help='transfer_key')
parser.add_argument("-file", '-f', required=True, nargs='?', help='Payload')

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-endpoint', '-u', nargs='?', help='API endpoint')
group.add_argument('-environment', '-e', action='store', help="API environment",
                   default="SendInvoiceZIP", choices=["test", "prod"])


def main():
    args = parser.parse_args()

    exitcode = 0

    with apix_public_api.ApixPublicApi(args.transfer_id, args.transfer_key, environment=args.environment) as apix:
        response: requests.Response = None

        data = None
        with open(args.file, "rb") as fh:
            data = fh.read()

        if args.method == "SendInvoiceZIP":
            response = apix.SendInvoiceZIP(
                args.software_name, args.software_version, data)
        elif args.method == "DeliveryMethod":
            response = apix.DeliveryMethod(data)
        elif args.method == "AddressQuery":
            response = apix.AddressQuery(data)
        elif args.method == "SendPrintZIP":
            response = apix.SendPrintZIP(
                args.software_name, args.software_version, data)
        elif args.method == "SendPayslip":
            response = apix.SendPayslip(data)
        else:
            raise Exception(
                "Unknown API method: {method}".format(method=args.method))

        if response.status_code != 200:
            raise Exception("Unknown HTTP error: [{status_code}] {content}".format(status_code=response.status_code, content=response.content))
        else:
            if response.content.find(b"<Status>OK</Status>") >= 0:
                print(response.content)
                sys.stderr.write("Request handled succesfully\n")
                exitcode = 0
            else:
                exitcode = 1
                print(response.content)
                sys.stderr.write(
                    "Request was rejected (attach api response for possible questions for Apix) \n")

    sys.exit(exitcode)


if __name__ == '__main__':
    main()
