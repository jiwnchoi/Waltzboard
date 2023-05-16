import { computed, signal } from '@preact/signals-react'

const configSignal = signal({
    robustness: 100,
    halvingRatio: 0.1,
    nEpoch: 100,
    nCandidate: 100,
    nChart: -1, // -1 is sample from trained distribution
})

export { configSignal }


