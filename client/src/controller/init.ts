import { batch, effect, signal } from '@preact/signals-react';
import axios from 'axios';
import { URI } from '../../config';
import { Configs, InitResponse } from '../types/API';
import { attributesSignal } from './attribute';
import { chartTypesSignal } from './chartType';
import { inferDashboard } from './infer';
import { trainWaltzboard } from './train';
import { transformationsSignal } from './transformation';

const initializedSignal = signal<boolean>(false);

export const configSignal = signal<Configs>({
    dataset: 'Movies',
    n_beam: 10,
    n_candidates: 50,
    n_epoch: 20,
    n_search_space: 100,
    robustness: 50,
});

const init = async () => {
    const response: InitResponse = (
        await axios.post(`${URI}/init`, configSignal.peek())
    ).data;
    configSignal.value = { ...response.configs };

    batch(() => {
        attributesSignal.value = response.attributes.map((attribute) => {
            return {
                ...attribute,
                prefer: false,
                ignore: false,
            };
        });
        chartTypesSignal.value = response.chartTypes.map((chartType) => {
            return {
                ...chartType,
                prefer: false,
                ignore: ['tick', 'arc'].includes(chartType.mark),
            };
        });
        transformationsSignal.value = response.transformations.map(
            (transformation) => {
                return {
                    ...transformation,
                    prefer: false,
                    ignore: ['sum', 'min', 'max'].includes(transformation.type),
                };
            }
        );
        // taskTypesSignal.value = response.taskTypes.map((taskType) => {
        //     return {
        //         ...taskType,
        //         chartTypes: taskType.chartTypes.map((chartType) => chartTypesSignal.peek().find((ct) => ct.name === chartType.name) as ChartType),
        //     };
        // });
        // selectedTaskTypeSignal.value = { ...selectedTaskTypeSignal.peek(), chartTypes: chartTypesSignal.peek() }
        initializedSignal.value = true;
    });
    initializedSignal.value = true;
};

effect(() => {
    init();
})();

export { init, initializedSignal };

