from common.td import TD

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

td_client = TD()

def my_handler(event, context):

    logger.info('Starting TD Ameritrade')

    return {
        'message' : message
    }