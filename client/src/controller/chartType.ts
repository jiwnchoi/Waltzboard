import { computed, signal } from '@preact/signals-react';
import { ChartType } from '../types/ChartType';
import { unSelectTaskType } from './taskType';

const chartTypesSignal = signal<ChartType[]>([]);

const targetChartTypeSignal = computed(() =>
    chartTypesSignal.value.filter((chartType) => !chartType.ignore).map((chartType) => chartType.mark)
);

const chartTypeWildcardSignal = computed(() =>
    chartTypesSignal.value
        .filter((chartType) => chartType.prefer)
        .map((chartType) => `${chartType.name}`)
);

const toggleChartTypePrefer = (target: ChartType) => {
    if (target.ignore) return;
    chartTypesSignal.value = chartTypesSignal.peek().map((chartType) => {
        if (chartType.name === target.name) {
            return {
                ...chartType,
                prefer: !chartType.prefer,
                ignore: false,
            };
        }
        return chartType;
    });
};

const toggleChartTypeIgnore = (target: ChartType) => {
    unSelectTaskType();
    chartTypesSignal.value = chartTypesSignal.peek().map((chartType) => {
        if (chartType.name === target.name) {
            chartType.ignore = !chartType.ignore;
            if (chartType.ignore) chartType.prefer = false;
        }
        return chartType;
    });
};

export {
    chartTypesSignal,
    targetChartTypeSignal,
    chartTypeWildcardSignal,
    toggleChartTypePrefer,
    toggleChartTypeIgnore,
};
