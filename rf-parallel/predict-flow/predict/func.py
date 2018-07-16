import fdk
import os
import json
import numpy as np
import pandas as pd
from predict_helper import *
from sklearn.externals import joblib
from functools import reduce


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

        # Parameters for the input testing dataset
        data_bucket_name = body.get('data_bucket_name')
        data_object_name = body.get('data_object_name')
        data_object_prefix_name = body.get('data_object_prefix_name')
        if data_object_prefix_name is not None:
            data_object_name = data_object_prefix_name + '/' + data_object_name
        data_file_delimiter = body.get('data_file_delimiter')

        # Parameters for the input model file
        fn_num = body.get('fn_num')
        model_object_bucket_name = body.get('model_object_bucket_name')
        model_object_prefix_name = body.get('model_object_prefix_name')
        model_object_prefix_name += '/model_'
        model_file_start_index = body.get('model_file_start')
        model_file_count = body.get('model_file_count')

        # Parameters for the output prediction file
        output_bucket_name = body.get('output_bucket_name')
        output_object_prefix_name = body.get('output_object_prefix_name')
        output_file_delimiter = body.get("output_file_delimiter")

        # Establishing connection to remote storage
        minio_client = minio_init_client(endpoint, access_key=access_key, secret_key=secret_key,
                                         secure=secure, region=region)

        # Creating directories in function's local storage
        if not os.path.exists('data'):
            os.mkdir('data')
            # Downloading input training dataset from remote storage
            minio_get_object(minio_client, data_bucket_name, data_object_name, 'data/test_data.csv', logger)
            logger.info('Downloaded file!')
        else:
            # Downloading input training dataset from remote storage
            if not os.path.exists('data/test_data.csv'):
                minio_get_object(minio_client, data_bucket_name, data_object_name, 'data/test_data.csv', logger)
                logger.info('Downloaded file!')

        if not os.path.exists('model'):
            os.mkdir('model')
        else:
            for the_file in os.listdir('model'):
                file_path = os.path.join('model', the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    logger.info('Unable to delete files in the model directory!')

        for i in range(model_file_start_index, model_file_start_index + model_file_count):
            model_object_name = model_object_prefix_name + str(i) + '.pkl'
            minio_get_object(minio_client, model_object_bucket_name, model_object_name,
                             'model/model_' + str(i) + '.pkl', logger)
        logger.info('Downloaded model!')

        if not os.path.exists('output'):
            os.mkdir('output')
        else:
            for the_file in os.listdir('output'):
                file_path = os.path.join('output', the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    logger.info('Unable to delete files in the output directory!')

        # Loading the input testing dataset into memory
        test_data = pd.read_csv('data/test_data.csv', sep=data_file_delimiter, header=None)
        test_X = np.array(test_data)
        logger.info('Loaded data!')

        # Loading the input model into memory
        rf_list = []
        for the_file in os.listdir('model'):
            file_path = os.path.join('model', the_file)
            rf_item = joblib.load(file_path)
            rf_list.append(rf_item)
        logger.info('Loaded model!')

        rf = reduce(combine_rfs, rf_list)

        # Predicting using the model for test data and persisting into local storage
        predictions = rf.predict_proba(test_X)

        if rf.n_outputs_ == 1:
            predictions *= rf.n_estimators
            np.savetxt('output/predictions.csv', predictions, delimiter=output_file_delimiter)
            logger.info('Finished predictions!')

            # Uploading the predictions into remote storage
            output_object_name = output_object_prefix_name + '/predictions_' + str(fn_num) + '.csv'
            minio_put_object(minio_client, output_bucket_name,  output_object_name, 'output/predictions.csv', logger)
            logger.info('Uploaded file to bucket: {0} with object name: {1}!'.format(output_bucket_name, output_object_name))
        else:
            for i, prediction in enumerate(predictions):
                prediction *= rf.n_estimators
                local_file_path = 'output/predictions_output_' + str(i) + '.csv'
                np.savetxt(local_file_path, prediction, delimiter=output_file_delimiter)
                logger.info('Finished predictions!')

                # Uploading the predictions into remote storage
                output_object_name = output_object_prefix_name + '/output_' + str(i) + '/predictions_' + str(fn_num) + '.csv'
                minio_put_object(minio_client, output_bucket_name, output_object_name, local_file_path, logger)
                logger.info('Uploaded file to bucket: {0} with object name: {1}!'.format(output_bucket_name,
                                                                                         output_object_name))
        return rf.n_outputs_, rf.n_estimators
    else:
        return {"message": "Data not sent!"}


if __name__ == "__main__":
    fdk.handle(handler)
