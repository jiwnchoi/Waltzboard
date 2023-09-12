import { computed, signal, effect } from '@preact/signals-react';
import axios from 'axios';
import { URI } from '../../config';
import { VariantsResponse } from '../types/API';
import { ChartView } from '../types/ChartView';
import { toChartView } from '../utils/toChartView';
import { chartKeysSignal } from './dashboard';

export const variantChartsSignal = signal<ChartView[]>([]);

export const isVariantsLoadingSignal = signal<boolean>(false);

export const detailTargetSignal = signal<number | undefined>(undefined);

export const isDetailExpanded = (idx: number) => {
  const value = detailTargetSignal.value ?? -1;
  return idx - 4 < value && value <= idx;
};

export const getVariants = async () => {
  if (chartKeysSignal.value.length === 0 || detailTargetSignal.value === undefined) {
    return;
  }
  isVariantsLoadingSignal.value = true;
  const response: VariantsResponse = (
    await axios.post(`${URI}/variants`, {
      chartKeys: chartKeysSignal.value,
      targetIndex: detailTargetSignal.value,
    })
  ).data;

  variantChartsSignal.value = response.variants.map((chart) =>
    toChartView(chart)
  );
    isVariantsLoadingSignal.value = false;
};


effect(() => {
  getVariants();
});