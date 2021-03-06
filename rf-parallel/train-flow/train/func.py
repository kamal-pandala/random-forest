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

        # Parameters for the input training dataset
        data_bucket_name = body.get('data_bucket_name')
        data_object_name = body.get('data_object_name')
        data_object_prefix_name = body.get('data_object_prefix_name')
        if data_object_prefix_name is not None:
            data_object_name = data_object_prefix_name + '/' + data_object_name
        data_file_delimiter = body.get('data_file_delimiter')

        # TODO - check type compatibility of scikit's RF implementation
        # Parameters for the Random Forest algorithm of scikit-learn
        estimator_params = body.get('estimator_params')
        for param_name in ['max_features', 'min_samples_split', 'min_samples_leaf']:
            estimator_params = param_type_conversion(estimator_params, param_name)

        # Parameters for the output model file
        model_object_bucket_name = body.get('model_object_bucket_name')
        model_object_prefix_name = body.get('model_object_prefix_name')
        file_num = str(node_number) + '_' + str(fn_num)
        model_object_name = model_object_prefix_name + '/model_' + file_num + '.pkl'

        # Establishing connection to remote storage
        minio_client = minio_init_client(endpoint, access_key=access_key, secret_key=secret_key,
                                         secure=secure, region=region)

        # Unique ID for storing the dataset locally - useful in case of hot functions
        local_dataset_name = body.get('data_local_name') + '.csv'

        # Creating directories in function's local  storage
        # Downloading input training dataset from remote storage
        if not os.path.exists('/tmp'):
            os.mkdir('/tmp')

        if not os.path.exists('/tmp/data'):
            os.mkdir('/tmp/data')
            minio_get_object(minio_client, data_bucket_name, data_object_name, '/tmp/data/' + local_dataset_name, logger)
            logger.info('Downloaded the input training data file!')
        else:

            if not os.path.exists('/tmp/data/train_data.csv'):
                minio_get_object(minio_client, data_bucket_name, data_object_name, '/tmp/data/' + local_dataset_name, logger)
                logger.info('Downloaded the input training data file!')

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
                except Exception as e:
                    logger.info('Unable to delete files in the model directory!')

        # Loading the input training dataset into memory
        train_data = pd.read_csv('/tmp/data/' + local_dataset_name, sep=data_file_delimiter, header=None)
        logger.info('Loaded the input training data into memory!')

        # Separation of the input training dataset into labels and features
        n_outputs = body.get('n_outputs')
        train_y = np.array(train_data.iloc[:, 0:n_outputs])
        train_X = np.array(train_data.drop(train_data.columns[0:n_outputs], axis=1))
        logger.info('Finished pre-processing the data!')

        # Initialisation of the Random Forest algorithm with the estimator parameters
        if estimator_params is not None:
            rf = RandomForestClassifier(**estimator_params)
        else:
            rf = RandomForestClassifier()

        # Fitting the model to the input training data
        rf.fit(train_X, train_y)
        logger.info('Finished fitting the model!')

        # Persisting the model into function's local storage
        joblib.dump(rf, '/tmp/model/model.pkl')
        logger.info('Persisted the model locally!')

        # Uploading the model into remote storage
        minio_put_object(minio_client, model_object_bucket_name,  model_object_name, '/tmp/model/model.pkl', logger)
        logger.info('Uploaded the model file to bucket: {0} with object name: {1}!'.format(model_object_bucket_name,
                                                                                 model_object_name))

        # TODO - Return codes
        return {"message": "Completed successfully!!!"}
    else:
        return {"message": "Data not sent!"}


if __name__ == "__main__":
    fdk.handle(handler)
