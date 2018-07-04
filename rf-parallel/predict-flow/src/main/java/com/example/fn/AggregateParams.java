package com.example.fn;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.io.Serializable;

@JsonIgnoreProperties(ignoreUnknown = true)
public class AggregateParams implements Serializable {
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

    @JsonProperty("output_bucket_name")
    private String outputBucketName;

    @JsonProperty("output_object_name_prefix")
    private String outputObjectNamePrefix;

    @JsonProperty("output_file_delimiter")
    private String outputFileDelimiter = ",";

    @JsonProperty("n_estimators")
    private Integer nEstimators;

    @JsonProperty("n_outputs")
    private Integer nOutputs;

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

    @JsonProperty("output_bucket_name")
    public String getOutputBucketName() {
        return outputBucketName;
    }

    @JsonProperty("output_bucket_name")
    public void setOutputBucketName(String outputBucketName) {
        this.outputBucketName = outputBucketName;
    }

    @JsonProperty("output_object_name_prefix")
    public String getOutputObjectNamePrefix() {
        return outputObjectNamePrefix;
    }

    @JsonProperty("output_object_name_prefix")
    public void setOutputObjectNamePrefix(String outputObjectNamePrefix) {
        this.outputObjectNamePrefix = outputObjectNamePrefix;
    }

    @JsonProperty("output_file_delimiter")
    public String getOutputFileDelimiter() {
        return outputFileDelimiter;
    }

    @JsonProperty("output_file_delimiter")
    public void setOutputFileDelimiter(String outputFileDelimiter) {
        this.outputFileDelimiter = outputFileDelimiter;
    }

    @JsonProperty("n_estimators")
    public Integer getnEstimators() {
        return nEstimators;
    }

    @JsonProperty("n_estimators")
    public void setnEstimators(Integer nEstimators) {
        this.nEstimators = nEstimators;
    }

    @JsonProperty("n_outputs")
    public Integer getnOutputs() {
        return nOutputs;
    }

    @JsonProperty("n_outputs")
    public void setnOutputs(Integer nOutputs) {
        this.nOutputs = nOutputs;
    }
}
