import fdk
import json
import sys
import uuid
import asyncio
import requests
import logging
import concurrent.futures
from helper import *
from functools import partial
from minio import Minio
from minio.error import ResponseError


def minio_init_client(endpoint, access_key=None, secret_key=None, secure=True,
                      region=None, http_client=None):
    client = Minio(endpoint, access_key, secret_key, secure, region, http_client)
    return client


def minio_count_objects(client, bucketname, prefixname, logger):
    try:
        objects = client.list_objects_v2(bucketname, prefix=prefixname, recursive=True)
        count = sum(1 for _ in objects)
        return count
    except ResponseError as err:
        logger.info(err)
        return 0


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


async def planner_1(body, logger):
    storage_client = StorageClient(body.get('endpoint'), body.get('port'), body.get('access_key'),
                                   body.get('secret_key'), body.get('secure'), body.get('region'))
    predict_data_object = DataObject(body.get('data_bucket_name'), body.get('data_object_name'))

    unique_id = uuid.uuid4()
    output_object = OutputObject(body.get('output_bucket_name'),
                                 output_object_prefix_name=str(unique_id))

    model_object = ModelObject(body.get('model_object_bucket_name'), body.get('model_object_prefix_name'))

    # Parameters required for initialising minio client
    endpoint = storage_client.endpoint
    port = storage_client.port
    if port is not None and port != 0:
        endpoint += ':' + str(port)

    access_key = storage_client.access_key
    secret_key = storage_client.secret_key
    secure = storage_client.secure
    region = storage_client.region

    # Establishing connection to remote storage
    minio_client = minio_init_client(endpoint, access_key=access_key, secret_key=secret_key,
                                     secure=secure, region=region)
    file_count = minio_count_objects(minio_client, model_object.model_object_bucket_name,
                                     model_object.model_object_prefix_name, logger)
    logger.info('No. of model files: ' + str(file_count))

    lb_endpoint = body.get('lb_planner_endpoint')
    lb_response = requests.get('http://' + lb_endpoint + ':8081/1/lb/nodes')
    n_nodes = len(lb_response.json().get('nodes'))
    n_predictions_per_node = file_count // n_nodes
    n_r_predictions = file_count % n_nodes

    logger.info('No. of predictions per node: ' + str(n_predictions_per_node))
    logger.info('No. of remainder predictions: ' + str(n_r_predictions))

    predict_async = []
    n_prediction_list = [0]
    for i in range(n_nodes):
        if n_r_predictions > 0:
            n = n_predictions_per_node + 1
            n_r_predictions -= 1
        else:
            n = n_predictions_per_node

        n_prediction_list.append(n + n_prediction_list[-1])

        estimator_client = EstimatorClient(lb_endpoint, '8081', False)

        predict_async.append(partial(estimator_client.predict, storage_client, predict_data_object,
                                     model_object, output_object, model_file_count=n))
    logger.info('Initialised predict_async objects!!!')

    with concurrent.futures.ThreadPoolExecutor(max_workers=n_nodes) as executor:
        loop = asyncio.get_event_loop()
        futures = [
            loop.run_in_executor(
                executor,
                predict_async[i],
                str(i) + ':' + str(n_prediction_list[i])
            )
            for i in range(n_nodes)
        ]
        output_list = []
        for output in await asyncio.gather(*futures):
            output_list.append(output)
        if all(output is not None for output in output_list):
            n_estimators = 0
            for output in output_list:
                n_estimators += output.output_attributes['n_estimators']
            n_outputs = output_list[0].output_attributes['n_outputs']
            logger.info('No. of total estimators: ' + str(n_estimators))
            logger.info('No. of outputs: ' + str(n_outputs))
            return output_object, n_estimators, n_outputs
        else:
            pass


async def planner_2(body, output_object, n_estimators, n_outputs, logger):
    logger.info('Inside planner_2!!!')

    storage_client = StorageClient(body.get('endpoint'), body.get('port'), body.get('access_key'),
                                   body.get('secret_key'), body.get('secure'), body.get('region'))

    payload_dict = {**storage_client.__dict__, **output_object.__dict__,
                    'n_outputs': n_outputs, 'n_estimators': n_estimators}

    lb_endpoint = body.get('lb_planner_endpoint')
    endpoint_url = 'http://' + lb_endpoint + ':8081' + '/r/rf-parallel/predict-flow/global-aggregate'
    response = requests.post(endpoint_url, json=payload_dict)
    logger.info(response.text)

    return output_object


async def handler(ctx, data=None, loop=None):
    if data and len(data) > 0:
        logger = get_logger(ctx)
        body = json.loads(data)

        logger.info('Resuming loop in handler!!!')
        if loop is None:
            loop = asyncio.get_event_loop()
            logger.info('Created new loop in handler!!!')

        output_object, n_estimators, n_outputs = await asyncio.ensure_future(planner_1(body, logger), loop=loop)
        output_object = await asyncio.ensure_future(planner_2(body, output_object, n_estimators, n_outputs, logger), loop=loop)
        logger.info('Loop completed in handler!!!')

    return json.dumps(output_object.__dict__)



if __name__ == "__main__":
    fdk.handle(handler)

