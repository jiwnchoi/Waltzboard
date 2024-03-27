import { attributePreferedSignal } from "../controller/attribute";
import { pinnedKeysSignal } from "../controller/dashboard";
import { transformationPreferredSignal } from "../controller/transformation";
import { WaltzboardChartModel } from "../types/API";
import { ChartView, TitleToken } from "../types/ChartView";

export const toChartView = (chart: WaltzboardChartModel): ChartView => {
  const specObject = JSON.parse(chart.spec);
  const title = chart.title;
  const titleToken: TitleToken[] = title.map((t) => {
    return {
      text: t,
      isPrefered:
        attributePreferedSignal.peek().includes(t) ||
        transformationPreferredSignal.peek().includes(t.toLowerCase()),
    };
  });
  specObject.autosize = { type: "fit", contains: "padding" };
  specObject.title = null;
  // if (specObject.encoding && specObject.encoding.color) {
  //   specObject.encoding.color.legend = { title: null };
  // }
  specObject.background = null;
  if ("color" in specObject.encoding) {
    specObject.encoding.color.legend = { orient: "bottom" };
  }

  return {
    key: chart.key,
    spec: specObject,
    statistics: chart.statistics,
    isPinned: pinnedKeysSignal.value.includes(chart.key),
    chartResults: undefined,
    title,
    titleToken,
  };
};
