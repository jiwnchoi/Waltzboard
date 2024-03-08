interface TransformationFetched {
  name: string;
  type: string;
}

interface Transformation extends TransformationFetched {
  ignore: boolean;
  prefer: boolean;
}

export type { Transformation, TransformationFetched };
