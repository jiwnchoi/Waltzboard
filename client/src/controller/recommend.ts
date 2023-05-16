import { computed, signal } from "@preact/signals-react"
import { RecommendBody, RecommendResponse, TrainBody, TrainResponse } from "../types/API"
import { weightSignal } from "./oracleWeight"
import { attributeContrainedSignal, attributePreferedSignal } from "./attribute"
import { chartTypeConstrainedSignal, chartTypePreferredSignal } from "./chartType"
import axios from "axios"
import { URI } from "../../config"
import { chartKeysSignal, dashboardSignal } from "./dashboard"
import { ChartView, TitleToken } from "../types/ChartView"

const recommendBodySignal = computed<RecommendBody>(() => {
    return {
        chartKeys: chartKeysSignal.value,
        nResults: 5,
    }
})

const recommendedChartsSignal = signal<ChartView[]>([])

const isRecommendingSignal = signal<boolean>(false)

const recommendChart = async () => {
    const response: RecommendResponse = (await axios.post(`${URI}/recommend`, recommendBodySignal.peek())).data
    recommendedChartsSignal.value = response.charts.map((chart, i) => {
        const specObject = JSON.parse(chart.spec);
        const title: string[] = JSON.parse(specObject.description!);
        const titleToken: TitleToken[] = title.map((t) => {
            return {
                text: t,
                isPrefered: attributePreferedSignal.value.includes(t),
            };
        });
        specObject.autosize = { type: 'fit', contains: 'padding' };
        if (specObject.encoding && specObject.encoding.color) {
            specObject.encoding.color.legend = { title: null };
        }
        return {
            key: chart.key,
            spec: specObject,
            statistics: chart.statistics,
            title: titleToken,
            isPinned: false,
        };
    })
    isRecommendingSignal.value = false
}


export { recommendChart, isRecommendingSignal, recommendedChartsSignal }