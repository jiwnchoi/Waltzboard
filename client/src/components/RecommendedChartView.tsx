import { Badge, Center, Divider, Flex, Icon, Text } from '@chakra-ui/react';
import { RiDeleteBinLine, RiPushpinFill, RiPushpinLine } from 'react-icons/ri';
import { TbExchange } from 'react-icons/tb';
import { VegaLite } from 'react-vega';
import { Handler } from 'vega-tooltip';
import type { ChartView } from '../types/ChartView';
import { removeChart, togglePinChart } from '../controller/dashboard';

const StatisticFeatureBadge = ({ feature }: { feature: string | null }) => {
  if (feature === null) return null;
  return <Badge>{feature.replace('has_', '')}</Badge>;
};
interface ChartViewProps {
  chart: ChartView;
  width: number;
  height: number;
}
const RecommendedChartView = ({ chart, width, height }: ChartViewProps) => {
  const spec = chart.spec;
  spec.config = {
    axis: {
      labelFontSize: 8,
      titleFontSize: 8,
    },
  };
  return (
    <Flex
      flexDir={'column'}
      w={'full'}
      h="fit-content"
      bgColor="white"
      borderRadius={'md'}
      boxShadow="sm"
      p={0}
      gap={1}
    >
      <Flex flexDir={'row'} justifyContent={'space-between'} align="top">
        <Text w="full" fontSize={'2xs'} lineHeight={'3'} textAlign="center">
          {chart.title.map((t, i) =>
            t.isPrefered ? (
              <Text key={`rec-chart-${i}`} as="span" fontWeight={800} color="pink.400">
                {`${t.text} `}
              </Text>
            ) : (
              <Text key={`rec-chart-${i}`} as="span" fontWeight={500}>
                {`${t.text} `}
              </Text>
            )
          )}
        </Text>
      </Flex>
      <Center height="full" px={4}>
        <VegaLite
          height={height}
          width={width}
          spec={chart.spec}
          actions={false}
          tooltip={new Handler().call}
        />
      </Center>
      <Divider />
    </Flex>
  );
};

export default RecommendedChartView;
