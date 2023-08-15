import { computed, signal } from '@preact/signals-react';
import { unSelectTaskType } from './taskType';
import { Aggregation } from '../types/Aggregation';

const aggregationsSignal = signal<Aggregation[]>([]);

const targetAggregationSignal = computed(() =>
    aggregationsSignal.value.filter((aggregation) => !aggregation.ignore).map((aggregation) => aggregation.type)
);

const aggregationPreferredSignal = computed(() =>
    aggregationsSignal.value
        .filter((aggregation) => aggregation.prefer)
        .map((aggregation) => `${aggregation.type}`)
);

const aggregationConstrainedSignal = computed(() =>
    aggregationsSignal.value
        .filter((aggregation) => aggregation.ignore)
        .map((aggregation) => `${aggregation.type}`)
);


const toggleAggregationPrefer = (target: Aggregation) => {
    if (target.ignore) return;
    aggregationsSignal.value = aggregationsSignal.peek().map((aggregation) => {
        if (aggregation.name === target.name) {
            return {
                ...aggregation,
                prefer: !aggregation.prefer,
                ignore: false,
            };
        }
        return aggregation;
    });
};

const toggleAggregationIgnore = (target: Aggregation) => {
    unSelectTaskType();
    aggregationsSignal.value = aggregationsSignal.peek().map((aggregation) => {
        if (aggregation.name === target.name) {
            aggregation.ignore = !aggregation.ignore;
            if (aggregation.ignore) aggregation.prefer = false;
        }
        return aggregation;
    });
};

export {
    aggregationsSignal,
    aggregationConstrainedSignal,
    targetAggregationSignal,
    aggregationPreferredSignal,
    toggleAggregationPrefer,
    toggleAggregationIgnore,
};
