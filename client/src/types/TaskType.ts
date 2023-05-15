import { ChartType, ChartTypeFetched } from "./ChartType";
import { OracleWeight } from "./OracleWeight";


interface TaskTypeFetched {
    name: string;
    weight: OracleWeight;
    chartTypes: ChartTypeFetched[];
}

interface TaskType extends TaskTypeFetched {
    chartTypes: ChartType[];
}


export type { TaskType, TaskTypeFetched }