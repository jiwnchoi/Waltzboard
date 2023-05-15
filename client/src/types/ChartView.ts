import { VisualizationSpec } from "react-vega";

interface StatisticFeature {
    [key: string]: (string | null)[]
}

interface TitleToken {
    text: string;
    isPrefered: boolean;
}

interface ChartView {
    index: number;
    spec: VisualizationSpec | any;
    isPinned: boolean;
    statistic_feature: StatisticFeature;
    title: TitleToken[];
}

export type { ChartView, StatisticFeature, TitleToken };
