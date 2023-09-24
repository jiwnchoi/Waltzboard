import { computed, signal, effect, batch } from '@preact/signals-react';
import axios from 'axios';
import { URI } from '../../config';
import { InspectResponse, VariantsResponse } from '../types/API';
import { ChartView } from '../types/ChartView';
import { toChartView } from '../utils/toChartView';
import { chartKeysSignal, dashboardSignal } from './dashboard';
import { NUM_COL } from '../components/Main';
import { inferResponseSignal } from './infer';
import { fromChartView } from '../utils/fromChartView';
import { OracleSingleResult } from '../types/OracleResult';
import { isAppendPanelOpen } from './append';

export const variantChartsSignal = signal<ChartView[]>([]);

export const isVariantsLoadingSignal = signal<boolean>(false);
export const isInspectionLoadingSignal = signal<boolean>(false);

export const inspectionIndexSignal = signal<number>(-1);

export const inspectionSignal = signal<OracleSingleResult | undefined>(
  undefined
);

export const inspectionChartSignal = computed(() => {
  const target = inspectionIndexSignal.value;
  if (target === -1) return undefined;
  return dashboardSignal.value[target];
});

export const isDetailExpanded = (idx: number) => {
  // if (isAppendPanelOpen.value) return false;
  const value = inspectionIndexSignal.value;
  return idx - NUM_COL < value && value <= idx;
};

export const getVariants = async () => {
  if (
    chartKeysSignal.value.length === 0 ||
    inspectionIndexSignal.value === -1
  ) {
    variantChartsSignal.value = [];
    return;
  }
  isVariantsLoadingSignal.value = true;
  const response: VariantsResponse = (
    await axios.post(`${URI}/variants`, {
      chartKeys: chartKeysSignal.value,
      targetIndex: inspectionIndexSignal.value,
    })
  ).data;

  variantChartsSignal.value = response.variants.map((chart) =>
    toChartView(chart)
  );
  isVariantsLoadingSignal.value = false;
};

export const replaceChart = (idx: number, chart: ChartView) => {
  inferResponseSignal.value = {
    ...inferResponseSignal.value,
    charts: inferResponseSignal.value.charts.map((c, i) =>
      i === idx ? fromChartView(chart) : c
    ),
  };
};

export const getInspectation = async () => {
  isInspectionLoadingSignal.value = true;
  const target = inspectionIndexSignal.value;
  if (target === -1) {
    inspectionSignal.value = undefined;
    return;
  }
  const chartKeys = chartKeysSignal.value;
  const res: InspectResponse = (
    await axios.post(`${URI}/inspect`, {
      chartKeys,
      target,
    })
  ).data;
  inspectionSignal.value = res.result;
  isInspectionLoadingSignal.value = false;
};

effect(() => {
  batch(() => {
    getVariants();
    getInspectation();
  });
});
