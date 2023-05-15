import { batch, effect, signal } from '@preact/signals-react';
import { TaskType } from '../types/TaskType';
import { chartTypesSignal } from './chartType';
import { weightSignal } from './oracleWeight';

const defaultTaskType: TaskType = {
    name: 'User Task',
    weight: {
        specificity: 1,
        interestingness: 1,
        coverage: 1,
        uniqueness: 1,
    },
    chartTypes: [],
};

const taskTypesSignal = signal<TaskType[]>([defaultTaskType]);

const selectedTaskTypeSignal = signal<TaskType>(defaultTaskType);

const unSelectTaskType = () => {
    selectedTaskTypeSignal.value = {
        name: defaultTaskType.name,
        weight: weightSignal.peek(),
        chartTypes: chartTypesSignal.peek(),
    };
};

// Effect when selectedTaskTypeSignal changes
effect(() => {
    batch(() => {
        weightSignal.value = selectedTaskTypeSignal.value.weight;

        if (selectedTaskTypeSignal.value.name === defaultTaskType.name) return;

        chartTypesSignal.value = chartTypesSignal.peek().map((chartType) => {
            if (
                selectedTaskTypeSignal.value.chartTypes.some(
                    (selectedChartType) => selectedChartType.name === chartType.name
                )
            ) {
                return {
                    ...chartType,
                    ignore: false,
                };
            }
            return {
                ...chartType,
                ignore: true,
            };
        });
    });
});

export { taskTypesSignal, selectedTaskTypeSignal, unSelectTaskType };
