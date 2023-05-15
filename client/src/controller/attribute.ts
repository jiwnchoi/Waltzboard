import { computed, signal } from "@preact/signals-react";
import { Attribute } from "../types/Attribute";
import { unSelectTaskType } from "./taskType";


const attributesSignal = signal<Attribute[]>([]);


const attributePreferedSignal = computed(() =>
    attributesSignal
        .value
        .filter((attribute) => attribute.prefer)
        .map((attribute) => attribute.name)
);


const attributeWildcardsSignal = computed(() =>
    attributePreferedSignal
        .value
        .map((attribute) => `attr_${attribute}`)
);


const toggleAttributePrefer = (target: Attribute) => {
    unSelectTaskType();
    attributesSignal.value = attributesSignal.peek().map((attribute) => {
        if (attribute.name === target.name) {
            return {
                ...attribute,
                prefer: !attribute.prefer,
            };
        }
        return attribute;
    });
};


export { attributesSignal, attributePreferedSignal, attributeWildcardsSignal, toggleAttributePrefer };


