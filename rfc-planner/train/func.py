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


async def planner(body, logger):
    estimator_params = body.get('estimator_params')
    n_estimators = estimator_params['n_estimators']
    logger.info('No. of required estimators: ' + str(n_estimators))

    storage_client = StorageClient(body.get('endpoint'), body.get('port'), body.get('access_key'),
                                   body.get('secret_key'), body.get('secure'))
    train_data_object = DataObject(body.get('data_bucket_name'), body.get('data_object_name'))

    unique_id = uuid.uuid4()
    model_object = ModelObject(body.get('model_object_bucket_name'),
                               model_object_prefix_name=str(unique_id))

    lb_endpoint = body.get('lb_planner_endpoint')
    lb_response = requests.get('http://' + lb_endpoint + ':8081/1/lb/nodes')
    n_nodes = len(lb_response.json().get('nodes'))
    n_estimators_per_node = n_estimators // n_nodes
    n_r_estimators = n_estimators % n_nodes

    logger.info('No. of estimators per node: ' + str(n_estimators_per_node))
    logger.info('No. of remainder estimators: ' + str(n_r_estimators))

    fit_async = []
    for i in range(n_nodes):
        if n_r_estimators > 0:
            n = n_estimators_per_node + 1
            n_r_estimators -= 1
        else:
            n = n_estimators_per_node

        estimator_params['n_estimators'] = n
        rfc = RandomForestClassifier(**estimator_params)
        estimator_client = EstimatorClient(lb_endpoint, '8081', False)

        fit_async.append(partial(estimator_client.fit, rfc, storage_client, train_data_object,
                                 model_object, n_outputs=body.get('n_outputs'),
                                 aggregate_models=body.get('aggregate_models')))
    logger.info('Initialised fit_async objects!!!')

    with concurrent.futures.ThreadPoolExecutor(max_workers=n_nodes) as executor:
        loop = asyncio.get_event_loop()
        futures = [
            loop.run_in_executor(
                executor,
                fit_async[i],
                i
            )
            for i in range(n_nodes)
        ]
        model_list = []
        for model in await asyncio.gather(*futures):
            model_list.append(model)
        if all(model is not None for model in model_list):
            return model_list[0]
        else:
            pass


async def handler(ctx, data=None, loop=None):
    if data and len(data) > 0:
        logger = get_logger(ctx)
        body = json.loads(data)

        logger.info('Resuming loop in handler!!!')
        if loop is None:
            loop = asyncio.get_event_loop()
            logger.info('Created new loop in handler!!!')

        model_object = await asyncio.ensure_future(planner(body, logger), loop=loop)
        logger.info('Loop completed in handler!!!')

        aggregate_models = body.get('aggregate_models')
        if aggregate_models:
            pass

    return json.dumps(model_object.__dict__)



if __name__ == "__main__":
    fdk.handle(handler)

