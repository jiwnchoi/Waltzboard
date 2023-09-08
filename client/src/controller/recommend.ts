import { computed, signal, effect } from "@preact/signals-react"
import axios from "axios"
import { URI } from "../../config"
import { RecommendBody, RecommendResponse } from "../types/API"
import { ChartView, TitleToken } from "../types/ChartView"
import { attributePreferedSignal } from "./attribute"
import { chartKeysSignal, dashboardSignal } from "./dashboard"
import { transformationPreferredSignal } from "./transformation"

const recommendBodySignal = computed<RecommendBody>(() => {
    return {
        chartKeys: chartKeysSignal.value,
        preferences: attributePreferedSignal.value,
        nResults: 5,
    }
})

const recommendedChartsSignal = signal<ChartView[]>([])

const isRecommendingSignal = signal<boolean>(false)

const recommendChart = async () => {
    isRecommendingSignal.value = true
    const response: RecommendResponse = (await axios.post(`${URI}/recommend`, recommendBodySignal.value)).data
    recommendedChartsSignal.value = response.charts.map((chart, i) => {
        const specObject = JSON.parse(chart.spec);
        specObject.title = null
        const title: string[] = chart.title;
        const titleToken: TitleToken[] = title.map((t) => {
            return {
                text: t,
                isPrefered: attributePreferedSignal.value.includes(t) || transformationPreferredSignal.value.includes(t),
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
            titleToken,
            title,
            isPinned: false,
        };
    })
    isRecommendingSignal.value = false
}

effect(() => {
    if (dashboardSignal.value.length > 0) {
        isRecommendingSignal.value = true
        recommendChart()
        isRecommendingSignal.value = false
    }
})


export { isRecommendingSignal, recommendChart, recommendedChartsSignal }
