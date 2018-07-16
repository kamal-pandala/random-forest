package com.example.fn;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.io.Serializable;

@JsonIgnoreProperties(ignoreUnknown = true)
public class TrainParams implements Serializable {
    @JsonProperty("fn_num")
    private Integer fnNum;

    @JsonProperty("endpoint")
    private String endpoint;

    @JsonProperty("port")
    private int port = 0;

    @JsonProperty("access_key")
    private String accessKey;

    @JsonProperty("secret_key")
    private String secretKey;

    @JsonProperty("secure")
    private Boolean secure = true;

    @JsonProperty("region")
    private String region;

    @JsonProperty("data_bucket_name")
    private String dataBucketName;

    @JsonProperty("data_object_name")
    private String dataObjectName;

    @JsonProperty("data_object_prefix_name")
    private String dataObjectPrefixName;

    @JsonProperty("data_file_delimiter")
    private String dataFileDelimiter = ",";

    @JsonProperty("model_object_bucket_name")
    private String modelObjectBucketName;

    @JsonProperty("model_object_prefix_name")
    private String modelObjectPrefixName;

    @JsonProperty("estimator_params")
    private EstimatorParams estimatorParams;

    @JsonProperty("n_outputs")
    private Integer nOutputs = 1;

    @JsonProperty("aggregate_models")
    private Boolean aggregateModels = false;

    @JsonProperty("fn_num")
    public Integer getFnNum() {
        return fnNum;
    }

    @JsonProperty("fn_num")
    public void setFnNum(Integer fnNum) {
        this.fnNum = fnNum;
    }

    @JsonProperty("endpoint")
    public String getEndpoint() {
        return endpoint;
    }

    @JsonProperty("endpoint")
    public void setEndpoint(String endpoint) {
        this.endpoint = endpoint;
    }

    @JsonProperty("port")
    public int getPort() {
        return port;
    }

    @JsonProperty("port")
    public void setPort(int port) {
        this.port = port;
    }

    @JsonProperty("access_key")
    public String getAccessKey() {
        return accessKey;
    }

    @JsonProperty("access_key")
    public void setAccessKey(String accessKey) {
        this.accessKey = accessKey;
    }

    @JsonProperty("secret_key")
    public String getSecretKey() {
        return secretKey;
    }

    @JsonProperty("secret_key")
    public void setSecretKey(String secretKey) {
        this.secretKey = secretKey;
    }

    @JsonProperty("secure")
    public Boolean getSecure() {
        return secure;
    }

    @JsonProperty("secure")
    public void setSecure(Boolean secure) {
        this.secure = secure;
    }

    @JsonProperty("region")
    public String getRegion() {
        return region;
    }

    @JsonProperty("region")
    public void setRegion(String region) {
        this.region = region;
    }

    @JsonProperty("data_bucket_name")
    public String getDataBucketName() {
        return dataBucketName;
    }

    @JsonProperty("data_bucket_name")
    public void setDataBucketName(String dataBucketName) {
        this.dataBucketName = dataBucketName;
    }

    @JsonProperty("data_object_name")
    public String getDataObjectName() {
        return dataObjectName;
    }

    @JsonProperty("data_object_name")
    public void setDataObjectName(String dataObjectName) {
        this.dataObjectName = dataObjectName;
    }

    @JsonProperty("data_object_prefix_name")
    public String getDataObjectPrefixName() {
        return dataObjectPrefixName;
    }

    @JsonProperty("data_object_prefix_name")
    public void setDataObjectPrefixName(String dataObjectPrefixName) {
        this.dataObjectPrefixName = dataObjectPrefixName;
    }

    @JsonProperty("data_file_delimiter")
    public String getDataFileDelimiter() {
        return dataFileDelimiter;
    }

    @JsonProperty("data_file_delimiter")
    public void setDataFileDelimiter(String dataFileDelimiter) {
        this.dataFileDelimiter = dataFileDelimiter;
    }

    @JsonProperty("model_object_bucket_name")
    public String getModelObjectBucketName() {
        return modelObjectBucketName;
    }

    @JsonProperty("model_object_bucket_name")
    public void setModelObjectBucketName(String modelObjectBucketName) {
        this.modelObjectBucketName = modelObjectBucketName;
    }

    @JsonProperty("model_object_prefix_name")
    public String getModelObjectPrefixName() {
        return modelObjectPrefixName;
    }

    @JsonProperty("model_object_prefix_name")
    public void setModelObjectPrefixName(String modelObjectPrefixName) {
        this.modelObjectPrefixName = modelObjectPrefixName;
    }

    @JsonProperty("estimator_params")
    public EstimatorParams getEstimatorParams() {
        return estimatorParams;
    }

    @JsonProperty("estimator_params")
    public void setEstimatorParams(EstimatorParams estimatorParams) {
        this.estimatorParams = estimatorParams;
    }

    @JsonProperty("n_outputs")
    public Integer getnOutputs() {
        return nOutputs;
    }

    @JsonProperty("n_outputs")
    public void setnOutputs(Integer nOutputs) {
        this.nOutputs = nOutputs;
    }

    @JsonProperty("aggregate_models")
    public Boolean getAggregateModels() {
        return aggregateModels;
    }

    @JsonProperty("aggregate_models")
    public void setAggregateModels(Boolean aggregateModels) {
        this.aggregateModels = aggregateModels;
    }
}
