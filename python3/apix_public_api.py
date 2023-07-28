"""
Unofficial Apix API client implementation

Basic wrapper (helps with requests, does not check or parse responses)

https://wiki.apix.fi/rest-api-for-external-usage
"""

import sys
import requests
import hashlib
import time


class ApixPublicApiException(Exception):
    pass


class ApixPublicApi(object):
    __transfer_id = None
    __transfer_key = None

    __api_endpoint = None
    __terminal_api_endpoint = None

    def __init__(self, transfer_id: str, transfer_key: str, environment: str = None, endpoints: dict = None) -> None:

        self.__transfer_id = transfer_id
        self.__transfer_key = transfer_key

        if environment is None and endpoints is None:
            raise ApixPublicApiException(
                "init failed, please define either environment[test,prod] or endpoints[dict]")

        if environment is not None and endpoints is not None:
            raise ApixPublicApiException(
                "init failed, please define either environment[test,prod] or endpoints[dict]")

        if endpoints is None and environment == "prod":
            self.__api_endpoint = "https://api.apix.fi"
            self.__terminal_api_endpoint = "https://terminal.apix.fi"
        elif endpoints is None and environment == "test":
            self.__api_endpoint = "https://test-api.apix.fi"
            self.__terminal_api_endpoint = "https://test-terminal.apix.fi"
        elif endpoints and type(endpoints) == dict:
            if not "api" in endpoints:
                raise ApixPublicApiException(
                    "init failed, endpoints must have 'api' key")
            if not "terminal" in endpoints:
                raise ApixPublicApiException(
                    "init failed, endpoints must have 'terminal' key")

            self.__api_endpoint = endpoints["api"]
            self.__terminal_api_endpoint = endpoints["terminal"]
        pass

    def SendInvoiceZIP(self, software_name: str, software_version: str, data: bytes) -> requests.Response:
        """
            SendInvoiceZIP implementation

            software_name: apix informed parameter software_name
            software_version: apix informed parameter software_version
            data: document (invoice, EDI, other) data

            returns requests.Response object
        """

        timestamp = time.strftime("%Y%m%d%H%m%S", time.gmtime())

        h = hashlib.sha256()
        h.update("+".join([software_name, software_version,
                           self.__transfer_id, timestamp, self.__transfer_key]).encode("utf-8"))
        digest = h.hexdigest()

        headers = {'Content-type': 'application/octet-stream'}

        params = {"soft": software_name, "ver": software_version,
                  "TraID": self.__transfer_id, "t": timestamp, "d": "SHA-256:" + digest}

        url = "{endpoint}/invoices?".format(endpoint=self.__api_endpoint)

        response = requests.put(url, data, params=params, headers=headers)
        return response

    def DeliveryMethod(self, request) -> requests.Response:
        """
            DeliveryMethod implementation

            request: Apix Request-xml defined in wiki

            returns requests.Response object
        """

        timestamp = time.strftime("%Y%m%d%H%m%S", time.gmtime())

        h = hashlib.sha256()
        h.update("+".join([self.__transfer_id, timestamp,
                 self.__transfer_key]).encode("utf-8"))
        digest = h.hexdigest()

        headers = {'Content-type': 'text/xml'}

        params = {"TraID": self.__transfer_id,
                  "t": timestamp, "d": "SHA-256:" + digest}

        url = "{endpoint}/method?".format(endpoint=self.__api_endpoint)

        response = requests.put(url, request, params=params, headers=headers)
        return response

    def AddressQuery(self, request) -> requests.Response:
        """
            AddressQuery implementation

            request: Apix Request-xml defined in wiki

            returns requests.Response object
        """

        timestamp = time.strftime("%Y%m%d%H%m%S", time.gmtime())

        h = hashlib.sha256()
        h.update("+".join([self.__transfer_id, timestamp,
                 self.__transfer_key]).encode("utf-8"))
        digest = h.hexdigest()

        headers = {'Content-type': 'text/xml'}

        params = {"TraID": self.__transfer_id,
                  "t": timestamp, "d": "SHA-256:" + digest}

        url = "{endpoint}/method?".format(endpoint=self.__api_endpoint)

        response = requests.put(url, request, params=params, headers=headers)
        return response

    def SendPrintZIP(self, software_name: str, software_version: str, data: bytes) -> requests.Response:
        """
            SendPrintZIP implementation

            software_name: customer can decide, information only
            software_version: customer can decide, information only
            data: zip archive containing letterxml data and document pdf

            returns requests.Response object
        """

        timestamp = time.strftime("%Y%m%d%H%m%S", time.gmtime())

        h = hashlib.sha256()
        h.update("+".join([software_name, software_version,
                           self.__transfer_id, timestamp, self.__transfer_key]).encode("utf-8"))
        digest = h.hexdigest()

        headers = {'Content-type': 'application/octet-stream'}

        params = {"soft": software_name, "ver": software_version,
                  "TraID": self.__transfer_id, "t": timestamp, "d": "SHA-256:" + digest}

        url = "{endpoint}/print?".format(endpoint=self.__api_endpoint)

        response = requests.put(url, data, params=params, headers=headers)
        return response

    def SendPayslip(self, data) -> requests.Response:
        """
            SendPayslip implementation
            data: zip archive containing payslip 2.0 xml and payslip image pdf

            returns requests.Response object
        """

        timestamp = time.strftime("%Y%m%d%H%m%S", time.gmtime())

        h = hashlib.sha256()
        h.update("+".join([self.__transfer_id, timestamp,
                 self.__transfer_key]).encode("utf-8"))
        digest = h.hexdigest()

        headers = {'Content-type': 'application/octet-stream'}

        params = {
            "TraID": self.__transfer_id, "t": timestamp, "d": "SHA-256:" + digest}

        url = "{endpoint}/sendpayslip?".format(endpoint=self.__api_endpoint)

        response = requests.put(url, data, params=params, headers=headers)
        return response

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        pass


if __name__ == '__main__':
    raise Exception('Use as library')
