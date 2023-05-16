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
const ChartView = ({ chart, width, height }: ChartViewProps) => {
  return (
    <Flex
      flexDir={'column'}
      w={'full'}
      h="fit-content"
      bgColor="white"
      borderRadius={'md'}
      boxShadow="sm"
      p={2}
      gap={2}
    >
      <Flex flexDir={'row'} justifyContent={'space-between'} align="top">
        <Icon mr={2} as={TbExchange} boxSize={4} onClick={() => {}} />
        <Icon
          mr={4}
          as={chart.isPinned ? RiPushpinFill : RiPushpinLine}
          boxSize={4}
          onClick={() => {
            togglePinChart(chart.key);
          }}
        />
        <Text w="full" fontSize={'xs'} textAlign="center">
          {chart.title.map((t) =>
            t.isPrefered ? (
              <Text as="span" fontWeight={800} color="pink.400">
                {`${t.text} `}
              </Text>
            ) : (
              <Text as="span" fontWeight={500}>
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
        />
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
      {Object.keys(chart.statistics).map((key) => {
        if (chart.statistics[key].filter((f) => f !== null).length === 0) return null;
        return (
          <Flex gap={1}>
            <Text fontSize={'xs'} textAlign="center" fontWeight={400} mr="auto">
              {key.replace("['", '').replace("']", '').replace("', '", ' & ')}
            </Text>
            {chart.statistics[key].map((feature) => (
              <StatisticFeatureBadge feature={feature} />
            ))}
          </Flex>
        );
      })}
    </Flex>
  );
};

export default ChartView;
