import { computed, signal } from "@preact/signals-react";
import { Attribute } from "../types/Attribute";

const attributesSignal = signal<Attribute[]>([]);

const attributePreferedSignal = computed(() =>
  attributesSignal.value
    .filter((attribute) => attribute.prefer)
    .map((attribute) => attribute.name),
);

const attributeContrainedSignal = computed(() =>
  attributesSignal.value
    .filter((attribute) => attribute.ignore)
    .map((attribute) => attribute.name),
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
  const newAttrs = attributesSignal.peek().map((attribute) => {
    if (attribute.name === target.name) {
      attribute.ignore = !attribute.ignore;
      if (attribute.ignore) attribute.prefer = false;
    }
    return attribute;
  });
  if (newAttrs.filter((a) => !a.ignore).length < 3)
    alert("You must have at least 3 attributes");
  else attributesSignal.value = newAttrs;
};

export {
  attributesSignal,
  attributePreferedSignal,
  attributeContrainedSignal,
  toggleAttributePrefer,
  toggleAttributeIgnore,
};
