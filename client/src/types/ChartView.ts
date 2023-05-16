import type { TopLevelSpec } from "vega-lite";
import { GleanerChartModel } from "../types/API";

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
    title: TitleToken[];
}

export type { ChartView, StatisticFeature, TitleToken };
