import fdk
import os
import json
import shutil
import numpy as np
import pandas as pd
from predict_helper import *
from sklearn.externals import joblib
from functools import reduce


def handler(ctx, data=None, loop=None):
    if data and len(data) > 0:
        logger = get_logger(ctx)
        body = json.loads(data)

        fn_num = body.get('fn_num')
        node_number = body.get('node_number')
        logger.info('Function {0} on node {1} has started running!'.format(fn_num, node_number))

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

        # Parameters for the input prediction dataset
        data_bucket_name = body.get('data_bucket_name')
        data_object_name = body.get('data_object_name')
        data_object_prefix_name = body.get('data_object_prefix_name')
        if data_object_prefix_name is not None:
            data_object_name = data_object_prefix_name + '/' + data_object_name
        data_file_delimiter = body.get('data_file_delimiter')

        # Parameters for the input model file
        model_object_bucket_name = body.get('model_object_bucket_name')
        model_object_prefix_name = body.get('model_object_prefix_name')
        model_file_start_index = body.get('model_file_start')
        model_file_count = body.get('model_file_count')

        # Parameters for the output prediction file
        output_bucket_name = body.get('output_bucket_name')
        output_object_prefix_name = body.get('output_object_prefix_name')
        output_file_delimiter = body.get("output_file_delimiter")

        # Establishing connection to remote storage
        minio_client = minio_init_client(endpoint, access_key=access_key, secret_key=secret_key,
                                         secure=secure, region=region)

        # Unique ID for storing the dataset locally - useful in case of hot functions
        local_dataset_name = body.get('data_local_name') + '.csv'

        # Creating directories in function's local storage
        # Downloading input prediction dataset from remote storage
        if not os.path.exists('/tmp'):
            os.mkdir('/tmp')

        if not os.path.exists('/tmp/data'):
            os.mkdir('/tmp/data')
            minio_get_object(minio_client, data_bucket_name, data_object_name, '/tmp/data/' + local_dataset_name, logger)
            logger.info('Downloaded file!')
        else:
            if not os.path.exists('/tmp/data/test_data.csv'):
                minio_get_object(minio_client, data_bucket_name, data_object_name, '/tmp/data/' + local_dataset_name, logger)
                logger.info('Downloaded file!')

        # TODO - Delete folders as well
        # Cleaning up any existing model files and directories
        if not os.path.exists('/tmp/model'):
            os.mkdir('/tmp/model')
        else:
            for the_file in os.listdir('/tmp/model'):
                file_path = os.path.join('/tmp/model', the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    logger.info('Unable to delete files in the model directory!')

        # Downloading the fitted model files
        minio_get_objects_in_range(minio_client, model_object_bucket_name, model_object_prefix_name,
                                   '/tmp/model', model_file_start_index, model_file_count, logger)
        logger.info('Downloaded models!')

        # Cleaning up any existing output files and directories
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

        # Loading the input prediction dataset into memory
        test_data = pd.read_csv('/tmp/data/' + local_dataset_name, sep=data_file_delimiter, header=None)
        test_X = np.array(test_data)
        logger.info('Loaded data!')

        # Loading the input model files into memory
        rf_list = []
        for the_file in os.listdir('/tmp/model'):
            file_path = os.path.join('/tmp/model', the_file)
            rf_item = joblib.load(file_path)
            rf_list.append(rf_item)
        logger.info('Loaded model!')

        # Combining the models in memory into one model for prediction
        rf = reduce(combine_rfs, rf_list)

        # Predicting probabilities using the combined model for prediction data
        predictions = rf.predict_proba(test_X)

        # Processing and persisting based on number of outputs in the job
        if rf.n_outputs_ == 1:
            predictions *= rf.n_estimators
            np.savetxt('/tmp/output/predictions.csv', predictions, delimiter=output_file_delimiter)
            logger.info('Finished predictions!')

            # Uploading the prediction file into remote storage
            output_object_name = output_object_prefix_name + '/' + node_number + '/predictions_' + str(fn_num) + '.csv'
            minio_put_object(minio_client, output_bucket_name, output_object_name, '/tmp/output/predictions.csv', logger)
            logger.info('Uploaded file to bucket: {0} with object name: {1}!'
                        .format(output_bucket_name, output_object_name))
        else:
            for i, prediction in enumerate(predictions):
                prediction *= rf.n_estimators
                local_file_path = '/tmp/output/predictions_output_' + str(i) + '.csv'
                np.savetxt(local_file_path, prediction, delimiter=output_file_delimiter)
                logger.info('Finished predictions!')

                # Uploading the multiple prediction files into remote storage
                output_object_name = output_object_prefix_name + '/' + node_number + '/output_' + str(i) + '/predictions_' \
                                     + str(fn_num) + '.csv'
                minio_put_object(minio_client, output_bucket_name, output_object_name, local_file_path, logger)
                logger.info('Uploaded file to bucket: {0} with object name: {1}!'
                            .format(output_bucket_name, output_object_name))

        return rf.n_outputs_, rf.n_estimators
    else:
        return {"message": "Data not sent!"}


if __name__ == "__main__":
    fdk.handle(handler)
