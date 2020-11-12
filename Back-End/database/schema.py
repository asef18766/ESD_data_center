from mongoengine import (
    Document,
    EmbeddedDocument
)
from mongoengine.fields import (
    StringField,
    IntField,
    FloatField,
    BooleanField,
    URLField,
    EmbeddedDocumentField,
    EmbeddedDocumentListField,
    ListField,
    ReferenceField
)
class IDeviceConnectMethod(EmbeddedDocument):
    conn_type = StringField(max_length=255)
    meta = {'allow_inheritance': True}

class InternetConnect(IDeviceConnectMethod):
    ip = StringField(max_length=255)
    port = IntField()

class UsbConnect(IDeviceConnectMethod):
    fd = StringField(max_length=1000)

class DeviceMeta(Document):
    name = StringField(max_length=100,primary_key=True)
    icon_link = URLField()
    worker_type = BooleanField(required=True)
    min_throughput = FloatField(required=True)
    max_throughput = FloatField(required=True)
    unit = StringField(max_length=100)
    connection_method = EmbeddedDocumentField(IDeviceConnectMethod)

class FarmNode(Document):
    token = StringField(max_length=1000, primary_key=True)
    node_name = StringField(max_length=1000)
    icon_link = URLField()
    input_devices = ListField(ReferenceField(DeviceMeta))
    output_devices = ListField(ReferenceField(DeviceMeta))

class OperateUnit(EmbeddedDocument):
    output_device = ReferenceField(DeviceMeta , required=True)
    operate = BooleanField(required=True)

class OperateFactor(EmbeddedDocument):
    input_device = ReferenceField(DeviceMeta, required=True)
    condiction = StringField(max_length=10)
    value = FloatField(required=True)
    solutions = ListField(EmbeddedDocumentField(OperateUnit, required=True))

class NodeConfig(Document):
    node = ReferenceField(FarmNode , required=True)
    version = StringField()
    configures = EmbeddedDocumentListField(OperateFactor)

class User(Document):
    identity = StringField(primary_key=True)
    nodes = ListField(ReferenceField(FarmNode))
    account = StringField()

class DeviceLog(Document):
    device = ReferenceField(DeviceMeta)
    data = FloatField(required = True)
