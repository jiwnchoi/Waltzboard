interface ChartTypeFetched {
    name: string;
    mark: string;
}

interface ChartType extends ChartTypeFetched {
    prefer: boolean;
    ignore: boolean;
}


export type { ChartTypeFetched, ChartType };
