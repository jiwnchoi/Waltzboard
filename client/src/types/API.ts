import { TransformationFetched } from './Transformation';
import type { AttributeFetched } from './Attribute';
import type { ChartTypeFetched } from './ChartType';
import { ChartView, StatisticFeature } from './ChartView';
import type { OracleResult, OracleSingleResult } from './OracleResult';
import { OracleWeight } from './OracleWeight';
import { TransformationDist, AttributeDist, ChartTypeDist } from './Space';
import { TaskTypeFetched } from './TaskType';

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

export interface GleanerChartModel {
  key: string;
  title: string[];
  spec: string;
  statistics: StatisticFeature[];
}

export interface InferBody {
  nCharts: number | null;
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

export interface InitResponse {
  chartTypes: ChartTypeFetched[];
  taskTypes: TaskTypeFetched[];
  attributes: AttributeFetched[];
  transformations: TransformationFetched[];
}

export interface InferResponse {
  charts: GleanerChartModel[];
  result: OracleResult;
  chartResults: OracleResult[];
}

export interface RecommendResponse {
  charts: GleanerChartModel[];
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
  variants: GleanerChartModel[];
}

export interface InspectBody {
  chartKeys: string[];
  target: number;
}

export interface InspectResponse {
  result: OracleSingleResult;
}
