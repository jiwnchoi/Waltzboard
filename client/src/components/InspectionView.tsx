import {
  Badge,
  Center,
  Divider,
  Flex,
  FlexProps,
  Grid,
  GridItem,
  Spinner,
  Text,
} from '@chakra-ui/react';
import { format } from 'd3-format';
import { VegaLite } from 'react-vega';
import { Handler } from 'vega-tooltip';
import {
  inspectionChartSignal,
  inspectionIndexSignal,
  inspectionSignal,
  isInspectionLoadingSignal,
  isVariantsLoadingSignal,
  replaceChart,
} from '../controller/details';
import type { ChartView } from '../types/ChartView';
import { inferResponseSignal } from '../controller/infer';

interface ChartViewProps extends FlexProps {
  chart: ChartView;
  chartWidth: number;
  chartHeight: number;
}
const StatisticFeatureBadge = ({ feature }: { feature: string | null }) => {
  if (feature === null) return null;
  return (
    <GridItem>
      <Badge>{feature.replace('has_', '')}</Badge>
    </GridItem>
  );
};

export const InspectionView = () => {
  return (
    <Flex
      minW={'200px'}
      flexDir={'column'}
      bgColor={'white'}
      borderRadius="md"
      p={2}
      my={2}
    >
      <Text fontSize={'md'} fontWeight={600} mb={2}>
        Without this chart
      </Text>
      {isInspectionLoadingSignal.value && (
        <Center w="full" minH={180}>
          <Spinner size="md" />
        </Center>
      )}
      {!isInspectionLoadingSignal.value &&
        inspectionChartSignal.value?.chartResults &&
        Object.entries(inspectionChartSignal.value.chartResults).map(
          ([key, value]) => {
            const currentScore =
              inferResponseSignal.value.result[
                key as keyof typeof inferResponseSignal.value.result
              ];
            return (
              <Flex
                key={`inspect-${key}`}
                flexDir={'row'}
                justifyContent={'space-between'}
                alignItems={'center'}
                mb={3}
              >
                <Text color={'gray.500'} fontSize={'sm'} fontWeight={600}>
                  {key[0].toUpperCase() + key.slice(1)}
                </Text>
                <Text>
                  <Text
                    as={'span'}
                    fontSize={'sm'}
                    fontWeight={800}
                    color={
                      currentScore == value
                        ? 'black'
                        : currentScore > value
                        ? 'green.500'
                        : 'red.500'
                    }
                  >
                    {format('.2f')(currentScore - value)}
                  </Text>
                  {/* <Text as={'span'} fontSize={'sm'}>
                    {key === 'score' ? `/4.00` : `/1.00`}
                  </Text> */}
                </Text>
              </Flex>
            );
          }
        )}
    </Flex>
  );
};

export const InsightsView = () => {
  return (
    <Flex
      flexDir={'column'}
      bgColor={'white'}
      borderRadius="md"
      p={2}
      my={2}
      w={336}
    >
      <Text fontSize={'md'} fontWeight={600} mb={2}>
        This chart contains these insights
      </Text>

      {inspectionChartSignal.value && (
        <Flex flexDir={'column'} gap={2} mt={2} overflowY={'auto'} w={'320px'}>
          {inspectionChartSignal.value.statistics.map(
            ({ key, features }, i) => {
              return (
                <Flex
                  key={`stat-${i}`}
                  flexDir={'row'}
                  justifyContent={'space-between'}
                  alignItems={'center'}
                  w={'full'}
                >
                  <Text fontSize={'sm'} w={'140px'} mr={4}>
                    {key}
                  </Text>
                  <Grid w={'170px'} templateColumns={'repeat(2, 1fr)'} gap={1}>
                    {features.map((feature) => (
                      <StatisticFeatureBadge feature={feature} />
                    ))}
                  </Grid>
                </Flex>
              );
            }
          )}
        </Flex>
      )}
    </Flex>
  );
};

export const VariantChartView = (props: ChartViewProps) => {
  return (
    <Flex
      flexDir={'column'}
      {...props}
      bgColor={'white'}
      borderRadius="md"
      my={2}
      p={2}
      _hover={{
        cursor: 'pointer',
        bgColor: 'gray.100',
      }}
      onClick={() => {
        replaceChart(inspectionIndexSignal.value, props.chart);
      }}
    >
      <Center w="full" verticalAlign={'center'} minH="42px">
        <Text w="full" fontSize={'sm'} textAlign="center">
          {props.chart.titleToken.map((t, i) =>
            t.isPrefered ? (
              <Text
                key={`rec-chart-${i}`}
                as="span"
                fontWeight={800}
                color="pink.400"
              >
                {`${t.text} `}
              </Text>
            ) : (
              <Text key={`rec-chart-${i}`} as="span" fontWeight={500}>
                {`${t.text} `}
              </Text>
            )
          )}
        </Text>
      </Center>
      <Center height="full" px={4}>
        <VegaLite
          height={props.chartHeight}
          width={props.chartWidth}
          spec={props.chart.spec}
          actions={false}
          tooltip={new Handler().call}
        />
      </Center>
    </Flex>
  );
};
