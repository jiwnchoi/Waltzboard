interface AttributeDist {
    name: string;
    x: number;
    y: number;
    z: number;
}

interface ChartTypeDist { 
    name: string;
    prob: number;
}

interface AggregationDist {
    name: string;
    prob: number;
}

export type { AttributeDist, ChartTypeDist, AggregationDist }