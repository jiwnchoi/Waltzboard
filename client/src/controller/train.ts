import { computed, signal } from '@preact/signals-react';
import axios from 'axios';
import { URI } from '../../config';
import type { TrainBody, TrainResponse } from '../types/API';
import {
  transformationConstrainedSignal,
  transformationPreferredSignal,
} from './transformation';
import {
  attributeContrainedSignal,
  attributePreferedSignal,
} from './attribute';
import {
  chartTypeConstrainedSignal,
  chartTypePreferredSignal,
} from './chartType';
import { weightSignal } from './oracleWeight';

const trainBodySignal = computed<TrainBody>(() => {
  return {
    weight: weightSignal.value,
    preferences: [
      ...attributePreferedSignal.value,
      ...chartTypePreferredSignal.value,
      ...transformationPreferredSignal.value,
    ],
    constraints: [
      ...attributeContrainedSignal.value,
      ...chartTypeConstrainedSignal.value,
      ...transformationConstrainedSignal.value,
    ],
  };
});

const trainResponseSignal = signal<TrainResponse>({
  attribute: [],
  chartType: [],
  transformation: [],
  result: {
    score: [],
    specificity: [],
    interestingness: [],
    coverage: [],
    diversity: [],
    parsimony: [],
  },
});

const attributeDistSignal = computed(() => trainResponseSignal.value.attribute);

const chartTypeDistSignal = computed(() => trainResponseSignal.value.chartType);

const transformationDistSignal = computed(
  () => trainResponseSignal.value.transformation
);

const scoreDistSignal = computed(() => trainResponseSignal.value.result);

const trainGleaner = async () => {
  isTrainingSignal.value = true;
  const response: TrainResponse = (
    await axios.post(`${URI}/train`, trainBodySignal.peek())
  ).data;
  response.transformation = response.transformation.filter(
    (transformation) =>
      !['year', 'day', 'month', 'bin'].includes(transformation.name)
  );
  response.transformation.sort((a, b) => {
    if (a.name === 'None') return 1;
    if (b.name === 'None') return -1;
    return 0;
  });
  response.attribute.sort((a, b) => {
    if (a.name === 'None') return 1;
    if (b.name === 'None') return -1;
    return 0;
  });

  trainResponseSignal.value = response;
  isTrainingSignal.value = false;
  isTrainedSignal.value = true;
};

const isTrainingSignal = signal<boolean>(false);
const isTrainedSignal = signal<boolean>(false);

export {
  transformationDistSignal,
  attributeDistSignal,
  chartTypeDistSignal,
  scoreDistSignal,
  isTrainedSignal,
  isTrainingSignal,
  trainGleaner,
};
