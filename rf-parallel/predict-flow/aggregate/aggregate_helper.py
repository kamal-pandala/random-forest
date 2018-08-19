import sys
import logging
import numpy as np
from minio import Minio
from minio.error import ResponseError


def minio_init_client(endpoint, access_key=None, secret_key=None, secure=True,
                      region=None, http_client=None):
    client = Minio(endpoint, access_key, secret_key, secure, region, http_client)
    return client


def minio_get_object(client, bucketname, objectname, filepath, logger):
    try:
        client.fget_object(bucketname, objectname, filepath)
    except ResponseError as err:
        logger.info(err)

        
def minio_put_object(client, bucketname, objectname, filepath, logger):
    try:
        client.fput_object(bucketname, objectname, filepath)
    except ResponseError as err:
        logger.info(err)


def minio_get_all_objects(client, bucketname, prefixname, local_file_prefix, logger):
    try:
        objects = client.list_objects_v2(bucketname, prefix=prefixname, recursive=True)
        for obj in objects:
            minio_get_object(client, bucketname, obj.object_name,
                             local_file_prefix + '/' + obj.object_name.split('/')[1], logger)
    except ResponseError as err:
        logger.info(err)


def get_logger(ctx):
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stderr)
    call_id = ctx.CallID()
    formatter = logging.Formatter(
        '[call: {0}] - '.format(call_id) +
        '%(asctime)s - '
        '%(name)s - '
        '%(levelname)s - '
        '%(message)s'
    )
    ch.setFormatter(formatter)
    root.addHandler(ch)
    return root


def combine_predictions(prediction_a, prediction_b):
    prediction_a += prediction_b
    return prediction_a


def concatenate_multioutput_predictions(predictions_a, predictions_b):
    predictions_a = np.concatenate((predictions_a, predictions_b), axis=1)
    return predictions_a
