import { Point } from '@visx/point';
import { scaleLinear } from '@visx/scale';
import { Line, LineRadial } from '@visx/shape';
import { Text } from '@visx/text';
import { inferResponseSignal } from '../controller/infer';
import { ScaleSVG } from '@visx/responsive';
import { Group } from '@visx/group';
import { schemeCategory10 } from 'd3-scale-chromatic';
import { scoreDistSignal } from '../controller/train';

interface Margin {
  top: number;
  bottom: number;
  left: number;
  right: number;
}

interface ScoreDistViewProps {
  width: number;
  height: number;
}

type RadarAxisProps = {
  margin: Margin;
} & ScoreDistViewProps;

type RadarMarkProps = {
  color: string;
  data: number[];
} & RadarAxisProps;

type RadarRangeMarkProps = {
  color: string;
  dataMin: number[];
  dataMax: number[];
} & RadarAxisProps;

const LABEL: string[] = ['Spe', 'Int', 'Cov', 'Div', 'Par'];
const margin = { top: 0, bottom: 40, left: 35, right: 35 };

const genAngles = (length: number) =>
  [...new Array(length + 1)].map((_, i) => ({
    angle: i * (360 / length) + (length % 2 === 0 ? 0 : 360 / length / 2),
  }));

const genPoints = (length: number, radius: number) => {
  const step = (Math.PI * 2) / length;
  return [...new Array(length)].map((_, i) => ({
    x: radius * Math.sin(i * step),
    y: radius * Math.cos(i * step),
  }));
};

const genPolygonPoints = (data: number[], scale: (n: number) => number) => {
  const step = (Math.PI * 2) / data.length;
  const points: { x: number; y: number }[] = new Array(data.length).fill({
    x: 0,
    y: 0,
  });
  const pointString: string = new Array(data.length + 1).fill('').reduce((res, _, i) => {
    if (i > data.length) return res;
    const xVal = scale(data[i - 1]) * Math.sin(i * step);
    const yVal = scale(data[i - 1]) * Math.cos(i * step);
    points[i - 1] = { x: xVal, y: yVal };
    res += `${xVal},${yVal} `;
    return res;
  });

  return { points, pointString };
};

const radialScale = scaleLinear<number>({
  domain: [360, 0],
  range: [0, Math.PI * 2],
});

export const RadarAxis = (props: RadarAxisProps & { data: number[] }) => {
  const { width, height, margin, data } = props;
  const yMax = height - margin.top - margin.bottom;
  const xMax = width - margin.left - margin.right;
  const radius = Math.min(xMax, yMax) / 2;
  const labelRadius = Math.min(xMax, yMax) / 2 + 20;

  const webs = genAngles(5);
  const points = genPoints(5, radius);
  const labelPoints = genPoints(5, labelRadius);

  const zeroPoint = new Point({ x: 0, y: 0 });

  return (
    <>
      {[...new Array(5)].map((_, i) => (
        <LineRadial
          key={`web-${i}`}
          data={webs}
          angle={(d) => radialScale(d.angle) ?? 0}
          radius={((i + 1) * radius) / 5}
          fill="none"
          stroke={'#E2E2E2'}
          strokeWidth={1}
          strokeOpacity={0.8}
          strokeLinecap="round"
        />
      ))}
      {[...new Array(5)].map((_, i) => (
        <Line key={`radar-line-${i}`} from={zeroPoint} to={points[i]} stroke={'#E2E2E2'} />
      ))}
      {labelPoints.map((value, i) => (
        <>
          <Text
            key={`radar-label-${i}`}
            x={labelPoints[i].x}
            y={labelPoints[i].y}
            dy={-8}
            fontSize={14}
            textAnchor={'middle'}
            verticalAnchor="middle"
            fill="gray"
            fontWeight="bold"
          >
            {LABEL[(i + 4) % LABEL.length]}
          </Text>
          <Text
            key={`radar-score-${i}`}
            x={labelPoints[i].x}
            y={labelPoints[i].y}
            fontSize={14}
            dy={8}
            textAnchor={'middle'}
            verticalAnchor="middle"
            fill={schemeCategory10[0]}
            fontWeight="bold"
          >
            {data[(i + 4) % LABEL.length].toFixed(2)}
          </Text>
        </>
      ))}
    </>
  );
};

export const RadarRangeMark = (props: RadarRangeMarkProps) => {
  const { width, height, margin, color, dataMin, dataMax } = props;
  const yMax = height - margin.top - margin.bottom;
  const xMax = width - margin.left - margin.right;
  const radius = Math.min(xMax, yMax) / 2;

  const yScale = scaleLinear<number>({
    domain: [0, 1],
    range: [0, radius],
  });

  const minPoints = genPolygonPoints(dataMin, (d) => yScale(d) ?? 0);
  const maxPoints = genPolygonPoints(dataMax, (d) => yScale(d) ?? 0);

  return (
    <>
      <mask id="radar-mask">
        <rect x={-radius} y={-radius} width={radius * 2} height={radius * 2} fill="white" />
        <polygon points={minPoints.pointString} fill="black" />
      </mask>
      <polygon
        points={maxPoints.pointString}
        fill={color}
        fillOpacity={0.4}
        // stroke={color}
        // strokeWidth={1}
        mask="url(#radar-mask)"
      />
      {/* {minPoints.points.map((point, i) => (
        <circle key={`min-point-${i}`} cx={point.x} cy={point.y} r={1} fill={color} />
      ))}
      {maxPoints.points.map((point, i) => (
        <circle key={`max-point-${i}`} cx={point.x} cy={point.y} r={1} fill={color} />
      ))} */}
    </>
  );
};

