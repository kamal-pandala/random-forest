import fdk
import json
import asyncio
import uvloop
import requests
import concurrent.futures
from helper import *
from functools import partial


async def planner(body, loop):
    estimator_params = body.get('estimator_params')
    n_estimators = estimator_params['n_estimators']

    storage_client = StorageClient(body.get('endpoint'), body.get('port'), body.get('access_key'),
                                   body.get('secret_key'), body.get('secure'))
    train_data_object = DataObject(body.get('data_bucket_name'), body.get('data_object_name'))
    model_object = ModelObject(body.get('model_object_bucket_name'))

    lb_endpoint = body.get('lb_planner_endpoint')
    lb_response = requests.get('http://' + lb_endpoint + ':8081/1/lb/nodes')
    n_nodes = len(lb_response.json().get('nodes'))
    n_estimators_per_node = n_estimators // n_nodes
    n_r_estimators = n_estimators % n_nodes

    fit_async = []
    n_list = [0]
    for i in range(n_nodes):
        if n_r_estimators > 0:
            n = n_estimators_per_node + 1
            n_r_estimators -= 1
        else:
            n = n_estimators_per_node

        n_list.append(n + n_list[-1])

        estimator_params['n_estimators'] = n
        rfc = RandomForestClassifier(**estimator_params)
        estimator_client = EstimatorClient(lb_endpoint, '8081', False)

        fit_async.append(partial(estimator_client.fit, rfc, storage_client, train_data_object,
                                 model_object, n_outputs=body.get('n_outputs'),
                                 aggregate_models=body.get('aggregate_models')))

    with concurrent.futures.ThreadPoolExecutor(max_workers=n_nodes) as executor:
        # loop = asyncio.get_event_loop()
        futures = [
            loop.run_in_executor(
                executor,
                fit_async[i],
                n_list[i]
            )
            for i in range(n_nodes)
        ]
        for response in await asyncio.gather(*futures):
            print(response)


def handler(ctx, data=None, loop=None):
    if data and len(data) > 0:
        body = json.loads(data)

        if loop is None:
            asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
            loop = asyncio.get_event_loop()
        loop.run_until_complete(planner(body, loop))

    return {"message": "Hello"}



if __name__ == "__main__":
    fdk.handle(handler)

