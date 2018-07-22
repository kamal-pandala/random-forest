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
        if not os.path.exists('output'):
            os.mkdir('output')
        else:
            for the_file in os.listdir('output'):
                file_path = os.path.join('output', the_file)
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
        logger.info('Downloaded the prediction files!')

        if n_outputs == 1:
            minio_get_all_objects(minio_client, output_bucket_name, output_object_prefix_name,
                                  'output', logger)

            # Deleting previously existing aggregated predictions file if any
            if os.path.isfile('output/final_predictions.csv'):
                os.unlink('output/final_predictions.csv')

            # Loading all the predictions files into memory
            predictions = []
            for the_file in os.listdir('output'):
                file_path = os.path.join('output', the_file)
                try:
                    if os.path.isfile(file_path):
                        predictions.append(np.array(pd.read_csv(file_path, sep=output_file_delimiter, header=None)))
                except Exception as e:
                    logger.info('Unable to read files in the output directory!')
            logger.info('Loaded the prediction files!')

            # Combining and normalising the predictions over the number of estimators
            combined_prediction = reduce(combine_predictions, predictions)
            combined_prediction /= n_estimators
            logger.info('Combined the predictions!')

            # Assigning labels to the maximum probable score
            final_prediction = np.argmax(combined_prediction, axis=1)

            # Persisting the final aggregated predictions file
            np.savetxt('output/final_predictions.csv', final_prediction, delimiter=output_file_delimiter)
            minio_put_object(minio_client, output_bucket_name, output_object_prefix_name + '/final_predictions.csv',
                             'output/final_predictions.csv', logger)
            logger.info('Uploaded the final prediction file!')
        else:
            # Downloading all the predictions files into memory for each output at a time
            multioutput_predictions = []
            for i in range(n_outputs):
                os.mkdir('output/output_' + str(i))
                minio_get_all_objects(minio_client, output_bucket_name, output_object_prefix_name + '/output_' + str(i),
                                      'output/output_' + str(i), logger)

                # Loading all the predictions files into memory
                predictions = []
                for the_file in os.listdir('output/output_' + str(i)):
                    file_path = os.path.join('output/output_' + str(i), the_file)
                    try:
                        if os.path.isfile(file_path):
                            predictions.append(np.array(pd.read_csv(file_path, sep=output_file_delimiter, header=None)))
                    except Exception as e:
                        logger.info('Unable to read files in the output directory!')

                # Combining and normalising the predictions over the number of estimators
                combined_prediction = reduce(combine_predictions, predictions)
                combined_prediction /= n_estimators

                # Assigning labels to the maximum probable score
                final_prediction = np.argmax(combined_prediction, axis=1)
                multioutput_predictions.append(final_prediction)

            # Combining the predictions of multiple outputs into a single file
            final_predictions = reduce(concatenate_multioutput_predictions, multioutput_predictions)

            # Persisting the final aggregated predictions file
            np.savetxt('output/final_predictions.csv', final_predictions, delimiter=output_file_delimiter)
            minio_put_object(minio_client, output_bucket_name, output_object_prefix_name + '/final_predictions.csv',
                             'output/final_predictions.csv', logger)

        return {"message": "Completed successfully!!!"}
    else:
        return {"message": "Data not sent!"}



if __name__ == "__main__":
    fdk.handle(handler)

