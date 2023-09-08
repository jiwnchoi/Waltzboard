import { Badge, Center, Collapse, Divider, Flex, Icon, Text } from '@chakra-ui/react';
import {
  RiArrowDownSLine,
  RiArrowUpSLine,
  RiDeleteBinLine,
  RiPushpinFill,
  RiPushpinLine,
} from 'react-icons/ri';
import { TbExchange } from 'react-icons/tb';
import { VegaLite } from 'react-vega';
import { Handler } from 'vega-tooltip';
import type { ChartView } from '../types/ChartView';
import { removeChart, togglePinChart } from '../controller/dashboard';
import { useSignal } from '@preact/signals-react';

const StatisticFeatureBadge = ({ feature }: { feature: string | null }) => {
  if (feature === null) return null;
  return <Badge>{feature.replace('has_', '')}</Badge>;
};
interface ChartViewProps {
  chart: ChartView;
  width: number;
  height: number;
}
const ChartView = ({ chart, width, height }: ChartViewProps) => {
  const showStatistics = useSignal(false);
  const toggleShowStatistics = () => {
    showStatistics.value = !showStatistics.value;
  };
  return (
    <Flex flexDir={'column'} w={'full'} h="fit-content" p={2}>
      <Flex flexDir={'row'} justifyContent={'space-between'} align="top" mb={2}>
        <Icon
          mr={4}
          as={chart.isPinned ? RiPushpinFill : RiPushpinLine}
          boxSize={4}
          onClick={() => {
            togglePinChart(chart.key);
          }}
          _hover={{ cursor: 'pointer' }}
        />
        <Text w="full" fontSize={'sm'} textAlign="center">
          {chart.titleToken.map((t, index) =>
            t.isPrefered ? (
              <Text key={index} as="span" fontWeight={800} color="pink.400">
                {`${t.text} `}
              </Text>
            ) : (
              <Text key={index} as="span" fontWeight={500}>
                {`${t.text} `}
              </Text>
            )
          )}
        </Text>
        <Icon
          ml={4}
          as={RiDeleteBinLine}
          boxSize={4}
          onClick={() => {
            removeChart(chart.key);
          }}
          _hover={{ cursor: 'pointer' }}
        />
      </Flex>
      <Center height="full" px={4} mb={2}>
        <VegaLite
          height={height}
          width={width}
          spec={chart.spec}
          actions={false}
          tooltip={new Handler().call}
        />
      </Center>
      <Divider mb={2} />
      <Flex flexDir={'row'} justifyContent={'space-between'} align="center">
        <Text fontSize={'sm'} textAlign="center" fontWeight={400} mr="auto">
          Statistics
        </Text>
        {showStatistics.value ? (
          <Icon as={RiArrowDownSLine} boxSize={4} onClick={toggleShowStatistics} />
        ) : (
          <Icon as={RiArrowUpSLine} boxSize={4} onClick={toggleShowStatistics} />
        )}
      </Flex>

      <Collapse in={showStatistics.value} animateOpacity>
        <Flex flexDir={'column'} gap={2} mt={2}>
          {Object.keys(chart.statistics).map((key, i) => {
            if (chart.statistics[key].filter((f) => f !== null).length === 0) return null;
            return (
              <Flex gap={1} key={`stat-${i}`}>
                <Text fontSize={'sm'} textAlign="center" fontWeight={400} mr="auto">
                  {key.replace("['", '').replace("']", '').replace("', '", ' & ')}
                </Text>
                {chart.statistics[key].map((feature) => (
                  <StatisticFeatureBadge feature={feature} />
                ))}
              </Flex>
            );
          })}
        </Flex>
      </Collapse>
    </Flex>
  );
};

export default ChartView;
