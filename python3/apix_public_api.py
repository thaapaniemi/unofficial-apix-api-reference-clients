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

    ###  Administrative functions ###

    @staticmethod
    def AuthenticateByUser(username: str, password: str, environment: str, endpoint: str = None) -> requests.Response:
        if endpoint is None and environment == "prod":
            endpoint = "https://api.apix.fi"
        elif endpoint is None and environment == "test":
            endpoint = "https://test-api.apix.fi"

        timestamp = time.strftime("%Y%m%d%H%m%S", time.gmtime())

        pwhash = hashlib.sha256(password.encode("utf-8"))

        h = hashlib.sha256()
        h.update(
            "+".join([username, timestamp, pwhash.hexdigest()]).encode("utf-8"))
        digest = h.hexdigest()

        params = {"uid": username, "t": timestamp, "d": "SHA-256:" + digest}

        url = "{endpoint}/authuser?".format(endpoint=endpoint)

        response = requests.get(url, params=params)
        return response

    def RetrieveTransferID(self, company_id) -> requests.Response:
        """
            RetrieveTransferID non-implementation

            RetrieveTransferID is a deprecated function, please use AuthenticateByUser
        """
        raise NotImplemented()

    def RetrieveCompanyInformation(self) -> requests.Response:
        timestamp = time.strftime("%Y%m%d%H%m%S", time.gmtime())

        h = hashlib.sha256()
        h.update("+".join([self.__transfer_id, timestamp,
                 self.__transfer_key]).encode("utf-8"))
        digest = h.hexdigest()

        params = {"TraID": self.__transfer_id,
                  "t": timestamp, "d": "SHA-256:" + digest}

        url = "{endpoint}/getcompanyinfo?".format(endpoint=self.__api_endpoint)

        response = requests.get(url, params=params)
        return response

    ###  Sending functions ###

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

     # Receiving functions
    def ListInvoiceZIPs(self) -> requests.Response:
        """
            ListInvoiceZIPs implementation

            returns requests.Response object
        """
        timestamp = time.strftime("%Y%m%d%H%m%S", time.gmtime())

        h = hashlib.sha256()
        h.update("+".join([self.__transfer_id, timestamp,
                 self.__transfer_key]).encode("utf-8"))
        digest = h.hexdigest()

        params = {"TraID": self.__transfer_id,
                  "t": timestamp, "d": "SHA-256:" + digest}

        url = "{endpoint}/list2?".format(endpoint=self.__terminal_api_endpoint)

        response = requests.get(url, params=params)
        return response

    def SetReceiveEmail(self, request):
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

        url = "{endpoint}/email?".format(endpoint=self.__api_endpoint)

        response = requests.put(url, request, params=params, headers=headers)

    def Download(self, storage_id, storage_key):
        raise NotImplementedError("TODO")

    def GetMetadata(self, storage_id, storage_key):
        raise NotImplementedError("TODO")

    # Accounting functions
    def GetUsedSaldo(self, storage_id, storage_key):
        raise NotImplementedError("TODO")

    # Payslip API

    def Delete(self, receiver_hash, date_id):
        raise NotImplementedError("TODO")

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        pass


if __name__ == '__main__':
    raise Exception('Use as library')
