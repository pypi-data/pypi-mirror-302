# pylint: disable=import-error
import json
import backoff
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from syncari.logger import SyncariLogger
from syncari.models import ErrorResponse

logger = SyncariLogger.get_logger('rest_client')

class RetryableException(Exception):
    """Class to mark an ApiException as retryable."""

class SyncariException(Exception):
    error_response = None
    def __init__(self, error_response: ErrorResponse) -> None:
        self.error_response = error_response

class NotSupportedException(Exception):
    error_response = None
    def __init__(self, error_response: ErrorResponse) -> None:
        err_msg = "Operation is not supported" if error_response is None else error_response.message
        self.error_response = ErrorResponse(message=err_msg, status_code=405)

# pylint: disable=too-many-instance-attributes
class SyncariRestClient:

    success_responses=[200,201,202,204]

    """
        Default Syncari Rest Client
    """
    def __init__(self, base_url, auth_config, numRetries=5, backoff_factor=2):
        self.auth_config = auth_config
        self.rest_url = base_url
        self._session = requests.Session()

        retry_strategy = Retry(
            total=numRetries,
            status_forcelist=[429, 500, 502, 503, 504],
            backoff_factor=backoff_factor,
            allowed_methods=["HEAD", "GET", "POST", "OPTIONS"],
            raise_on_status=False
        )
        #adapter = HTTPAdapter(max_retries=retry_strategy)

        adapter = requests.adapters.HTTPAdapter(max_retries=retry_strategy)
        self._session.mount('https://', adapter)

    def get(self, path, **kwargs):
        """
            A default get request
        """
        return self.rest_request('GET', path, **kwargs)

    def post(self, path, **kwargs):
        """
            A default post request
        """
        return self.rest_request('POST', path, **kwargs)

    def put(self, path, **kwargs):
        """
            A default put request
        """
        return self.rest_request('PUT', path, **kwargs)

    def delete(self, path, **kwargs):
        """
            A default delete request
        """
        return self.rest_request('DELETE', path, **kwargs)

    @backoff.on_exception(backoff.expo,
                          RetryableException,
                          max_time=5 * 60, # in seconds
                          factor=30,
                          jitter=None)
    def _retryable_request(self, method, url, stream=False, **kwargs):
        """
            A retryable request call
        """
        resp = None
        err_msg = 'Failed to execute {} on url:{}'.format(method, url)

        try:
            req = requests.Request(method, url, **kwargs).prepare()
            resp = self._session.send(req, stream=stream)
            logger.info("%s: HTTP %s %s",resp.status_code, method, url)
        except Exception as e:
            logger.error("Request to %s failed, payload %s error %s", url,
                         kwargs, e)
            raise SyncariException(error_response=ErrorResponse(message=err_msg, detail=str(e), status_code=500))

        if resp.status_code not in self.success_responses:
            logger.error("Request to %s failed with status code %s, payload %s response %s",url, resp.status_code,kwargs, resp.text)
            error_resp = ErrorResponse(message=err_msg, detail=self.__get_error_response_details(resp), status_code=resp.status_code)
            raise SyncariException(error_response=error_resp)

        return resp

    def rest_request(self, method, path, **kwargs):
        """
            Rest request with relative path. The rest_url (base_url) should be set
        """
        url = self.rest_url+path
        logger.info("%s: %s", method, url)
        return self._retryable_request(method, url, **kwargs)

    def __get_error_response_details(self, error):
        """
            A simple wrapper to get error response in a readable format
        """
        error_resp_json = {
            'reason': error.reason,
            'status_code': error.status_code,
            'content': error.text
        }
        return json.dumps(error_resp_json)
