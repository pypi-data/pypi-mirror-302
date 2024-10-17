
# pylint: disable=missing-class-docstring, import-error, missing-function-docstring
import json
from syncari.models import *
from syncari.synapse.abstract_synapse import Synapse

class MockSynapse(Synapse):

    def __print(self, funcname, request):
        self.logger.info(funcname)
        self.logger.info(request)
        print()

    def test(self):
        return self.connection

    def synapse_info(self):
        return SynapseInfo(
            name='test_synapse',category='crm',
            metadata=UIMetadata(displayName='Test Synapse', helpUrl='https://support.syncari.com'),
            supportedAuthTypes=[AuthMetadata(authType=AuthType.BASIC_TOKEN)],
            configuredFields=[AuthField(name='CRM ID')])

    def describe(self, desc_request):
        self.__print(self.describe.__name__, desc_request)
        schemas = []
        mock_attr = Attribute.parse_obj({'apiName':'MockAttr','displayName':'MockAttrDisplayName'})
        schemas.append(Schema.parse_obj({'apiName':'MockSchema','displayName':'MockDisplayName','attributes':[mock_attr]}))
        return schemas

    def read(self, sync_request):
        self.__print(self.read.__name__, sync_request)
        watermark = sync_request.watermark
        eds = []
        eds.append(Record.parse_obj({'name':'MockRecord','values':{'key':'val'}}))
        return ReadResponse(watermark=watermark,data=eds)

    def get_by_id(self, sync_request):
        self.__print(self.get_by_id.__name__, sync_request)
        eds = []
        eds.append(Record.parse_obj({'name':'MockRecord','values':{'key':'val'}}))
        return eds

    def create(self, sync_request):
        self.__print(self.create.__name__, sync_request)
        results = []
        results.append(Result.parse_obj({'id':'MockID'}))
        return results

    def update(self, sync_request):
        self.__print(self.update.__name__, sync_request)
        results = []
        results.append(Result.parse_obj({'id':'MockID'}))
        return results

    def delete(self, sync_request):
        self.__print(self.delete.__name__, sync_request)
        results = []
        results.append(Result.parse_obj({'id':'MockID'}))
        return results

    def extract_webhook_identifier(self, webhook_request):
        self.__print(self.extract_webhook_identifier.__name__, webhook_request)
        return 'MockWebhookID'

    def process_webhook(self, webhook_request):
        self.__print(self.process_webhook.__name__, webhook_request)
        eds = []
        eds.append(Record.parse_obj({'name':'MockRecord','values':{'key':'val'}}))
        return eds

    def getHeaders(self):
        return {'test': 'test'}

def test_connect():
    synapse_request = Request(type=RequestType.TEST,
        connection=get_connection(),
        body=None).json()
    synapse = MockSynapse(synapse_request)
    resp = synapse.execute()
    assert resp is not None

def test_get_synapse_info():
    synapse_request = Request(type=RequestType.SYNAPSE_INFO,
                              connection=get_connection(),
                              body=None).json()
    synapse = MockSynapse(synapse_request)
    resp = synapse.execute()
    expected = json.loads(resp)
    assert resp is not None
    synapseInfo = SynapseInfo.parse_raw(resp)
    assert synapseInfo is not None
    assert synapseInfo.metadata is not None
    assert synapseInfo.metadata.helpUrl is not None
    assert synapseInfo.metadata.helpUrl == 'https://support.syncari.com'
def test_describe_route():
    synapse_request = Request(type=RequestType.DESCRIBE,
        connection=get_connection(),
        body=DescribeRequest(entities=['test'])).json()
    synapse = MockSynapse(synapse_request)
    resp = json.loads(synapse.execute())
    mock_schema = Schema.parse_raw(resp[0])
    assert mock_schema.apiName == 'MockSchema'
    assert mock_schema.displayName == 'MockDisplayName'

def test_read_synapse_request():
    synapse_request = Request(type=RequestType.READ,
        connection=get_connection(),
        body=SyncRequest(
            entity=Schema(apiName='test',displayName='Test',attributes=[]), 
            watermark=Watermark(start=0, end=0))).json()
    synapse = MockSynapse(synapse_request)
    resp = json.loads(synapse.execute())
    assert resp is not None

def test_get_synapse_request():
    synapse_request = Request(type=RequestType.GET_BY_ID,
        connection=get_connection(),
        body=SyncRequest(
            entity=Schema(apiName='test',displayName='Test',attributes=[]), 
            watermark=Watermark(start=0, end=0))).json()
    synapse = MockSynapse(synapse_request)
    resp = json.loads(synapse.execute())
    assert resp is not None
    mock_record = Record.parse_raw(resp[0])
    assert mock_record.name == 'MockRecord'

def test_create_synapse_request():
    synapse_request = Request(type=RequestType.CREATE,
        connection=get_connection(),
        body=SyncRequest(
            entity=Schema(apiName='test',displayName='Test',attributes=[]), 
            watermark=Watermark(start=0, end=0))).json()
    synapse = MockSynapse(synapse_request)
    resp = json.loads(synapse.execute())
    assert resp is not None
    mock_record = Result.parse_raw(resp[0])
    assert mock_record.id == 'MockID'

def test_update_synapse_request():
    synapse_request = Request(type=RequestType.UPDATE,
        connection=get_connection(),
        body=SyncRequest(
            entity=Schema(apiName='test',displayName='Test',attributes=[]), 
            watermark=Watermark(start=0, end=0))).json()
    synapse = MockSynapse(synapse_request)
    resp = json.loads(synapse.execute())
    assert resp is not None
    mock_record = Result.parse_raw(resp[0])
    assert mock_record.id == 'MockID'

def test_delete_synapse_request():
    synapse_request = Request(type=RequestType.DELETE,
        connection=get_connection(),
        body=SyncRequest(
            entity=Schema(apiName='test',displayName='Test',attributes=[]), 
            watermark=Watermark(start=0, end=0))).json()
    synapse = MockSynapse(synapse_request)
    resp = json.loads(synapse.execute())
    assert resp is not None
    mock_record = Result.parse_raw(resp[0])
    assert mock_record.id == 'MockID'

def test_process_webook_request():
    synapse_request = Request(type=RequestType.PROCESS_WEBHOOK,
        connection=get_connection(),
        body=WebhookRequest(body=json.dumps([{'key':'value'}]))).json()
    synapse = MockSynapse(synapse_request)
    resp = json.loads(synapse.execute())
    assert resp is not None
    mock_event_data = Record.parse_raw(resp[0])
    assert mock_event_data.name == 'MockRecord'


def test_extract_webhook_identifier():
    synapse_request = Request(type=RequestType.EXTRACT_WEBHOOK_IDENTIFIER,
        connection=get_connection(),
        body=WebhookRequest(body=json.dumps([{'key':'value'}]))).json()
    synapse = MockSynapse(synapse_request)
    resp = synapse.execute()
    assert resp is not None
    assert resp == 'MockWebhookID'


def get_connection():
    authConfig=AuthConfig(endpoint='http://endpoint.com')
    connection = Connection(id='1', name='name', authConfig=authConfig, idFieldName='idfield', watermarkFieldName='watermarkfield', 
        endpoint='http://endpoint.com', createdAtFieldName='createdfield', updatedAtFieldName='updatedfield', oAuthRedirectUrl='http://redirect.com')
    return connection
