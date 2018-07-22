import fdk
import os
import json
import numpy as np
import pandas as pd
from train_helper import *
from sklearn.externals import joblib
from sklearn.ensemble import RandomForestClassifier


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

        # Parameters for the input training dataset
        data_bucket_name = body.get('data_bucket_name')
        data_object_name = body.get('data_object_name')
        data_object_prefix_name = body.get('data_object_prefix_name')
        if data_object_prefix_name is not None:
            data_object_name = data_object_prefix_name + '/' + data_object_name
        data_file_delimiter = body.get('data_file_delimiter')

        # Parameters for the output model file
        fn_num = body.get('fn_num')
        model_object_bucket_name = body.get('model_object_bucket_name')
        model_object_prefix_name = body.get('model_object_prefix_name')
        model_object_name = model_object_prefix_name + '/model_' + str(fn_num) + '.pkl'

        # Parameters for the Random Forest algorithm of scikit-learn
        estimator_params = body.get('estimator_params')
        for param_name in ["max_features", "min_samples_split", "min_samples_leaf"]:
            estimator_params = param_type_conversion(estimator_params, param_name)

        # Establishing connection to remote storage
        minio_client = minio_init_client(endpoint, access_key=access_key, secret_key=secret_key,
                                         secure=secure, region=region)

        # Creating directories in function's local  storage
        # Downloading input training dataset from remote storage
        if not os.path.exists('data'):
            os.mkdir('data')
            minio_get_object(minio_client, data_bucket_name, data_object_name, 'data/train_data.csv', logger)
            logger.info('Downloaded file!')
        else:

            if not os.path.exists('data/train_data.csv'):
                minio_get_object(minio_client, data_bucket_name, data_object_name, 'data/train_data.csv', logger)
                logger.info('Downloaded file!')

        # TODO - Delete folders as well
        # Cleaning up any existing model files and directories
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

        # Loading the input training dataset into memory
        train_data = pd.read_csv('data/train_data.csv', sep=data_file_delimiter, header=None)
        logger.info('Loaded file!')

        # Separation of the input training dataset into labels and features
        n_outputs = body.get('n_outputs')
        train_y = np.array(train_data.iloc[:, 0:n_outputs])
        train_X = np.array(train_data.drop(train_data.columns[0:n_outputs], axis=1))

        # Initialisation of the Random Forest algorithm with the estimator parameters
        if estimator_params is not None:
            rf = RandomForestClassifier(**estimator_params)
        else:
            rf = RandomForestClassifier()

        # Fitting the model to the input training data
        rf.fit(train_X, train_y)
        logger.info('Finished training!')

        # Persisting the model into function's local storage
        joblib.dump(rf, 'model/model.pkl')
        logger.info('Dumped model!')

        # Uploading the model into remote storage
        minio_put_object(minio_client, model_object_bucket_name,  model_object_name, 'model/model.pkl', logger)
        logger.info('Uploaded file to bucket: {0} with object name: {1}!'.format(model_object_bucket_name, model_object_name))

        # TODO - Return codes
        return {"message": "Completed successfully!!!"}
    else:
        return {"message": "Data not sent!"}


if __name__ == "__main__":
    fdk.handle(handler)
