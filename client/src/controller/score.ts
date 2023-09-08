import axios from 'axios';
import { URI } from '../../config';
import type { ChartView, TitleToken } from '../types/ChartView';
import { computed, effect } from '@preact/signals-react';
import { ScoreBody, ScoreResponse } from '../types/API';
import { dashboardSignal, isProcessingSignal } from './dashboard';
import { inferResponseSignal } from './infer';

const scoreBodySignal = computed<ScoreBody>(() => {
    return { chartKeys: dashboardSignal.value.map((chart) => chart.key) };
});

const scoreDashboard = async () => {
    const response: ScoreResponse = (await axios.post(`${URI}/score`, scoreBodySignal.peek())).data;
    inferResponseSignal.value.result = response.result;
    isProcessingSignal.value = false;
};

effect(() => {
    if (dashboardSignal.value.length > 1) {
        isProcessingSignal.value = true;
        scoreDashboard();
        isProcessingSignal.value = false;
    }
});

export { scoreDashboard }