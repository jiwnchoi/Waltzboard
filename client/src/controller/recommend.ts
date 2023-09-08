import { computed, signal, effect } from "@preact/signals-react"
import axios from "axios"
import { URI } from "../../config"
import { RecommendBody, RecommendResponse } from "../types/API"
import { ChartView, TitleToken } from "../types/ChartView"
import { attributePreferedSignal } from "./attribute"
import { chartKeysSignal, dashboardSignal } from "./dashboard"
import { transformationPreferredSignal } from "./transformation"
import { inferResponseSignal } from "./infer"

const recommendBodySignal = computed<RecommendBody>(() => {
    return {
        chartKeys: chartKeysSignal.value,
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
        specObject.background = null;
        if (specObject.encoding && specObject.encoding.color) {
            specObject.encoding.color.legend = { title: null };
        }
        return {
            key: chart.key,
            spec: specObject,
            statistics: chart.statistics,
            titleToken,
            title,
            chartResults: undefined,
            isPinned: false,
        };
    })
    isRecommendingSignal.value = false
}

const appendChartToDashboard = (chart: ChartView) => {
    console.log(chart)
    inferResponseSignal.value = {
        ... inferResponseSignal.peek(),
        charts : [
            ...inferResponseSignal.peek().charts,
            {
                key: chart.key,
                spec: JSON.stringify(chart.spec),
                title: chart.title,
                statistics: chart.statistics,
            }
        ]
    }
}

effect(() => {
    if (dashboardSignal.value.length > 0) {
        isRecommendingSignal.value = true
        recommendChart()
        isRecommendingSignal.value = false
    }
})


export { isRecommendingSignal, recommendChart, recommendedChartsSignal, appendChartToDashboard }
