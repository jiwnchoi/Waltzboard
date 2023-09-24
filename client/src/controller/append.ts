import { effect, signal } from '@preact/signals-react';
import axios from 'axios';
import { URI } from '../../config';
import { GetChartResponse } from '../types/API';
import { ChartView } from '../types/ChartView';
import { toChartView } from '../utils/toChartView';
import { chartKeysSignal } from './dashboard';
import { inspectionIndexSignal } from './details';



export const inputTuple = signal<(string | null)[]>([
  null,
  null,
  null,
  null,
  null,
  null,
  null,
]);

export const inputChart = signal<ChartView | null>(null);

export const isTupleValid = signal<boolean>(false);

export const isRecommendingSignal = signal<boolean>(false);

export const resetTuple = () => {
  inputTuple.value = [null, null, null, null, null, null, null];
};

export const recommendedChartViewSignal = signal<ChartView[]>([]);

effect(() => {
  const getIsValid = async () => {
    const res = await axios.get(
      `${URI}/is_valid?token=${JSON.stringify(inputTuple.value)}`
    );
    isTupleValid.value = res.data.isValid;
  };
  getIsValid();
});

effect(() => {
  const getChartFromToken = async () => {
    if (!isTupleValid.value) return null;
    const res: GetChartResponse = (
      await axios.get(
        `${URI}/get_chart?token=${JSON.stringify(inputTuple.value)}`
      )
    ).data;
    inputChart.value = toChartView(res.chart);
  };
  if (!isTupleValid.value) inputChart.value = null;
  getChartFromToken();
});

export const getRecommendedChartView = async () => {
  isRecommendingSignal.value = true;
  const res = await axios.post(`${URI}/recommends`, {
    chartKeys: chartKeysSignal.peek(),
  });
  recommendedChartViewSignal.value = res.data.recommends.map((chart: any) =>
    toChartView(chart)
  );
  isRecommendingSignal.value = false;
};


export const isAppendPanelOpen = signal(false);
export const toggleAppendPanel = () => {
  if (!isAppendPanelOpen.value) getRecommendedChartView();
  inspectionIndexSignal.value = -1;
  isAppendPanelOpen.value = !isAppendPanelOpen.value;
  inputTuple.value = [null, null, null, null, null, null, null];
  inputChart.value = null;
  recommendedChartViewSignal.value = [];
};