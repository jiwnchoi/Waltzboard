import { computed, signal } from '@preact/signals-react';
import axios from 'axios';
import { URI } from '../../config';
import { InferBody, InferResponse } from '../types/API';
import { configSignal } from './config';
import { pinnedKeysSignal } from './dashboard';

const inferResponseSignal = signal<InferResponse>({
    charts: [],
    result: {
        score: 0,
        diversity: 0,
        coverage: 0,
        specificity: 0,
        interestingness: 0,
        conciseness: 0,
    },
    dist: {
        score: [],
        specificity: [],
        interestingness: [],
        coverage: [],
        diversity: [],
        conciseness: [],
    },
});


const inferBodySignal = computed<InferBody>(() => {
    return {
        nCharts: configSignal.value.nChart,
        chartKeys: pinnedKeysSignal.value,
    }
});

const isInferingSignal = signal<boolean>(false);


const inferDashboard = async () => {
    const response = await axios.post(`${URI}/infer`, inferBodySignal.peek());
    inferResponseSignal.value = response.data as InferResponse;
    isInferingSignal.value = false;
};


export {
    inferResponseSignal,
    isInferingSignal,
    inferBodySignal,
    inferDashboard,
};
