import { computed, signal } from "@preact/signals-react"
import axios from "axios"
import { URI } from "../../config"
import { RecommendBody, RecommendResponse } from "../types/API"
import { ChartView, TitleToken } from "../types/ChartView"
import { attributePreferedSignal } from "./attribute"
import { chartKeysSignal } from "./dashboard"

const recommendBodySignal = computed<RecommendBody>(() => {
    return {
        chartKeys: chartKeysSignal.value,
        nResults: 5,
    }
})

const recommendedChartsSignal = signal<ChartView[]>([])

const isRecommendingSignal = signal<boolean>(false)

const recommendChart = async () => {
    console.log(recommendBodySignal.peek())
    const response: RecommendResponse = (await axios.post(`${URI}/recommend`, recommendBodySignal.peek())).data
    recommendedChartsSignal.value = response.charts.map((chart, i) => {
        const specObject = JSON.parse(chart.spec);
        specObject.title = null
        // const title: string[] = JSON.parse(specObject.description!);
        const title: string[] = chart.title;
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
            titleToken,
            title,
            isPinned: false,
        };
    })
    console.log(recommendedChartsSignal.peek())
    isRecommendingSignal.value = false
}


export { isRecommendingSignal, recommendChart, recommendedChartsSignal }
