import zmq
import hashlib
from event_sub.protos.events_pb2 import *
from event_sub.protos.validator_pb2 import *
#from event_sub import initiate_training
from event_sub.azure_face_module import AzureFaceModule
from rest_endpoint.internals.get_state_data import GetStateData

DIGITAL_ID_ADDRESS_PREFIX = hashlib.sha512("digital_id".encode('utf-8')).hexdigest()[0:6]
VALIDATOR_ZMQ_LINK  = "tcp://validator:4004"
EVENT_TYPE = "sawtooth/state-delta"

def SubscribeEvent():
    subscription = EventSubscription(
    event_type="sawtooth/state-delta",
    filters=[

        EventFilter(
            key="address",
            match_string=DIGITAL_ID_ADDRESS_PREFIX+".*",
            filter_type=EventFilter.REGEX_ANY)
    ])

    ctx = zmq.Context()
    socket = ctx.socket(zmq.DEALER)
    socket.connect(VALIDATOR_ZMQ_LINK)


    request = ClientEventsSubscribeRequest(
        subscriptions=[subscription]).SerializeToString()

    correlation_id = "123"
    msg = Message(
        correlation_id=correlation_id,
        message_type=Message.CLIENT_EVENTS_SUBSCRIBE_REQUEST,
        content=request)


    socket.send_multipart([msg.SerializeToString()])

    while True:
        resp = socket.recv_multipart()[-1]


        msg = Message()
        msg.ParseFromString(resp)


        """
        if msg.message_type != Message.CLIENT_EVENTS_SUBSCRIBE_RESPONSE:
            print("Unexpected message type")
            return
        """


        events = EventList()
        events.ParseFromString(msg.content)

        for e in events.events:
            if e.event_type == EVENT_TYPE:

                data = GetStateData(e.attributes[0].value)
                #initiate_training.Now(data['DigitalID-'],data['TrainingImageHash'])
                AzureFaceModule.initiate_cloud_training(data['DigitalID'],data['TrainingImageHash'])
