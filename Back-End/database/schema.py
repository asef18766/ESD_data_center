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
    ReferenceField,
    DictField,
    DateTimeField
)

class DeviceMeta(Document):
    hid = StringField(max_length=100,primary_key=True) # md5(node_token|device name)
    name = StringField(max_length=100)
    worker_type = BooleanField(required=True) # true for input, false for output
    min_throughput = FloatField(required=True)
    max_throughput = FloatField(required=True)
    unit = StringField(max_length=100)

class FarmNode(Document):
    pass

class DeviceLog(Document):
    device = ReferenceField(DeviceMeta)
    owner = ReferenceField(FarmNode)
    data = FloatField(required = True)
    timestamp = DateTimeField(required = True)

class OperateUnit(EmbeddedDocument):
    output_device = ReferenceField(DeviceMeta , required=True)
    operate = BooleanField(required=True)

class OperateFactor(EmbeddedDocument):
    input_device = ReferenceField(DeviceMeta, required=True)
    condiction = StringField(max_length=10)
    value = FloatField(required=True)
    solutions = ListField(EmbeddedDocumentField(OperateUnit, required=True))

class NodeConfig(Document):
    version = IntField()
    node_name = StringField(max_length=1000)
    icon_link = URLField()
    connection_method = DictField()
    configures = EmbeddedDocumentListField(OperateFactor)
    device_icons = DictField() # key:hid, value:URL

class FarmNode(Document):
    token = StringField(max_length=1000, primary_key=True)
    input_devices = ListField(ReferenceField(DeviceMeta))
    output_devices = ListField(ReferenceField(DeviceMeta))
    config = ReferenceField(NodeConfig)
    dev_logs = ListField(ReferenceField(DeviceLog))

class User(Document):
    identity = StringField(primary_key=True)
    nodes = ListField(ReferenceField(FarmNode))
    account = StringField()
