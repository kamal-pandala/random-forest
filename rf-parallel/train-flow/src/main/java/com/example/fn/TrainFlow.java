package com.example.fn;

import java.util.UUID;
import java.util.ArrayList;

import com.fnproject.fn.api.flow.FlowFuture;
import com.fnproject.fn.api.flow.HttpResponse;
import static com.fnproject.fn.api.flow.Flows.currentFlow;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class TrainFlow {

    static {
        System.setProperty("org.slf4j.simpleLogger.defaultLogLevel", "debug");
    }

    private static final Logger log = LoggerFactory.getLogger(TrainFlow.class);
    private static final int FUNCTION_LIMIT = 32;
    private static final int N_CORES_PER_FUNCTION = 1;

    public String handleRequest(TrainParams trainParams) {

        // Setting unique prefix for uploading model files
        String modelObjectPrefixName = UUID.randomUUID().toString();
        trainParams.setModelObjectPrefixName(modelObjectPrefixName);

        // Configuring no. of required functions and trees per function
        int nTreesRequired = trainParams.getEstimatorParams().getnEstimators();
        int nTreesPerFunction = 1;
        int nFunctionsRequired = nTreesRequired;
        int nRemainderTrees = 0;
        if (nTreesRequired > FUNCTION_LIMIT) {
            nTreesPerFunction = nTreesRequired / FUNCTION_LIMIT;
            nFunctionsRequired = FUNCTION_LIMIT;
            nRemainderTrees = nTreesRequired % FUNCTION_LIMIT;
        }

        // Setting no. of cores per function
        trainParams.getEstimatorParams().setnJobs(N_CORES_PER_FUNCTION);

        //TrainResponse trainResponse = new TrainResponse();

        // Creating clones of input params with fn_num as ID
        ArrayList<FlowFuture<HttpResponse>> trainParamsList = new ArrayList<>();
        for(int i = 0; i < nFunctionsRequired; i++) {
            trainParams.setFnNum(i);
            if (nRemainderTrees > 0) {
                trainParams.getEstimatorParams().setnEstimators(nTreesPerFunction + 1);
                nRemainderTrees--;
            } else {
                trainParams.getEstimatorParams().setnEstimators(nTreesPerFunction);
            }

            trainParamsList.add(currentFlow().invokeFunction("rf-parallel/train-flow/train",
                    trainParams));
        }


        currentFlow().allOf(trainParamsList.toArray(new FlowFuture[nFunctionsRequired]))
                .whenComplete((v, throwable) -> {
                    if (throwable != null) {
                        log.error("Failed!");

                        //trainResponse.setTrainSucess(false);
                    } else {
                        log.info("Success!");

                        //trainResponse.setTrainSucess(true);
                        //trainResponse.setModelObjectBucketName(trainParams.getModelObjectBucketName());
                        //trainResponse.setModelObjectPrefixName(modelObjectPrefixName);
                        //trainResponse.setModelObjectName();
                    }
                }).get();

        return modelObjectPrefixName;
    }

}