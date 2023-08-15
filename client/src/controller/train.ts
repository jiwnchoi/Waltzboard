import { computed, signal } from '@preact/signals-react';
import axios from 'axios';
import { URI } from '../../config';
import type { TrainBody, TrainResponse } from '../types/API';
import { aggregationConstrainedSignal, aggregationPreferredSignal } from './aggregation';
import { attributeContrainedSignal, attributePreferedSignal } from './attribute';
import { chartTypeConstrainedSignal, chartTypePreferredSignal } from './chartType';
import { weightSignal } from './oracleWeight';

const trainBodySignal = computed<TrainBody>(() => {
    return {
        weight: weightSignal.value,
        preferences: [
            ...attributePreferedSignal.value,
            ...chartTypePreferredSignal.value,
            ...aggregationPreferredSignal.value,
        ],
        constraints: [
            ...attributeContrainedSignal.value,
            ...chartTypeConstrainedSignal.value,
            ...aggregationConstrainedSignal.value,
        ],
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
};

const isTrainingSignal = signal<boolean>(false);
const isTrainedSignal = signal<boolean>(false);

export {
    aggregationDistSignal,
    attributeDistSignal,
    chartTypeDistSignal,
    isTrainedSignal,
    isTrainingSignal,
    trainGleaner
};

