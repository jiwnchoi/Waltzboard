import { computed, signal } from '@preact/signals-react';
import axios from 'axios';
import { URI } from '../../config';
import type { TrainBody, TrainResponse } from '../types/API';
import { attributeContrainedSignal, attributePreferedSignal } from './attribute';
import { chartTypeConstrainedSignal, chartTypePreferredSignal } from './chartType';
import { weightSignal } from './oracleWeight';

const trainBodySignal = computed<TrainBody>(() => {
    const weight = weightSignal.value;

    return {
        weight: weightSignal.value,
        preferences: [...attributePreferedSignal.value, ...chartTypePreferredSignal.value],
        constraints: [...attributeContrainedSignal.value, ...chartTypeConstrainedSignal.value],
    };
});

const trainResponseSignal = signal<TrainResponse>({
    attribute: [],
    chartType: [],
    aggregation: [],
});

const attributeDistSignal = computed(() => trainResponseSignal.value.attribute);

const chartTypeDistSignal = computed(() => trainResponseSignal.value.chartType);

const aggregationDistSignal = computed(() => trainResponseSignal.value.aggregation);

const trainGleaner = async () => {
    const response: TrainResponse = (await axios.post(`${URI}/train`, trainBodySignal.peek())).data;
    trainResponseSignal.value = response;
    isTrainingSignal.value = false;
    isTrainedSignal.value = true;

    console.log('train response', response);
    console.log(attributeDistSignal.peek());
    console.log(chartTypeDistSignal.peek());
    console.log(aggregationDistSignal.peek());
};

const isTrainingSignal = signal<boolean>(false);
const isTrainedSignal = signal<boolean>(false);

export {
    aggregationDistSignal,
    attributeDistSignal,
    chartTypeDistSignal,
    isTrainedSignal,
    isTrainingSignal,
    trainGleaner,
};
