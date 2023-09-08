import { batch, computed, effect } from '@preact/signals-react';
import axios from 'axios';
import { URI } from '../../config';
import { ScoreBody, ScoreResponse } from '../types/API';
import { dashboardSignal, isProcessingSignal } from './dashboard';
import { inferResponseSignal } from './infer';

const scoreBodySignal = computed<ScoreBody>(() => {
    return { chartKeys: dashboardSignal.value.map((chart) => chart.key) };
});

const scoreDashboard = async () => {
    const response: ScoreResponse = (await axios.post(`${URI}/score`, scoreBodySignal.peek())).data;
    batch(() => {
        inferResponseSignal.value.result = response.result;
        response.chartResults.forEach((chartResult, i) => {
            dashboardSignal.value[i].chartResults = chartResult;
        }
        );
    });
    isProcessingSignal.value = false;
};

effect(() => {
    if (dashboardSignal.value.length > 1) {
        isProcessingSignal.value = true;
        scoreDashboard();
        isProcessingSignal.value = false;
    }
});

export { scoreDashboard };
