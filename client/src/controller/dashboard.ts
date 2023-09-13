import { computed, signal } from '@preact/signals-react';
import type { ChartView } from '../types/ChartView';
import { toChartView } from '../utils/toChartView';
import { inferResponseSignal } from './infer';
import { fromChartView } from '../utils/fromChartView';
import { getRecommendedChartView } from './append';

const dashboardSignal = computed<ChartView[]>(() =>
  inferResponseSignal.value.charts.map((chart) => toChartView(chart))
);

const chartKeysSignal = computed<string[]>(() =>
  dashboardSignal.value.map((chart) => chart.key)
);

const isProcessingSignal = signal<boolean>(false);

const pinnedKeysSignal = signal<string[]>([]);

export const appendChart = (chart: ChartView) => {
  const current = inferResponseSignal.peek();
  const chartKeys = chartKeysSignal.peek();
  if (chartKeys.includes(chart.key)) return;

  inferResponseSignal.value = {
    ...current,
    charts: [...current.charts, fromChartView(chart)],
  };
  getRecommendedChartView();
};

export const removeChart = (chart: ChartView) => {
  const current = inferResponseSignal.peek();
  inferResponseSignal.value = {
    ...current,
    charts: current.charts.filter((c) => c.key !== chart.key),
  };
  getRecommendedChartView();
};

const togglePinChart = (key: string) => {
  if (pinnedKeysSignal.value.includes(key)) {
    pinnedKeysSignal.value = pinnedKeysSignal.value.filter((i) => i !== key);
  } else {
    pinnedKeysSignal.value = [...pinnedKeysSignal.value, key];
  }
};

export {
  chartKeysSignal,
  dashboardSignal,
  isProcessingSignal,
  pinnedKeysSignal,
  togglePinChart,
};
