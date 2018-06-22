package com.example.fn;

import java.util.List;
import java.util.HashMap;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;

@JsonIgnoreProperties(ignoreUnknown = true)
public class EstimatorParams {
    @JsonProperty("n_estimators")
    private Integer nEstimators = 10;

    @JsonProperty("criterion")
    private String criterion = "gini";

    @JsonProperty("max_depth")
    private Integer maxDepth = null;

    @JsonProperty("min_samples_split")
    private String minSamplesSplit = "2";

    @JsonProperty("min_samples_leaf")
    private String minSamplesLeaf = "1";

    @JsonProperty("min_weight_fraction_leaf")
    private Float minWeightFractionLeaf = 0.0F;

    @JsonProperty("max_features")
    private String maxFeatures = "auto";

    @JsonProperty("max_leaf_nodes")
    private Integer maxLeafNodes = null;

    @JsonProperty("min_impurity_decrease")
    private Float minImpurityDecrease = 0.0F;

    @JsonProperty("min_impurity_split")
    private Float minImpuritySplit = null;

    @JsonProperty("bootstrap")
    private Boolean bootstrap = true;

    @JsonProperty("oob_score")
    private Boolean oobScore = false;

    @JsonProperty("n_jobs")
    private Integer nJobs = 1;

    @JsonProperty("random_state")
    private Integer randomState = null;

    @JsonProperty("verbose")
    private Integer verbose = 0;

    @JsonProperty("warm_start")
    private Boolean warmStart = false;

    @JsonProperty("class_weight")
    private List<HashMap<Integer, Integer>> classWeight = null;

    @JsonProperty("n_estimators")
    public Integer getnEstimators() {
        return nEstimators;
    }

    @JsonProperty("n_estimators")
    public void setnEstimators(Integer nEstimators) {
        this.nEstimators = nEstimators;
    }

    @JsonProperty("criterion")
    public String getCriterion() {
        return criterion;
    }

    @JsonProperty("criterion")
    public void setCriterion(String criterion) {
        this.criterion = criterion;
    }

    @JsonProperty("max_depth")
    public Integer getMaxDepth() {
        return maxDepth;
    }

    @JsonProperty("max_depth")
    public void setMaxDepth(Integer maxDepth) {
        this.maxDepth = maxDepth;
    }

    @JsonProperty("min_samples_split")
    public String getMinSamplesSplit() {
        return minSamplesSplit;
    }

    @JsonProperty("min_samples_split")
    public void setMinSamplesSplit(String minSamplesSplit) {
        this.minSamplesSplit = minSamplesSplit;
    }

    @JsonProperty("min_samples_leaf")
    public String getMinSamplesLeaf() {
        return minSamplesLeaf;
    }

    @JsonProperty("min_samples_leaf")
    public void setMinSamplesLeaf(String minSamplesLeaf) {
        this.minSamplesLeaf = minSamplesLeaf;
    }

    @JsonProperty("min_weight_fraction_leaf")
    public Float getMinWeightFractionLeaf() {
        return minWeightFractionLeaf;
    }

    @JsonProperty("min_weight_fraction_leaf")
    public void setMinWeightFractionLeaf(Float minWeightFractionLeaf) {
        this.minWeightFractionLeaf = minWeightFractionLeaf;
    }

    @JsonProperty("max_features")
    public String getMaxFeatures() {
        return maxFeatures;
    }

    @JsonProperty("max_features")
    public void setMaxFeatures(String maxFeatures) {
        this.maxFeatures = maxFeatures;
    }

    @JsonProperty("max_leaf_nodes")
    public Integer getMaxLeafNodes() {
        return maxLeafNodes;
    }

    @JsonProperty("max_leaf_nodes")
    public void setMaxLeafNodes(Integer maxLeafNodes) {
        this.maxLeafNodes = maxLeafNodes;
    }

    @JsonProperty("min_impurity_decrease")
    public Float getMinImpurityDecrease() {
        return minImpurityDecrease;
    }

    @JsonProperty("min_impurity_decrease")
    public void setMinImpurityDecrease(Float minImpurityDecrease) {
        this.minImpurityDecrease = minImpurityDecrease;
    }

    @JsonProperty("min_impurity_split")
    public Float getMinImpuritySplit() {
        return minImpuritySplit;
    }

    @JsonProperty("min_impurity_split")
    public void setMinImpuritySplit(Float minImpuritySplit) {
        this.minImpuritySplit = minImpuritySplit;
    }

    @JsonProperty("bootstrap")
    public Boolean getBootstrap() {
        return bootstrap;
    }

    @JsonProperty("bootstrap")
    public void setBootstrap(Boolean bootstrap) {
        this.bootstrap = bootstrap;
    }

    @JsonProperty("oob_score")
    public Boolean getOobScore() {
        return oobScore;
    }

    @JsonProperty("oob_score")
    public void setOobScore(Boolean oobScore) {
        this.oobScore = oobScore;
    }

    @JsonProperty("n_jobs")
    public Integer getnJobs() {
        return nJobs;
    }

    @JsonProperty("n_jobs")
    public void setnJobs(Integer nJobs) {
        this.nJobs = nJobs;
    }

    @JsonProperty("random_state")
    public Integer getRandomState() {
        return randomState;
    }

    @JsonProperty("random_state")
    public void setRandomState(Integer randomState) {
        this.randomState = randomState;
    }

    @JsonProperty("verbose")
    public Integer getVerbose() {
        return verbose;
    }

    @JsonProperty("verbose")
    public void setVerbose(Integer verbose) {
        this.verbose = verbose;
    }

    @JsonProperty("warm_start")
    public Boolean getWarmStart() {
        return warmStart;
    }

    @JsonProperty("warm_start")
    public void setWarmStart(Boolean warmStart) {
        this.warmStart = warmStart;
    }

    @JsonProperty("class_weight")
    public List<HashMap<Integer, Integer>> getClassWeight() {
        return classWeight;
    }

    @JsonProperty("class_weight")
    public void setClassWeight(List<HashMap<Integer, Integer>> classWeight) {
        this.classWeight = classWeight;
    }
}
