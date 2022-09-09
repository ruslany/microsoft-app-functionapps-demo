import logging
import os, uuid

import azure.functions as func
from azure.storage.queue import (
        QueueClient,
        BinaryBase64EncodePolicy,
        BinaryBase64DecodePolicy
)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request GetWorkItems.')

    connect_str = os.getenv("AzureWebJobsStorage")

    base64_queue_client = QueueClient.from_connection_string(
                            conn_str=connect_str, queue_name='outqueue',
                            message_encode_policy = BinaryBase64EncodePolicy(),
                            message_decode_policy = BinaryBase64DecodePolicy()
                        )

    properties = base64_queue_client.get_queue_properties()
    count = properties.approximate_message_count
    
    return func.HttpResponse(
        f"There are {count} pending work items",
        status_code=200
    )
