API_COMPONENT_NAME = "ORGS_TX_CONNECTOR"
API_VERSION = "v1"
API_LEVEL = "core"


def frame_msg(data,status="OK"):
    base_msg = {
        "API_COMPONENT_NAME" : API_COMPONENT_NAME,
        "API_VERSION" : API_VERSION,
        "API_LEVEL" :API_LEVEL,
        "request" : {
            "status" : status,
            "body" : data
        }
    }
    return base_msg