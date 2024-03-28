import type { TopLevelSpec } from "vega-lite";
import { WaltzboardChartModel } from "./API";
import { OracleResult } from "./OracleResult";

interface StatisticFeature {
  key: string[];
  features: (string | null)[];
}

interface TitleToken {
  text: string;
  isPrefered: boolean;
}

interface ChartView extends WaltzboardChartModel {
  key: string;
  spec: TopLevelSpec | any;
  statistics: StatisticFeature[];

  isPinned: boolean;
  titleToken: TitleToken[];
  chartResults: OracleResult | undefined;
}

export type { ChartView, StatisticFeature, TitleToken };
