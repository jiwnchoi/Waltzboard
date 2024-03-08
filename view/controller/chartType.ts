import { computed, signal } from "@preact/signals-react";
import { ChartType } from "../types/ChartType";

const chartTypesSignal = signal<ChartType[]>([]);

const targetChartTypeSignal = computed(() =>
  chartTypesSignal.value
    .filter((chartType) => !chartType.ignore)
    .map((chartType) => chartType.mark),
);

const chartTypePreferredSignal = computed(() =>
  chartTypesSignal.value
    .filter((chartType) => chartType.prefer)
    .map((chartType) => `${chartType.mark}`),
);

const chartTypeConstrainedSignal = computed(() =>
  chartTypesSignal.value
    .filter((chartType) => chartType.ignore)
    .map((chartType) => `${chartType.mark}`),
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
  const newCTs = chartTypesSignal.peek().map((chartType) => {
    if (chartType.name === target.name) {
      chartType.ignore = !chartType.ignore;
      if (chartType.ignore) chartType.prefer = false;
    }
    return chartType;
  });
  if (newCTs.filter((c) => !c.ignore).length < 3)
    alert("You must have at least 3 chart types");
  else chartTypesSignal.value = newCTs;
  return newCTs;
};

export {
  chartTypesSignal,
  chartTypeConstrainedSignal,
  targetChartTypeSignal,
  chartTypePreferredSignal,
  toggleChartTypePrefer,
  toggleChartTypeIgnore,
};
