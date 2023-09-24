import { batch, computed, signal } from '@preact/signals-react';
import axios from 'axios';
import { URI } from '../../config';
import { InferBody, InferResponse } from '../types/API';
import { pinnedKeysSignal } from './dashboard';
import { isTrainingSignal } from './train';

const inferResponseSignal = signal<InferResponse>({
  charts: [],
  result: {
    score: 0,
    diversity: 0,
    coverage: 0,
    specificity: 0,
    interestingness: 0,
    parsimony: 0,
  },
  chartResults: [],
});

const inferBodySignal = computed<InferBody>(() => {
  return {
    chartKeys: pinnedKeysSignal.value,
  };
});

const isInferingSignal = signal<boolean>(false);

export const isLoading = computed(() => {
  return isInferingSignal.value || isTrainingSignal.value;
})

const inferDashboard = async () => {
  const response = await axios.post(`${URI}/infer`, inferBodySignal.peek());
  batch(() => {
    inferResponseSignal.value = response.data as InferResponse;
    isInferingSignal.value = false;
  });
};

export {
  inferBodySignal,
  inferDashboard,
  inferResponseSignal,
  isInferingSignal,
};
