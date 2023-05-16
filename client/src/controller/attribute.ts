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

const attributeContrainedSignal = computed(() =>
    attributesSignal
        .value
        .filter((attribute) => attribute.ignore)
        .map((attribute) => attribute.name)
);



const toggleAttributePrefer = (target: Attribute) => {
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

const toggleAttributeIgnore = (target: Attribute) => {
    attributesSignal.value = attributesSignal.peek().map((attribute) => {
        if (attribute.name === target.name) {
            attribute.ignore = !attribute.ignore;
            if (attribute.ignore) attribute.prefer = false;
        }
        return attribute;
    });
};



export { attributesSignal, attributePreferedSignal, attributeContrainedSignal, toggleAttributePrefer, toggleAttributeIgnore };


