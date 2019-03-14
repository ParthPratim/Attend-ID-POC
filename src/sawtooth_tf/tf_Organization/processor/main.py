import os
from sawtooth_sdk.processor.core import TransactionProcessor
from sawtooth_sdk.processor.log import init_console_logging
from sawtooth_sdk.processor.log import log_configuration
from sawtooth_sdk.processor.config import get_log_config
from sawtooth_sdk.processor.config import get_log_dir
from processor.handler import tf_Organization


def processor_main():
    print("VERBOSE : Processor Began")
    tp = TransactionProcessor(url='tcp://'+os.environ['HOSTNAME']+':4004')
    handler = tf_Organization()
    tp.add_handler(handler)
    tp.start()

""" 
Transaction Processor - Organization : 
1> Register new organization
 """
