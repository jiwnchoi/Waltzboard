import { Divider, Flex, Text } from '@chakra-ui/react';
import { useComputed } from '@preact/signals-react';
import { scaleLinear } from '@visx/scale';
import { BoxPlot } from '@visx/stats';
import { weightSignal } from '../controller/oracleWeight';
import { inferResponseSignal } from '../controller/infer';

type Target = 'score' | 'diversity' | 'coverage' | 'interestingness' | 'specificity' | 'parsimony';

interface ResultPlotProps {
  width: number;
  height: number;
  target: Target;
}

const getMinMax = (target: Target) => {
  if (target === 'score') {
    return [
      0,
      weightSignal.peek().specificity +
        weightSignal.peek().interestingness +
        weightSignal.peek().coverage +
        weightSignal.peek().diversity +
        weightSignal.peek().parsimony,
    ];
  } else if (target === 'parsimony') {
    return [0, 2];
  } else {
    return [0, 1];
  }
};

export const ResultPlot = ({ width, height, target }: ResultPlotProps) => {
  const resultDistribution = useComputed(() => inferResponseSignal.value.dist[target]);
  const sortedDistribution = useComputed(() =>
    resultDistribution.value.slice().sort((a, b) => a - b)
  );

  const stats = useComputed(() => {
    return {
      min: Math.min(...resultDistribution.value),
      max: Math.max(...resultDistribution.value),
      median: sortedDistribution.value[Math.floor(sortedDistribution.value.length / 2)],
      firstQuartile: sortedDistribution.value[Math.floor(sortedDistribution.value.length / 4)],
      thirdQuartile: sortedDistribution.value[Math.floor(sortedDistribution.value.length * 0.75)],
    };
  });
  const valueScale = useComputed(() =>
    scaleLinear({ range: [0, width * 0.8], round: true, domain: getMinMax(target) })
  );

  const currentScore = inferResponseSignal.value.result[target];

  return (
    <Flex width={'full'} flexDir={'column'} gap={1}>
      <Flex flexDir={'row'} align="center" gap={1}>
        <Text fontSize={'xs'} fontWeight={500}>
          {`${target.charAt(0).toUpperCase() + target.slice(1)}`}
        </Text>
        <Text fontSize={'xs'} fontWeight={700}>
          {`${currentScore.toFixed(2)}/${getMinMax(target)[1].toFixed(2)}`}
        </Text>
      </Flex>
      <svg height={height} width={240}>
        <BoxPlot
          min={stats.value.min}
          max={stats.value.max}
          firstQuartile={stats.value.firstQuartile}
          thirdQuartile={stats.value.thirdQuartile}
          median={stats.value.median}
          boxWidth={height}
          outliers={[currentScore]}
          rx={0}
          ry={0}
          outlierProps={{
            fill: '#DD6CA4',
            fillOpacity: 1,
          }}
          fill="gray"
          fillOpacity={0.2}
          stroke="black"
          horizontal={true}
          valueScale={valueScale.value}
        />
      </svg>
      <Divider mt={1} />
    </Flex>
  );
};
