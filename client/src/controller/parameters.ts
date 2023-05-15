import { computed, signal } from '@preact/signals-react'

const parametersSignal = signal({
    numVis: 12,
    numSample: 500,
    numFilters: 0,
})

const numVisSignal = computed(() => parametersSignal.value.numVis)
const numSampleSignal = computed(() => parametersSignal.value.numSample)
const numFiltersSignal = computed(() => parametersSignal.value.numFilters)

const setNumVis = (numVis: number) => {
    parametersSignal.value = {
        ...parametersSignal.value,
        numVis
    }
}

const setNumSample = (numSample: number) => {
    parametersSignal.value = {
        ...parametersSignal.value,
        numSample
    }
}

const setNumFilters = (numFilters: number) => {
    parametersSignal.value = {
        ...parametersSignal.value,
        numFilters
    }
}

export {
    numVisSignal,
    numSampleSignal,
    numFiltersSignal,
    setNumVis,
    setNumSample,
    setNumFilters
}
