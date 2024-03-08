import { computed, signal } from "@preact/signals-react";
import { Transformation } from "../types/Transformation";

const transformationsSignal = signal<Transformation[]>([]);

const notDayTransformationsSignal = computed(() =>
  transformationsSignal.value.filter(
    (transformation) =>
      !["year", "day", "month", "bin"].includes(transformation.type),
  ),
);

const dayTransformationsSignal = computed(() =>
  transformationsSignal.value.filter((transformation) =>
    ["year", "day", "month"].includes(transformation.type),
  ),
);

const targetTransformationSignal = computed(() =>
  transformationsSignal.value
    .filter((transformation) => !transformation.ignore)
    .map((transformation) => transformation.type),
);

const transformationPreferredSignal = computed(() =>
  transformationsSignal.value
    .filter((transformation) => transformation.prefer)
    .map((transformation) => `${transformation.type}`),
);

const transformationConstrainedSignal = computed(() =>
  transformationsSignal.value
    .filter((transformation) => transformation.ignore)
    .map((transformation) => `${transformation.type}`),
);

const toggleTransformationPrefer = (target: Transformation) => {
  if (target.ignore) return;
  transformationsSignal.value = transformationsSignal
    .peek()
    .map((transformation) => {
      if (transformation.name === target.name) {
        return {
          ...transformation,
          prefer: !transformation.prefer,
          ignore: false,
        };
      }
      return transformation;
    });
};

const toggleTransformationIgnore = (target: Transformation) => {
  const newTRS = transformationsSignal.peek().map((transformation) => {
    if (transformation.name === target.name) {
      transformation.ignore = !transformation.ignore;
      if (transformation.ignore) transformation.prefer = false;
    }
    return transformation;
  });
  if (newTRS.filter((c) => !c.ignore).length < 5)
    alert("You must have at least 5 transformations");
  else transformationsSignal.value = newTRS;
};

export {
  transformationsSignal,
  transformationConstrainedSignal,
  targetTransformationSignal,
  transformationPreferredSignal,
  toggleTransformationPrefer,
  toggleTransformationIgnore,
  notDayTransformationsSignal,
  dayTransformationsSignal,
};
