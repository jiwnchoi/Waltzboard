import { computed, signal } from '@preact/signals-react';
import type { ChartView } from '../types/ChartView';
import { toChartView } from '../utils/toChartView';
import { inferResponseSignal } from './infer';

const dashboardSignal = computed<ChartView[]>(() =>
  inferResponseSignal.value.charts.map((chart => toChartView(chart))
))

const chartKeysSignal = computed<string[]>(() =>
  dashboardSignal.value.map((chart) => chart.key)
);

const isProcessingSignal = signal<boolean>(false);

const pinnedKeysSignal = signal<string[]>([]);

const removeChart = (key: string) => {
  inferResponseSignal.value = {
    ...inferResponseSignal.peek(),
    charts: inferResponseSignal
      .peek()
      .charts.filter((chart) => chart.key !== key),
  };
};

const togglePinChart = (key: string) => {
  if (pinnedKeysSignal.value.includes(key)) {
    pinnedKeysSignal.value = pinnedKeysSignal.value.filter((i) => i !== key);
  } else {
    pinnedKeysSignal.value = [...pinnedKeysSignal.value, key];
  }
};

export {
    chartKeysSignal, dashboardSignal,
    isProcessingSignal,
    pinnedKeysSignal, removeChart,
    togglePinChart
};

