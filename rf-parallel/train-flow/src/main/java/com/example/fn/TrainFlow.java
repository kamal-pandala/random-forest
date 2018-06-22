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
        System.setProperty("org.slf4j.simpleLogger.defaultLogLevel", "info");
    }

    private static final Logger log = LoggerFactory.getLogger(TrainFlow.class);
    private static final int FUNCTION_LIMIT = 4;
    private static final int N_CORES_PER_FUNCTION = 1;

    public void handleRequest(TrainParams trainParams) {

        // Configuring no. of required functions and trees per function
        int nTreesRequired = trainParams.getEstimatorParams().getnEstimators();
        int nTreesPerFunction = 1;
        int nFunctionsRequired = nTreesRequired;
        if (nTreesRequired > FUNCTION_LIMIT) {
            nTreesPerFunction = nTreesRequired / FUNCTION_LIMIT;
            nFunctionsRequired = FUNCTION_LIMIT;
        }
        trainParams.getEstimatorParams().setnEstimators(nTreesPerFunction);

        // Setting no. of cores per function
        trainParams.getEstimatorParams().setnJobs(N_CORES_PER_FUNCTION);

        // Setting unique prefix for uploading model files
        String modelObjectNamePrefix = UUID.randomUUID().toString();
        trainParams.setModelObjectNamePrefix(modelObjectNamePrefix);

        // Creating clones of input params with fn_num as ID
        ArrayList<FlowFuture<HttpResponse>> trainParamsList = new ArrayList<>();
        for(int i = 0; i < nFunctionsRequired; i++) {
            trainParams.setFnNum(i);
            trainParamsList.add(currentFlow().invokeFunction("rf-parallel/train-flow/train", trainParams));
        }

        currentFlow().allOf(trainParamsList.toArray(new FlowFuture[nFunctionsRequired]))
                .whenComplete((v, throwable) -> {
                    if (throwable != null) {
                        log.error("Failed!");
                    } else {
                        log.info("Success!");
                    }
                });
    }

}