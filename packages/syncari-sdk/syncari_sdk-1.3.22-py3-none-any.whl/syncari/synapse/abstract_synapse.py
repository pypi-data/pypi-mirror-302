from abc import ABC, abstractmethod
import json
from typing import Dict

from syncari.models import *
from syncari.rest.client import SyncariException, NotSupportedException
from ..logger import SyncariLogger

# pylint: disable=missing-function-docstring
class Synapse(ABC):
    """
        The abstract synapse class to enforce synapse implementations
    """
    raw_request = None
    connection = None
    request = None
    request_type = None
    init_error = None
    _logger = None

    def __init__(self, raw_request: Request) -> None:
        try:
            self.raw_request = Request.parse_raw(raw_request)
            self.request_type = self.raw_request.type
            self.connection = self.raw_request.connection
            self.request = self.__set_request()
            self._logger = None
        except Exception as e:
            err_msg = 'Failed to execute request {}'.format(raw_request.body)
            self.logger.error(err_msg)
            self.init_error = ErrorResponse(message=err_msg, status_code=400, detail=str(e))

    def __set_request(self):
        if self.request_type == RequestType.DESCRIBE:
            return DescribeRequest.parse_obj(self.raw_request.body)
        elif self.request_type in [RequestType.GET_ACCESS_TOKEN]:
            return OAuthRequest.parse_obj(self.raw_request.body)
        elif self.request_type in [RequestType.READ, RequestType.GET_BY_ID, RequestType.CREATE, RequestType.UPDATE, RequestType.DELETE]:
            return SyncRequest.parse_obj(self.raw_request.body)
        elif self.request_type in [RequestType.EXTRACT_WEBHOOK_IDENTIFIER, RequestType.PROCESS_WEBHOOK]:
            return WebhookRequest.parse_obj(self.raw_request.body)
        else:
            return self.raw_request

    def __get_access_token(self, oauth_request: OAuthRequest) -> dict:
        resp = dict()
        resp['grant_type'] = 'authorization_code'
        resp['code'] = oauth_request.code
        resp['client_id'] = oauth_request.authConfig.clientId
        resp['client_secret'] = oauth_request.authConfig.clientSecret
        resp['redirect_uri'] = oauth_request.redirectUri
        return resp

    def __refresh_token(self, connection: Connection) -> dict:
        resp = dict()
        resp['grant_type'] = 'refresh_token'
        resp['refresh_token'] = connection.authConfig.refreshToken
        resp['client_id'] = connection.authConfig.clientId
        resp['client_secret'] = connection.authConfig.clientSecret
        return resp

    def execute(self):
        """
            The route method that looks for the type of the synapse request and invokes
            appropriate synapse supported method.
        """
        # If there is an initialization exception, just return as response. This is needed to capture it as a well defined error.
        if self.init_error is not None:
            return self.init_error

        self.logger.info(self.request_type)
        # Request type test has credentials in it, we dont want to log.
        # TODO: find ways to just log non-sensitive info.
        if self.request_type is not RequestType.TEST:
            self.logger.info(self.request)
        response = None
        try:
            if self.request_type == RequestType.TEST:
                response = self.test(self.connection)
                if not isinstance(response, Connection):
                    raise self.__prep_invalid_response_exception(response)

            elif self.request_type == RequestType.SYNAPSE_INFO:
                response = self.synapse_info()
                if not isinstance(response, SynapseInfo):
                    raise self.__prep_invalid_response_exception(response)

            elif self.request_type == RequestType.DESCRIBE:
                response = self.describe(self.request)
                if not isinstance(response, list):
                    raise self.__prep_invalid_response_exception(response)
                for val in response:
                    if not isinstance(val, Schema):
                        raise self.__prep_invalid_response_exception(response)

            elif self.request_type == RequestType.READ:
                response = self.read(self.request)
                if not isinstance(response, ReadResponse):
                    raise self.__prep_invalid_response_exception(response)

            elif self.request_type == RequestType.GET_ACCESS_TOKEN:
                if hasattr(self, "get_access_token") and callable(self.get_access_token):
                    response = self.get_access_token(self.request)
                else:
                    response = self.__get_access_token(self.request)
                if not isinstance(response, dict):
                    raise self.__prep_invalid_response_exception(response)

            elif self.request_type == RequestType.REFRESH_TOKEN:
                if hasattr(self, "refresh_token") and callable(self.refresh_token):
                    response = self.refresh_token(self.connection)
                else:
                    response = self.__refresh_token(self.connection)
                if not isinstance(response, dict):
                    raise self.__prep_invalid_response_exception(response)

            elif self.request_type == RequestType.GET_BY_ID:
                response = self.get_by_id(self.request)
                if not isinstance(response, list):
                    raise self.__prep_invalid_response_exception(response)
                for val in response:
                    if not isinstance(val, Record):
                        raise self.__prep_invalid_response_exception(response)

            elif self.request_type == RequestType.CREATE:
                response = self.create(self.request)
                if not isinstance(response, list):
                    raise self.__prep_invalid_response_exception(response)
                for val in response:
                    if not isinstance(val, Result):
                        raise self.__prep_invalid_response_exception(response)

            elif self.request_type == RequestType.UPDATE:
                response = self.update(self.request)
                if not isinstance(response, list):
                    raise self.__prep_invalid_response_exception(response)
                for val in response:
                    if not isinstance(val, Result):
                        raise self.__prep_invalid_response_exception(response)

            elif self.request_type == RequestType.DELETE:
                response = self.delete(self.request)
                if not isinstance(response, list):
                    raise self.__prep_invalid_response_exception(response)
                for val in response:
                    if not isinstance(val, Result):
                        raise self.__prep_invalid_response_exception(response)

            elif self.request_type == RequestType.EXTRACT_WEBHOOK_IDENTIFIER:
                response = self.extract_webhook_identifier(self.request)
                if not isinstance(response, str):
                    raise self.__prep_invalid_response_exception(response)

            elif self.request_type == RequestType.PROCESS_WEBHOOK:
                response = self.process_webhook(self.request)
                if not isinstance(response, list):
                    raise self.__prep_invalid_response_exception(response)
                for val in response:
                    if not isinstance(val, Record):
                        raise self.__prep_invalid_response_exception(response)

            elif self.request_type == RequestType.GET_HEADERS:
                response = self.getHeaders()
                if not isinstance(response, dict):
                    raise self.__prep_invalid_response_exception(response)
                
            elif self.request_type == RequestType.SEARCH:
                response = self.search(self.request)
                if not isinstance(response, list):
                    raise self.__prep_invalid_response_exception(response)
                for val in response:
                    if not isinstance(val, Record):
                        raise self.__prep_invalid_response_exception(response)
                
            else:
                self.logger.error(self.request)
                raise Exception('Invalid synapse request {}'.format(self.request_type))

        except NotSupportedException as e:
            err_msg = 'Operation Not Supported {}'.format(self.request_type)
            response = e.error_response

        except SyncariException as e:
            err_msg = 'Failed to execute request {}'.format(self.request_type)
            response = e.error_response
            
        except Exception as e:
            err_msg = 'Failed to execute request {}'.format(self.request_type)
            self.logger.error(err_msg + " due to " + str(e))
            response = ErrorResponse(message=err_msg, status_code=400, detail=str(e))

        if (isinstance(response, list)):
            json_vals = []
            for v in response:
                json_vals.append(v.json())
            return json.dumps(json_vals)

        try:
            json_resp = response.json()
            return json_resp
        except Exception as e:
            self.logger.error('Encountered exception {}'.format(str(e)))
            self.logger.warn('Response was not serializable: {}'.format(response))
            return response

    def __prep_invalid_response_exception(self, response):
        err_msg = 'Invalid response type for request {}'.format(self.request_type)
        detail = 'The response: {}'.format(str(response))
        raise SyncariException(error_response=ErrorResponse(message=err_msg, detail=detail, status_code=400))

    def raise_not_supported_exception(self):
        raise NotSupportedException(error_response=ErrorResponse(message='Operation {} is not supported'.format(self.request_type), status_code=405))

    @property
    def name(self) -> str:
        """
            Synapse name.
        """
        return self.__class__.__name__

    def print(self, funcname, request):
        self.logger.info(funcname)
        self.logger.info(request)
        print()

    @property
    def logger(self):
        if self.raw_request.syncariId is not None:
            return SyncariLogger.get_logger(f"{self.raw_request.syncariId}")
        return SyncariLogger.get_logger("custom_synapse")

    @property
    def logger(self):
        # Check if the logger has already been created and cached
        if self._logger is not None:
            return self._logger

        # Determine the logger name based on the presence of syncariId
        if self.raw_request.syncariId is not None:
            logger_name = f"{self.raw_request.syncariId}"
            self._logger = SyncariLogger.get_logger(logger_name)
        else:
            self._logger = SyncariLogger.get_logger("custom_synapse")
        
        return self._logger

    @abstractmethod
    def synapse_info(self) -> SynapseInfo:
        pass

    @abstractmethod
    def test(self, connection: Connection) -> Connection:
        pass

    @abstractmethod
    def describe(self, desc_request: DescribeRequest) -> List[Schema]:
        pass

    @abstractmethod
    def read(self, sync_request: SyncRequest) -> ReadResponse:
        pass

    @abstractmethod
    def get_by_id(self, sync_request: SyncRequest) -> List[Record]:
        raise self.raise_not_supported_exception()

    @abstractmethod
    def create(self, sync_request: SyncRequest) -> List[Result]:
        pass

    @abstractmethod
    def update(self, sync_request: SyncRequest) -> List[Result]:
        pass

    @abstractmethod
    def delete(self, sync_request: SyncRequest) -> List[Result]:
        pass

    @abstractmethod
    def extract_webhook_identifier(self, webhook_request: WebhookRequest) -> str:
        pass

    def process_webhook(self, webhook_request: WebhookRequest) -> List[Record]:
        pass

    def getHeaders(self) -> Dict[str, str]:
        pass
    
    def search(self, search_request: SearchRequest) -> List[Record]:
        pass