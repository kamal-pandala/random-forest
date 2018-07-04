package com.example.fn;

import java.util.UUID;
import java.util.ArrayList;

import com.fnproject.fn.api.flow.FlowFuture;
import com.fnproject.fn.api.flow.HttpResponse;
import static com.fnproject.fn.api.flow.Flows.currentFlow;

import com.google.common.collect.Iterables;
import io.minio.MinioClient;
import io.minio.Result;
import io.minio.errors.MinioException;
import io.minio.messages.Item;
import org.apache.http.client.methods.HttpOptions;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class PredictFlow {

    static {
        System.setProperty("org.slf4j.simpleLogger.defaultLogLevel", "debug");
    }

    private static final Logger log = LoggerFactory.getLogger(PredictFlow.class);
    private static final int FUNCTION_LIMIT = 16;

    public static MinioClient getMinioClient(String endpoint, int port, String accessKey, String secretKey,
                                             String region, boolean secure) {
        MinioClient minioClient = null;
        try {
            minioClient = new MinioClient(endpoint, port, accessKey, secretKey, region, secure);
        } catch (MinioException e) {
            log.error("Error occurred: " + e);
        }
        return minioClient;
    }

    public Integer getModelFileCount(MinioClient minioClient, String bucketName, String prefix) {
        Integer modelFileCount = null;
        try {
            // Check whether bucket exists or not.
            boolean found = minioClient.bucketExists(bucketName);
            if (found) {
                // List objects from the bucket
                Iterable<Result<Item>> objects = minioClient.listObjects(bucketName, prefix, true, false);
                modelFileCount = Iterables.size(objects);
            } else {
                log.error("Model bucket: {} does not exist", bucketName);
            }
        } catch (Exception e) {
            log.error("Error occurred: " + e);
        }
        return modelFileCount;
    }

    public void handleRequest(PredictParams predictParams) {

        // Setting unique prefix for uploading output files
        String outputObjectNamePrefix = UUID.randomUUID().toString();
        predictParams.setOutputObjectNamePrefix(outputObjectNamePrefix);

        MinioClient minioClient = getMinioClient(predictParams.getEndpoint(), predictParams.getPort(),
                predictParams.getAccessKey(), predictParams.getSecretKey(),
                predictParams.getRegion(), predictParams.getSecure());
        Integer modelFileCount = getModelFileCount(minioClient, predictParams.getModelBucketName(),
                predictParams.getModelObjectNamePrefix());

        // Configuring no. of required functions and predictions per function
        int nPredictionsPerFunction = 1;
        int nFunctionsRequired = modelFileCount;
        int nRemainderPredictions = 0;
        if (nFunctionsRequired > FUNCTION_LIMIT) {
            nPredictionsPerFunction = nFunctionsRequired / FUNCTION_LIMIT;
            nFunctionsRequired = FUNCTION_LIMIT;
            nRemainderPredictions = nFunctionsRequired % FUNCTION_LIMIT;
        }

        // Creating clones of input params with fn_num as ID
        ArrayList<FlowFuture<HttpResponse>> predictParamsList = new ArrayList<>();
        int currentIndex = 0;
        for(int i = 0; i < nFunctionsRequired; i++) {
            predictParams.setFnNum(i);
            if (nRemainderPredictions > 0) {
                predictParams.setModelFileStart(currentIndex);
                predictParams.setModelFileCount(nPredictionsPerFunction + 1);
                nRemainderPredictions--;
                currentIndex += nPredictionsPerFunction + 1;
            } else {
                predictParams.setModelFileStart(currentIndex);
                predictParams.setModelFileCount(nPredictionsPerFunction);
                currentIndex += nPredictionsPerFunction;
            }
            predictParamsList.add(currentFlow().invokeFunction("rf-parallel/predict-flow/predict",
                    predictParams));
        }

        currentFlow().allOf(predictParamsList.toArray(new FlowFuture[nFunctionsRequired]))
                .whenComplete((v, throwable) -> {
                    if (throwable != null) {
                        log.error("Failed!");
                    } else {
                        log.info("Success!");

                        int n_estimators = 0;
                        int n_outputs = 0;
                        for (FlowFuture<HttpResponse> future : predictParamsList) {
                            String predictionResponse = new String(future.get().getBodyAsBytes());
                            predictionResponse = predictionResponse.substring(1, predictionResponse.length() - 1);
                            String[] predictionAttrs = predictionResponse.split(",");
                            if (n_outputs < 1) {
                                n_outputs = Integer.parseInt(predictionAttrs[0]);
                            }
                            n_estimators += Integer.parseInt(predictionAttrs[1]);
                        }

                        AggregateParams aggregateParams = new AggregateParams();
                        aggregateParams.setEndpoint(predictParams.getEndpoint());
                        aggregateParams.setPort(predictParams.getPort());
                        aggregateParams.setAccessKey(predictParams.getAccessKey());
                        aggregateParams.setSecretKey(predictParams.getSecretKey());
                        aggregateParams.setSecure(predictParams.getSecure());
                        aggregateParams.setRegion(predictParams.getRegion());
                        aggregateParams.setOutputBucketName(predictParams.getOutputBucketName());
                        aggregateParams.setOutputObjectNamePrefix(outputObjectNamePrefix);
                        aggregateParams.setOutputFileDelimiter(predictParams.getOutputFileDelimiter());
                        aggregateParams.setnEstimators(n_estimators);
                        aggregateParams.setnOutputs(n_outputs);

                        currentFlow().invokeFunction("rf-parallel/predict-flow/aggregate",
                                aggregateParams);
                    }
                });

    }

}