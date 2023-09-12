interface AttributeDist {
  name: string;
  x: number;
  y: number;
  z: number;
}

interface ChartTypeDist {
  name: string;
  prob: number;
}

interface TransformationDist {
  name: string;
  x: number;
  y: number;
  z: number;
}

export type { AttributeDist, ChartTypeDist, TransformationDist };
