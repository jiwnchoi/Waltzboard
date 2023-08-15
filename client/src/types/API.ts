import { AggregationFetched } from './Aggregation';
import type { AttributeFetched } from './Attribute';
import type { ChartTypeFetched } from './ChartType';
import { StatisticFeature } from './ChartView';
import type { OracleResult } from './OracleResult';
import { OracleWeight } from './OracleWeight';
import { AggregationDist, AttributeDist, ChartTypeDist } from './Space';
import { TaskTypeFetched } from './TaskType';

interface AttributeModel {
    name: string;
    type: string;
}

interface ScoreDistModel {
    score: number[];
    specificity: number[];
    interestingness: number[];
    coverage: number[];
    diversity: number[];
    parsimony: number[];
}

interface GleanerChartModel {
    key: string;
    title: string[];
    spec: string;
    statistics: StatisticFeature;
}


interface InferBody {
    nCharts: number | null;
    chartKeys: string[]
}

interface TrainBody {
    weight: OracleWeight;
    preferences: string[];
    constraints: string[];
}

interface RecommendBody {
    chartKeys: string[]
    nResults: number;
}

interface SetConfigBody {
    nCandidates: number;
    nFilters: number;
    robustness: number;
    halvingRatio: number;
}

interface InitResponse {
    chartTypes: ChartTypeFetched[];
    taskTypes: TaskTypeFetched[];
    attributes: AttributeFetched[];
    aggregations: AggregationFetched[];
}

interface InferResponse {
    charts: GleanerChartModel[];
    result: OracleResult;
    dist: ScoreDistModel;
}

interface RecommendResponse {
    charts: GleanerChartModel[];
}

interface TrainResponse {
    attribute: AttributeDist[];
    chartType: ChartTypeDist[];
    aggregation: AggregationDist[];
}

interface ScoreBody {
    chartKeys: string[];
}

interface ScoreResponse {
    result: OracleResult;
}

export type {
    InitResponse,
    InferResponse,
    RecommendResponse,
    TrainResponse,
    InferBody,
    TrainBody,
    RecommendBody,
    SetConfigBody,
    GleanerChartModel,
    AttributeModel,
    ScoreBody,
    ScoreResponse,
};
