import fdk
import os
import json
import numpy as np
import pandas as pd
from predict_helper import *
from sklearn.externals import joblib
from sklearn.ensemble import RandomForestClassifier


def handler(ctx, data=None, loop=None):
    if data and len(data) > 0:
        logger = get_logger(ctx)
        body = json.loads(data)

        endpoint = body.get('endpoint')
        access_key = body.get('access_key')
        secret_key = body.get('secret_key')
        # TODO - more values to to fetch and validation

        data_bucket_name = body.get('data_bucket_name')
        data_object_name = body.get('data_object_name')
        data_file_delimiter = body.get('data_file_delimiter')
        if data_file_delimiter is None:
            data_file_delimiter = ','

        fn_num = body.get('fn_num')
        model_bucket_name = body.get('model_bucket_name')
        model_object_name_prefix = body.get('model_object_name_prefix')
        model_object_name = model_object_name_prefix + '/model_' + str(fn_num) + '.pkl'

        output_bucket_name = body.get('output_bucket_name')
        output_object_name_prefix = body.get('output_object_name_prefix')
        output_object_name = output_object_name_prefix + '/predictions_' + str(fn_num) + '.csv'

        os.mkdir('data')
        os.mkdir('model')
        os.mkdir('output')

        minio_client = minio_init_client(endpoint, access_key=access_key, secret_key=secret_key, secure=False)

        minio_get_object(minio_client, model_bucket_name, model_object_name, 'model/model.pkl', logger)
        logger.info('Downloaded model!')

        rf = joblib.load('model/model.pkl')
        logger.info('Loaded model!')

        minio_get_object(minio_client, data_bucket_name, data_object_name, 'data/test_data.csv', logger)
        logger.info('Downloaded data!')

        test_data = pd.read_csv('data/test_data.csv', sep=data_file_delimiter, header=None)
        test_X = np.array(test_data)
        logger.info('Loaded data!')

        predictions = rf.predict(test_X)
        np.savetxt('output/predictions.csv', predictions, delimiter=',')
        logger.info('Finished predictions!')

        minio_put_object(minio_client, output_bucket_name,  output_object_name, 'output/predictions.csv', logger)
        logger.info('Uploaded file to bucket: {0} with object name: {1}!'.format(output_bucket_name, output_object_name))

        return {"message": "Completed successfully!!!"}
    else:
        return {"message": "Data not sent!"}


if __name__ == "__main__":
    fdk.handle(handler)
