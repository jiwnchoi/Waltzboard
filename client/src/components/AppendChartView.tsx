import {
  Box,
  Button,
  Center,
  Flex,
  FlexProps,
  Select,
  Spacer,
  Text,
} from '@chakra-ui/react';
import { ChartView } from '../types/ChartView';
import { VegaLite } from 'react-vega';
import { Handler } from 'vega-tooltip';
import { inputChart, inputTuple, isTupleValid } from '../controller/append';
import { chartTypesSignal } from '../controller/chartType';
import { attributesSignal } from '../controller/attribute';
import { transformationsSignal } from '../controller/transformation';
import { appendChart } from '../controller/dashboard';

interface ChartViewProps extends FlexProps {
  chart: ChartView;
  chartWidth: number;
  chartHeight: number;
}

export const ChartAppendPreview = () => {
  return (
    <Flex flexDir={'column'} w={270}>
      {inputChart.value && (
        <RecommendChartView
          chart={inputChart.value}
          chartWidth={250}
          chartHeight={125}
        />
      )}
      {!inputChart.value && (
        <Center w={'full'} h={130} textAlign={'center'} p={8}>
          Please input valid tuple and click the chart image
        </Center>
      )}
      <Spacer />
    </Flex>
  );
};

export const ChartAppendView = () => {
  return (
    <Flex flexDir={'column'} p={2} bgColor={'white'} borderRadius={'md'}>
      <Text fontSize={'md'} fontWeight={600} mb={2}>
        Configure Chart
      </Text>
      <Flex
        flexDir={'row'}
        justifyContent={'space-between'}
        align="top"
        gap={4}
      >
        <Flex flexDir={'column'} w={260}>
          <Flex
            flexDir={'row'}
            justifyContent={'space-between'}
            align="center"
            mb={2}
          >
            <Text
              fontSize={'sm'}
              minW={'60px'}
              align={'center'}
              fontWeight={700}
            >
              Chart Type
            </Text>
            <Select
              bgColor={'white'}
              fontSize={'sm'}
              size="sm"
              ml="2"
              onChange={(e) => {
                const oldCurrentState = [...inputTuple.peek()];
                oldCurrentState[0] = e.target.value;
                inputTuple.value = oldCurrentState;
              }}
            >
              <option key={`appendNone`} value={''}>
                None
              </option>
              {chartTypesSignal.value.map((chartType) => (
                <option key={`append${chartType.mark}`} value={chartType.mark}>
                  {chartType.name}
                </option>
              ))}
            </Select>
          </Flex>
          <Flex
            flexDir={'row'}
            justifyContent={'space-between'}
            align="center"
            mb={2}
          >
            <Text
              fontSize={'sm'}
              minW={'60px'}
              align={'center'}
              fontWeight={700}
            >
              X
            </Text>
            <Select
              bgColor={'white'}
              fontSize={'sm'}
              size="sm"
              ml="2"
              onChange={(e) => {
                const oldCurrentState = [...inputTuple.peek()];
                oldCurrentState[1] = e.target.value;
                inputTuple.value = oldCurrentState;
              }}
            >
              <option key={`appendNone`} value={''}>
                None
              </option>
              {attributesSignal.value.map((a) => (
                <option key={`append${a.name}x`} value={a.name}>
                  {a.name}
                </option>
              ))}
            </Select>
            <Select
              bgColor={'white'}
              fontSize={'sm'}
              ml="2"
              size="sm"
              maxW={'80px'}
              onChange={(e) => {
                const oldCurrentState = [...inputTuple.peek()];
                oldCurrentState[4] = e.target.value;
                inputTuple.value = oldCurrentState;
              }}
            >
              {transformationsSignal.value.map((a) => (
                <option key={`append${a.type}y`} value={a.type}>
                  {a.name}
                </option>
              ))}
            </Select>
          </Flex>
          <Flex
            flexDir={'row'}
            justifyContent={'space-between'}
            align="center"
            mb={2}
          >
            <Text
              fontSize={'sm'}
              minW={'60px'}
              align={'center'}
              fontWeight={700}
            >
              Y
            </Text>
            <Select
              bgColor={'white'}
              fontSize={'sm'}
              size="sm"
              ml="2"
              onChange={(e) => {
                const oldCurrentState = [...inputTuple.peek()];
                oldCurrentState[2] = e.target.value;
                inputTuple.value = oldCurrentState;
              }}
            >
              <option key={`appendNone`} value={''}>
                None
              </option>
              {attributesSignal.value.map((a) => (
                <option key={`append${a.name}x`} value={a.name}>
                  {a.name}
                </option>
              ))}
            </Select>
            <Select
              bgColor={'white'}
              fontSize={'sm'}
              ml="2"
              size="sm"
              maxW={'80px'}
              onChange={(e) => {
                const oldCurrentState = [...inputTuple.peek()];
                oldCurrentState[5] = e.target.value;
                inputTuple.value = oldCurrentState;
              }}
            >
              {transformationsSignal.value.map((a) => (
                <option key={`append${a.type}y`} value={a.type}>
                  {a.name}
                </option>
              ))}
            </Select>
          </Flex>
          <Flex
            flexDir={'row'}
            justifyContent={'space-between'}
            align="center"
            mb={2}
          >
            <Text
              fontSize={'sm'}
              minW={'60px'}
              align={'center'}
              fontWeight={700}
            >
              Z
            </Text>
            <Select
              bgColor={'white'}
              fontSize={'sm'}
              size="sm"
              ml="2"
              onChange={(e) => {
                const oldCurrentState = [...inputTuple.peek()];
                oldCurrentState[3] = e.target.value;
                inputTuple.value = oldCurrentState;
              }}
            >
              <option key={`appendNone`} value={''}>
                None
              </option>
              {attributesSignal.value.map((a) => (
                <option key={`append${a.name}x`} value={a.name}>
                  {a.name}
                </option>
              ))}
            </Select>
            <Select
              bgColor={'white'}
              fontSize={'sm'}
              ml="2"
              size="sm"
              maxW={'80px'}
              onChange={(e) => {
                const oldCurrentState = [...inputTuple.peek()];
                oldCurrentState[6] = e.target.value;
                inputTuple.value = oldCurrentState;
              }}
            >
              {transformationsSignal.value.map((a) => (
                <option key={`append${a.type}y`} value={a.type}>
                  {a.name}
                </option>
              ))}
            </Select>
          </Flex>
        </Flex>
        <ChartAppendPreview />
      </Flex>
    </Flex>
  );
};
export const RecommendChartView = (props: ChartViewProps) => {
  return (
    <Flex
      flexDir={'column'}
      {...props}
      bgColor={'white'}
      borderRadius="md"
      mb={2}
      p={2}
      pt={0}
      _hover={{
        cursor: 'pointer',
        bgColor: 'gray.100',
      }}
      onClick={() => appendChart(props.chart)}
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
