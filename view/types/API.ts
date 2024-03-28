import type { AttributeFetched } from "./Attribute";
import type { ChartTypeFetched } from "./ChartType";
import { StatisticFeature } from "./ChartView";
import type { OracleResult, OracleSingleResult } from "./OracleResult";
import { OracleWeight } from "./OracleWeight";
import { AttributeDist, ChartTypeDist, TransformationDist } from "./Space";
import { TaskTypeFetched } from "./TaskType";
import { TransformationFetched } from "./Transformation";

export interface AttributeModel {
  name: string;
  type: string;
}

export interface ScoreDistModel {
  score: number[];
  specificity: number[];
  interestingness: number[];
  coverage: number[];
  diversity: number[];
  parsimony: number[];
}

export interface WaltzboardChartModel {
  key: string;
  title: string[];
  spec: string;
  statistics: StatisticFeature[];
}

export interface InferBody {
  chartKeys: string[];
}

export interface TrainBody {
  weight: OracleWeight;
  preferences: string[];
  constraints: string[];
}

export interface RecommendBody {
  chartKeys: string[];
  nResults: number;
}

export interface SetConfigBody {
  nCandidates: number;
  nFilters: number;
  robustness: number;
  halvingRatio: number;
}

export interface InitBody {
  n_epoch?: number;
  n_candidates?: number;
  n_search_space?: number;
  n_beam?: number;
  robustness?: number;
  dataset?: string;
}

export interface Configs {
  [key: string]: string | number | null;
}

export interface InitResponse {
  chartTypes: ChartTypeFetched[];
  taskTypes: TaskTypeFetched[];
  attributes: AttributeFetched[];
  transformations: TransformationFetched[];
  configs: Configs;
}

export interface InferResponse {
  charts: WaltzboardChartModel[];
  result: OracleResult;
  chartResults: OracleResult[];
}

export interface RecommendResponse {
  charts: WaltzboardChartModel[];
}

export interface TrainResponse {
  attribute: AttributeDist[];
  chartType: ChartTypeDist[];
  transformation: TransformationDist[];
  result: ScoreDistModel;
}

export interface ScoreBody {
  chartKeys: string[];
}

export interface ScoreResponse {
  result: OracleResult;
  chartResults: OracleResult[];
}

export interface VariantsBody {
  chartKeys: string[];
  targetIndex: number;
}

export interface VariantsResponse {
  variants: WaltzboardChartModel[];
}

export interface InspectBody {
  chartKeys: string[];
  target: number;
}

export interface InspectResponse {
  result: OracleSingleResult;
}

export interface RecommendBody {
  chartKeys: string[];
}

export interface RecommendResponse {
  recommends: WaltzboardChartModel[];
}

export interface GetChartResponse {
  chart: WaltzboardChartModel | null;
}
