import os
import platform
import threading

import requests

from .exceptions import ServerError

__all__ = [
    "SimqClient",
]


class SimqClient(object):

    def __init__(
        self,
        base_url,
        api_key=None,
        api_key_header="apikey",
        worker=None,
        headers=None,
        **kwargs,
    ):
        self.base_url = self.fix_base_url(base_url)
        self.api_key = api_key
        self.worker = worker or self.get_default_worker_name()
        self.kwargs = kwargs
        # make headers
        self.headers = {}
        if self.api_key:
            self.headers[api_key_header] = self.api_key
        if headers:
            self.headers.update(headers)
        # 使用长连接
        self.httpclient = requests.Session()

    def fix_base_url(self, base_url):
        if base_url.endswith("/"):
            base_url = base_url[:-1]
        return base_url

    def get_default_worker_name(self):
        node = platform.node()
        pid = os.getpid()
        tid = threading.current_thread().ident
        return f"{node}-{pid}-{tid}"

    def get_service_url(self, channel, service):
        return f"{self.base_url}/{channel}/{service}"

    def get_response(self, response):
        if response.status_code != 200:
            raise ServerError(
                "server response status code != 200, status_code=%s",
                response.status_code,
            )
        try:
            response_data = response.json()
        except Exception:
            raise ServerError(
                "server response is not a valid json content, content=%s",
                response.content[:200],
            )
        if not "data" in response_data:
            raise ServerError(
                "server response format error, response_data=%s", response_data
            )
        return response_data["data"]

    def rpush(self, channel, data=None, id=None, add_time=None):
        url = self.get_service_url(channel, "rpush")
        response = self.httpclient.post(
            url,
            json={
                "data": data,
                "id": id,
                "add_time": add_time,
            },
            headers=self.headers,
        )
        return self.get_response(response)

    def lpush(self, channel, data=None, id=None, add_time=None):
        url = self.get_service_url(channel, "lpush")
        response = self.httpclient.post(
            url,
            json={
                "data": data,
                "id": id,
                "add_time": add_time,
            },
            headers=self.headers,
        )
        return self.get_response(response)

    def pop(self, channel, timeout=5):
        url = self.get_service_url(channel, "pop")
        response = self.httpclient.post(
            url,
            json={
                "worker": self.worker,
                "timeout": timeout,
            },
            headers=self.headers,
        )
        return self.get_response(response)

    def ack(self, channel, id, result=None):
        url = self.get_service_url(channel, "ack")
        response = self.httpclient.post(
            url,
            json={
                "id": id,
                "result": result,
            },
            headers=self.headers,
        )
        return self.get_response(response)

    def query(self, channel, id, timeout=0):
        url = self.get_service_url(channel, "query")
        response = self.httpclient.post(
            url,
            json={
                "id": id,
                "timeout": timeout,
            },
            headers=self.headers,
        )
        return self.get_response(response)

    def cancel(self, channel, id):
        url = self.get_service_url(channel, "query")
        response = self.httpclient.post(
            url,
            json={
                "id": id,
            },
            headers=self.headers,
        )
        return self.get_response(response)

    def ret(self, channel, id):
        url = self.get_service_url(channel, "ret")
        response = self.httpclient.post(
            url,
            json={
                "id": id,
            },
            headers=self.headers,
        )
        return self.get_response(response)
