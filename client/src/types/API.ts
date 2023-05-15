import type { AttributeFetched } from './Attribute';
import type { ChartTypeFetched } from './ChartType';
import { StatisticFeature } from './ChartView';
import type { OracleResult } from "./OracleResult";
import { OracleWeight } from './OracleWeight';
import { TaskTypeFetched } from './TaskType';


interface Result {
    indices: number[];
    vlspecs: string[];
    statistic_features: StatisticFeature[];
    result: OracleResult;
    sampled_results: OracleResult[];
}



interface Init {
    chartTypes: ChartTypeFetched[];
    taskTypes: TaskTypeFetched[];
    attributes: AttributeFetched[];
    result: Result;
}

interface SampleBody {
    indices: number[]
    numVis: number
    numSample: number
    numFilter: number
    weight: OracleWeight
    chartTypes: string[]
    wildcard: string[]
}

export type { Result, Init, SampleBody };
