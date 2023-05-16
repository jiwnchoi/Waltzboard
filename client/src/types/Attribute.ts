interface AttributeFetched {
    name: string;
    type: 'Q' | 'C' | 'N' | 'T';
}

interface Attribute extends AttributeFetched {
    prefer: boolean;
    ignore: boolean;
}

export type { AttributeFetched, Attribute };
