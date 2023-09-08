import type { TopLevelSpec } from "vega-lite";
import { GleanerChartModel } from "../types/API";
import { OracleResult } from "./OracleResult";

interface StatisticFeature {
    [key: string]: (string | null)[]
}

interface TitleToken {
    text: string;
    isPrefered: boolean;
}

interface ChartView extends GleanerChartModel {
    key: string;
    spec: TopLevelSpec | any;
    statistics: StatisticFeature;

    isPinned: boolean;
    titleToken: TitleToken[];
    chartResults: OracleResult | undefined;
}


export type { ChartView, StatisticFeature, TitleToken };