export const RadarMark = (props: RadarMarkProps) => {
  const { width, height, margin, color, data } = props;
  const yMax = height - margin.top - margin.bottom;
  const xMax = width - margin.left - margin.right;
  const radius = Math.min(xMax, yMax) / 2;

  const yScale = scaleLinear<number>({
    domain: [0, 1],
    range: [0, radius],
  });

  const polygonPoints = genPolygonPoints(data, (d) => yScale(d) ?? 0);
  return (
    <>
      <polygon
        points={polygonPoints.pointString}
        fill={color}
        fillOpacity={0}
        stroke={color}
        strokeWidth={1.5}
      />
      {polygonPoints.points.map((point, i) => (
        <circle key={`radar-point-${i}`} cx={point.x} cy={point.y} r={1} fill={color} />
      ))}
    </>
  );
};
export const ScoreDistView = ({ width, height }: ScoreDistViewProps) => {
  const scoreDist = scoreDistSignal.value;
  const sortedScoreDist = {
    score: scoreDist.score.sort((a, b) => a - b),
    specificity: scoreDist.specificity.sort((a, b) => a - b),
    interestingness: scoreDist.interestingness.sort((a, b) => a - b),
    coverage: scoreDist.coverage.sort((a, b) => a - b),
    diversity: scoreDist.diversity.sort((a, b) => a - b),
    parsimony: scoreDist.parsimony.sort((a, b) => a - b),
  };

  const q1Scores = {
    score: sortedScoreDist.score[Math.floor(sortedScoreDist.score.length / 4)],
    specificity: sortedScoreDist.specificity[Math.floor(sortedScoreDist.specificity.length / 4)],
    interestingness:
      sortedScoreDist.interestingness[Math.floor(sortedScoreDist.interestingness.length / 4)],
    coverage: sortedScoreDist.coverage[Math.floor(sortedScoreDist.coverage.length / 4)],
    diversity: sortedScoreDist.diversity[Math.floor(sortedScoreDist.diversity.length / 4)],
    parsimony: sortedScoreDist.parsimony[Math.floor(sortedScoreDist.parsimony.length / 4)],
  };
  const q3Scores = {
    score: sortedScoreDist.score[Math.floor((sortedScoreDist.score.length * 3) / 4)],
    specificity:
      sortedScoreDist.specificity[Math.floor((sortedScoreDist.specificity.length * 3) / 4)],
    interestingness:
      sortedScoreDist.interestingness[Math.floor((sortedScoreDist.interestingness.length * 3) / 4)],
    coverage: sortedScoreDist.coverage[Math.floor((sortedScoreDist.coverage.length * 3) / 4)],
    diversity: sortedScoreDist.diversity[Math.floor((sortedScoreDist.diversity.length * 3) / 4)],
    parsimony: sortedScoreDist.parsimony[Math.floor((sortedScoreDist.parsimony.length * 3) / 4)],
  };
  const medianScores = {
    score: sortedScoreDist.score[Math.floor(sortedScoreDist.score.length / 2)],
    specificity: sortedScoreDist.specificity[Math.floor(sortedScoreDist.specificity.length / 2)],
    interestingness:
      sortedScoreDist.interestingness[Math.floor(sortedScoreDist.interestingness.length / 2)],
    coverage: sortedScoreDist.coverage[Math.floor(sortedScoreDist.coverage.length / 2)],
    diversity: sortedScoreDist.diversity[Math.floor(sortedScoreDist.diversity.length / 2)],
    parsimony: sortedScoreDist.parsimony[Math.floor(sortedScoreDist.parsimony.length / 2)],
  };

  const minScores = {
    score: sortedScoreDist.score[0],
    specificity: sortedScoreDist.specificity[0],
    interestingness: sortedScoreDist.interestingness[0],
    coverage: sortedScoreDist.coverage[0],
    diversity: sortedScoreDist.diversity[0],
    parsimony: sortedScoreDist.parsimony[0],
  };

  const maxScores = {
    score: sortedScoreDist.score[sortedScoreDist.score.length - 1],
    specificity: sortedScoreDist.specificity[sortedScoreDist.specificity.length - 1],
    interestingness: sortedScoreDist.interestingness[sortedScoreDist.interestingness.length - 1],
    coverage: sortedScoreDist.coverage[sortedScoreDist.coverage.length - 1],
    diversity: sortedScoreDist.diversity[sortedScoreDist.diversity.length - 1],
    parsimony: sortedScoreDist.parsimony[sortedScoreDist.parsimony.length - 1],
  };
  const currentScore = inferResponseSignal.value.result;

  return (
    <ScaleSVG width={width} height={height}>
      <Group top={height / 2} left={width / 2}>
        <RadarAxis
          width={width}
          height={height}
          margin={margin}
          data={[
            currentScore.specificity,
            currentScore.interestingness,
            currentScore.coverage,
            currentScore.diversity,
            currentScore.parsimony,
          ]}
        />
        <RadarRangeMark
          width={width}
          height={height}
          margin={margin}
          color={'gray'}
          dataMin={[
            q1Scores.specificity,
            q1Scores.interestingness,
            q1Scores.coverage,
            q1Scores.diversity,
            q1Scores.parsimony,
          ]}
          dataMax={[
            q3Scores.specificity,
            q3Scores.interestingness,
            q3Scores.coverage,
            q3Scores.diversity,
            q3Scores.parsimony,
          ]}
        />
        <RadarMark
          width={width}
          height={height}
          margin={margin}
          color={schemeCategory10[0]}
          data={[
            currentScore.specificity,
            currentScore.interestingness,
            currentScore.coverage,
            currentScore.diversity,
            currentScore.parsimony,
          ]}
        />
      </Group>
    </ScaleSVG>
  );
};
