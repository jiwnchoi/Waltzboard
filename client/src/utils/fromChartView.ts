import { GleanerChartModel } from '../types/API';
import { ChartView } from '../types/ChartView';

export const fromChartView = (chartView: ChartView): GleanerChartModel => {
  return {
    key: chartView.key,
    spec: JSON.stringify(chartView.spec),
    statistics: chartView.statistics,
    title: chartView.title,
  };
};
