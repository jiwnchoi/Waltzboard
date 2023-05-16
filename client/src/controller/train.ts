import { computed, signal } from "@preact/signals-react"
import type { TrainBody, TrainResponse } from "../types/API"
import { weightSignal } from "./oracleWeight"
import { attributeContrainedSignal, attributePreferedSignal } from "./attribute"
import { chartTypeConstrainedSignal, chartTypePreferredSignal } from "./chartType"
import axios from "axios"
import { URI } from "../../config"


const trainBodySignal = computed<TrainBody>(() => {
    const weight = weightSignal.value

    return {
        weight: weightSignal.value,
        preferences: [...attributePreferedSignal.value, ...chartTypePreferredSignal.value],
        constraints: [...attributeContrainedSignal.value, ...chartTypeConstrainedSignal.value]
    }
})


const trainGleaner = async () => {
    const response: TrainResponse = (await axios.post(`${URI}/train`, trainBodySignal.peek())).data
    isTrainingSignal.value = false
    isTrainedSignal.value = true
}

const isTrainingSignal = signal<boolean>(false)
const isTrainedSignal = signal<boolean>(false)


export { trainGleaner, isTrainingSignal, isTrainedSignal }