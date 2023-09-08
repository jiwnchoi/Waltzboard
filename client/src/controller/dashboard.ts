import { computed, signal } from '@preact/signals-react';
import type { ChartView, TitleToken } from '../types/ChartView';
import { attributePreferedSignal } from './attribute';
import { inferResponseSignal } from './infer';
import { transformationPreferredSignal } from './transformation';


const dashboardSignal = computed<ChartView[]>(() =>
    inferResponseSignal.value.charts.map((chart, i) => {
        const specObject = JSON.parse(chart.spec);
        const title = chart.title
        const titleToken: TitleToken[] = title.map((t) => {
            return {
                text: t,
                isPrefered: attributePreferedSignal.peek().includes(t) || transformationPreferredSignal.peek().includes(t.toLowerCase()),
            };
        });
        specObject.autosize = { type: 'fit', contains: 'padding' };
        specObject.title = null;
        if (specObject.encoding && specObject.encoding.color) {
            specObject.encoding.color.legend = { title: null };
        }
        return {
            key: chart.key,
            spec: specObject,
            statistics: chart.statistics,
            isPinned: pinnedKeysSignal.value.includes(chart.key),
            title,
            titleToken,
        };
    })
);

const chartKeysSignal = computed<string[]>(() => dashboardSignal.value.map((chart) => chart.key));

const isProcessingSignal = signal<boolean>(false);

const pinnedKeysSignal = signal<string[]>([]);


const removeChart = (key: string) => {
    inferResponseSignal.value = {
        ...inferResponseSignal.peek(),
        charts: inferResponseSignal.peek().charts.filter((chart) => chart.key !== key)
    }

};

const togglePinChart = (key: string) => {
    if (pinnedKeysSignal.value.includes(key)) {
        pinnedKeysSignal.value = pinnedKeysSignal.value.filter((i) => i !== key);
    } else {
        pinnedKeysSignal.value = [...pinnedKeysSignal.value, key];
    }
};


export {
    dashboardSignal,
    isProcessingSignal,
    pinnedKeysSignal,
    chartKeysSignal,
    removeChart,
    togglePinChart,
};
