import { Badge, Center, Flex, FlexProps, Text } from '@chakra-ui/react';
import { VegaLite } from 'react-vega';
import { Handler } from 'vega-tooltip';
import { appendChartToDashboard } from '../controller/recommend';
import type { ChartView } from '../types/ChartView';

interface ChartViewProps extends FlexProps {
  chart: ChartView;
  chartWidth: number;
  chartHeight: number;
}
const RecommendedChartView = (props: ChartViewProps) => {
  return (
    <Flex
      flexDir={'column'}
      {...props}
      onClick={() => appendChartToDashboard(props.chart)}
      _hover={{
        backgroundColor: 'gray.100',
        cursor: 'pointer',
        borderRadius: 'md',
      }}
    >
      <Flex
        flexDir={'row'}
        justifyContent={'space-between'}
        align="top"
        w={'full'}
      >
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
      </Flex>
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

export default RecommendedChartView;
