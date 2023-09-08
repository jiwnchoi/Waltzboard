import { TransformationFetched } from './Transformation';
import type { AttributeFetched } from './Attribute';
import type { ChartTypeFetched } from './ChartType';
import { StatisticFeature } from './ChartView';
import type { OracleResult } from './OracleResult';
import { OracleWeight } from './OracleWeight';
import { TransformationDist, AttributeDist, ChartTypeDist } from './Space';
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
    chartKeys: string[];
}

interface TrainBody {
    weight: OracleWeight;
    preferences: string[];
    constraints: string[];
}

interface RecommendBody {
    chartKeys: string[];
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
    transformations: TransformationFetched[];
}

interface InferResponse {
    charts: GleanerChartModel[];
    result: OracleResult;
    chartResults: OracleResult[];
}

interface RecommendResponse {
    charts: GleanerChartModel[];
}

interface TrainResponse {
    attribute: AttributeDist[];
    chartType: ChartTypeDist[];
    transformation: TransformationDist[];
    result: ScoreDistModel;
}

interface ScoreBody {
    chartKeys: string[];
}

interface ScoreResponse {
    result: OracleResult;
    chartResults: OracleResult[];
}

export type {
    AttributeModel,
    GleanerChartModel,
    InferBody,
    InferResponse,
    InitResponse,
    RecommendBody,
    RecommendResponse,
    ScoreBody,
    ScoreResponse,
    SetConfigBody,
    TrainBody,
    TrainResponse,
};
