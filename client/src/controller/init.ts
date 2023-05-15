import { batch, effect, signal } from '@preact/signals-react'
import axios from "axios"
import { URI } from '../../config'
import { Init } from '../types/API'
import { ChartType } from '../types/ChartType'
import { attributesSignal } from './attribute'
import { chartTypesSignal } from './chartType'
import { resultSignal, sampleBodySignal } from './dashboard'
import { selectedTaskTypeSignal, taskTypesSignal } from './taskType'

const initializedSignal = signal<boolean>(false);


(effect(async () => {
    const response = await axios.post(`${URI}/init`, sampleBodySignal.peek());
    const data: Init = response.data;
    batch(() => {
        initializedSignal.value = true;
        attributesSignal.value = data.attributes.map((attribute) => {
            return {
                ...attribute,
                prefer: false,
                ignore: false,
            };
        });
        chartTypesSignal.value = data.chartTypes.map((chartType) => {
            return {
                ...chartType,
                prefer: false,
                ignore: false,
            };
        });
        taskTypesSignal.value = data.taskTypes.map((taskType) => {
            return {
                ...taskType,
                chartTypes: taskType.chartTypes.map((chartType) => chartTypesSignal.peek().find((ct) => ct.name === chartType.name) as ChartType),
            };
        });
        resultSignal.value = data.result;
        selectedTaskTypeSignal.value = { ...selectedTaskTypeSignal.peek(), chartTypes: chartTypesSignal.peek() }
    });
}))();


export { initializedSignal }
