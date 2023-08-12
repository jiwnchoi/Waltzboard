interface AggregationFetched {
    name: string;
    type: string;
}

interface Aggregation extends AggregationFetched {
    ignore: boolean;
    prefer: boolean;
}

export type { Aggregation, AggregationFetched }