import { batch, effect, signal } from "@preact/signals-react";
import axios from "axios";
import { URI } from "../config";
import { Configs, InitResponse } from "../types/API";
import { attributesSignal } from "./attribute";
import { chartTypesSignal } from "./chartType";
import { transformationsSignal } from "./transformation";
import { resetInferResponseSignal } from "./infer";
import { isAppendPanelOpen, toggleAppendPanel } from "./append";
import { pinnedKeysSignal } from "./dashboard";
import { inspectionIndexSignal, variantChartsSignal } from "./details";

const initializedSignal = signal<boolean>(false);
const isInitializing = signal<boolean>(false);

export const configSignal = signal<Configs>({
  userId: null,
  dataset: "Movies",
  n_beam: 10,
  n_candidates: 50,
  n_epoch: 20,
  n_search_space: 100,
  robustness: 1,
  n_min_chart: 2,
  acceleration: 1.0,
});

const init = async (code: string) => {
  isInitializing.value = true;
  resetInferResponseSignal();
  if (isAppendPanelOpen.peek()) toggleAppendPanel();
  pinnedKeysSignal.value = [];
  variantChartsSignal.value = [];
  inspectionIndexSignal.value = -1;

  const response: InitResponse = (
    await axios.post(`${URI}/init`, { ...configSignal.peek(), userId: code })
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
        // ignore: ["tick", "arc"].includes(chartType.mark),
        ignore: false,
      };
    });
    transformationsSignal.value = response.transformations.map(
      (transformation) => {
        return {
          ...transformation,
          prefer: false,
          ignore: false,
          // ignore: ["min", "max", "day"].includes(transformation.type),
        };
      },
    );
    // taskTypesSignal.value = response.taskTypes.map((taskType) => {
    //     return {
    //         ...taskType,
    //         chartTypes: taskType.chartTypes.map((chartType) => chartTypesSignal.peek().find((ct) => ct.name === chartType.name) as ChartType),
    //     };
    // });
    // selectedTaskTypeSignal.value = { ...selectedTaskTypeSignal.peek(), chartTypes: chartTypesSignal.peek() }
    initializedSignal.value = true;
    isInitializing.value = false;
  });
};

export { init, initializedSignal, isInitializing };
