package com.example.fn;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.io.Serializable;

@JsonIgnoreProperties(ignoreUnknown = true)
public class PredictParams implements Serializable {
    @JsonProperty("node_number")
    private String nodeNumber;

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

    @JsonProperty("data_local_name")
    private String dataLocalName;

    @JsonProperty("model_object_bucket_name")
    private String modelObjectBucketName;

    @JsonProperty("model_object_prefix_name")
    private String modelObjectPrefixName;

    @JsonProperty("model_file_start")
    private Integer modelFileStart;

    @JsonProperty("model_file_count")
    private Integer modelFileCount;

    @JsonProperty("output_bucket_name")
    private String outputBucketName;

    @JsonProperty("output_object_prefix_name")
    private String outputObjectPrefixName;

    @JsonProperty("output_file_delimiter")
    private String outputFileDelimiter = ",";

    @JsonProperty("node_number")
    public String getNodeNumber() {
        return nodeNumber;
    }

    @JsonProperty("node_number")
    public void setNodeNumber(String nodeNumber) {
        this.nodeNumber = nodeNumber;
    }

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

    @JsonProperty("data_local_name")
    public String getDataLocalName() {
        return dataLocalName;
    }

    @JsonProperty("data_local_name")
    public void setDataLocalName(String dataLocalName) {
        this.dataLocalName = dataLocalName;
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

    @JsonProperty("model_file_start")
    public Integer getModelFileStart() {
        return modelFileStart;
    }

    @JsonProperty("model_file_start")
    public void setModelFileStart(Integer modelFileStart) {
        this.modelFileStart = modelFileStart;
    }

    @JsonProperty("model_file_count")
    public Integer getModelFileCount() {
        return modelFileCount;
    }

    @JsonProperty("model_file_count")
    public void setModelFileCount(Integer modelFileCount) {
        this.modelFileCount = modelFileCount;
    }

    @JsonProperty("output_bucket_name")
    public String getOutputBucketName() {
        return outputBucketName;
    }

    @JsonProperty("output_bucket_name")
    public void setOutputBucketName(String outputBucketName) {
        this.outputBucketName = outputBucketName;
    }

    @JsonProperty("output_object_prefix_name")
    public String getOutputObjectPrefixName() {
        return outputObjectPrefixName;
    }

    @JsonProperty("output_object_prefix_name")
    public void setOutputObjectPrefixName(String outputObjectPrefixName) {
        this.outputObjectPrefixName = outputObjectPrefixName;
    }

    @JsonProperty("output_file_delimiter")
    public String getOutputFileDelimiter() {
        return outputFileDelimiter;
    }

    @JsonProperty("output_file_delimiter")
    public void setOutputFileDelimiter(String outputFileDelimiter) {
        this.outputFileDelimiter = outputFileDelimiter;
    }
}
