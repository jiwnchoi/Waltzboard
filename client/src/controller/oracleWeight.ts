import { signal } from '@preact/signals-react';
import { OracleWeight } from '../types/OracleWeight';

const weightSignal = signal<OracleWeight>({
    specificity: 1,
    interestingness: 1,
    coverage: 1,
    uniqueness: 1,
});



export { weightSignal };
