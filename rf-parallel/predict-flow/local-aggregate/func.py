import fdk
import os
import json
import shutil
import numpy as np
import pandas as pd
from functools import reduce
from aggregate_helper import *


def handler(ctx, data=None, loop=None):
    if data and len(data) > 0:
        logger = get_logger(ctx)
        body = json.loads(data)

        node_number = body.get('node_number')
        logger.info('Aggregate function on node {0} has started running!'.format(node_number))

        # TODO - validation and exception handling
        # Parameters required for initialising minio client
        endpoint = body.get('endpoint')
        port = body.get('port')
        if port is not None and port != 0:
            endpoint += ':' + str(port)

        access_key = body.get('access_key')
        secret_key = body.get('secret_key')
        secure = body.get('secure')
        region = body.get('region')

        # Parameters for the output prediction file
        output_bucket_name = body.get('output_bucket_name')
        output_object_prefix_name = body.get('output_object_prefix_name')
        output_file_delimiter = body.get("output_file_delimiter")

        # Parameters of the problem
        n_estimators = body.get('n_estimators')
        n_outputs = body.get('n_outputs')

        # Cleaning up any existing output files and directories
        if not os.path.exists('/tmp'):
            os.mkdir('/tmp')

        if not os.path.exists('/tmp/output'):
            os.mkdir('/tmp/output')
        else:
            for the_file in os.listdir('/tmp/output'):
                file_path = os.path.join('/tmp/output', the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    logger.info('Unable to delete files in the output directory!')

        # Establishing connection to remote storage
        minio_client = minio_init_client(endpoint, access_key=access_key, secret_key=secret_key,
                                         secure=secure, region=region)

        if n_outputs == 1:
            minio_get_all_objects(minio_client, output_bucket_name, output_object_prefix_name + '/' + node_number,
                                  '/tmp/output', logger)
            logger.info('Downloaded the prediction files!')

            # Loading all the predictions files into memory
            predictions = []
            for the_file in os.listdir('/tmp/output'):
                file_path = os.path.join('/tmp/output', the_file)
                try:
                    if os.path.isfile(file_path):
                        predictions.append(np.array(pd.read_csv(file_path, sep=output_file_delimiter, header=None)))
                except Exception as e:
                    logger.info('Unable to read files in the output directory!')
            logger.info('Loaded the prediction files!')

            # Combining and normalising the predictions over the number of estimators
            combined_prediction = reduce(combine_predictions, predictions)
            logger.info('Combined the predictions!')

            # Persisting the final aggregated predictions file
            np.savetxt('/tmp/output/local_predictions.csv', combined_prediction, delimiter=output_file_delimiter)
            minio_put_object(minio_client, output_bucket_name,
                             output_object_prefix_name + '/local/local_predictions_' + node_number + '.csv',
                             '/tmp/output/local_predictions.csv', logger)
            logger.info('Uploaded the local prediction file!')
        else:
            # Downloading all the predictions files into memory for each output at a time
            for i in range(n_outputs):
                os.mkdir('/tmp/output/output_' + str(i))
                minio_get_all_objects(minio_client, output_bucket_name,
                                      output_object_prefix_name + '/' + node_number + '/output_' + str(i),
                                      '/tmp/output/output_' + str(i), logger)

                # Loading all the predictions files into memory
                predictions = []
                for the_file in os.listdir('/tmp/output/output_' + str(i)):
                    file_path = os.path.join('/tmp/output/output_' + str(i), the_file)
                    try:
                        if os.path.isfile(file_path):
                            predictions.append(np.array(pd.read_csv(file_path, sep=output_file_delimiter, header=None)))
                    except Exception as e:
                        logger.info('Unable to read files in the output directory!')

                # Combining and normalising the predictions over the number of estimators
                combined_prediction = reduce(combine_predictions, predictions)

                # Persisting the final aggregated predictions file
                np.savetxt('/tmp/output/local_predictions_' + str(i) + '.csv', combined_prediction, delimiter=output_file_delimiter)
                minio_put_object(minio_client, output_bucket_name,
                                 output_object_prefix_name + '/local/output_' + str(i) + '/local_predictions_' + node_number + '.csv',
                                 '/tmp/output/local_predictions_' + str(i) + '.csv', logger)

        return n_outputs, n_estimators
    else:
        return {"message": "Data not sent!"}



if __name__ == "__main__":
    fdk.handle(handler)

