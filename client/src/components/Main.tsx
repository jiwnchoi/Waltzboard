import { Button, Flex, Input, Select, SimpleGrid, Text, VStack } from '@chakra-ui/react';
import { batch } from '@preact/signals-react';
import { useRef } from 'react';
import { attributesSignal } from '../controller/attribute';
import { chartTypesSignal } from '../controller/chartType';
import {
  currentScoreSignal,
  dashboardSignal,
  isProcessingSignal,
  sampleDashboard,
} from '../controller/dashboard';
import {
  numFiltersSignal,
  numSampleSignal,
  numVisSignal,
  setNumFilters,
  setNumSample,
  setNumVis,
} from '../controller/parameters';
import { selectedTaskTypeSignal, taskTypesSignal } from '../controller/taskType';
import Attribute from './AttributeSelector';
import { ChartTypeSelector } from './ChartTypeSelector';
import ChartView from './ChartView';
import { Section } from './Layout';
import { ResultPlot } from './ResultPlot';
import WeightSlider from './WeightSlider';

export const Main = () => {
  const numChartRef = useRef<HTMLInputElement>(null);
  const numSampleRef = useRef<HTMLInputElement>(null);
  const numFilterRef = useRef<HTMLInputElement>(null);
  console.log('main');
  return (
    <Flex w="full" minH="80vh" flexDir={'row'} justifyContent="space-between" px={4} gap={4}>
      <Flex flexDir={'column'} w={200} gap={2} h="fit-content">
        <Button
          boxShadow={'sm'}
          colorScheme="blue"
          color="white"
          loadingText="Processing..."
          size="xs"
          bgColor="#5677A4"
          w="full"
          isLoading={isProcessingSignal.value ? true : false}
          onClick={() => {
            isProcessingSignal.value = true;
            batch(() => {
              setNumVis(parseInt(numChartRef.current!.value));
              setNumSample(parseInt(numSampleRef.current!.value));
              setNumFilters(parseInt(numFilterRef.current!.value));
              sampleDashboard();
            });
          }}
        >
          {isProcessingSignal.value ? 'Processing...' : 'Run'}
        </Button>

        <Section title="Analytic Task" gap={1.5}>
          <Select
            placeholder="User Task"
            size="xs"
            value={selectedTaskTypeSignal.value.name}
            onChange={(e) => {
              selectedTaskTypeSignal.value = taskTypesSignal.value.find(
                (taskType) => taskType.name === e.target.value
              )!;
            }}
          >
            {taskTypesSignal.value.map((taskType, i) => (
              <option key={`taskType-${i}`}>{taskType.name}</option>
            ))}
          </Select>

          <WeightSlider title="specificity" />
          <WeightSlider title="interestingness" />
          <WeightSlider title="coverage" />
          <WeightSlider title="uniqueness" />
        </Section>
        <Section title="Parameters" gap={1.5} w={200}>
          <Flex flexDir={'row'} justifyContent={'space-between'} align="center">
            <Text fontSize={'xs'}># of Charts</Text>
            <Input
              size={'xs'}
              width={12}
              variant={'outline'}
              defaultValue={numVisSignal.value}
              ref={numChartRef}
            />
          </Flex>
          <Flex flexDir={'row'} justifyContent={'space-between'} align="center">
            <Text fontSize={'xs'}># of Samples</Text>
            <Input
              size={'xs'}
              width={12}
              variant={'outline'}
              defaultValue={numSampleSignal.value}
              ref={numSampleRef}
            />
          </Flex>
          <Flex flexDir={'row'} justifyContent={'space-between'} align="center">
            <Text fontSize={'xs'}># of Filters</Text>
            <Input
              size={'xs'}
              width={12}
              variant={'outline'}
              ref={numFilterRef}
              defaultValue={numFiltersSignal.value}
            />
          </Flex>
        </Section>
        <Section title="Chart Types" gap={1.5}>
          {chartTypesSignal.value.map((chartType, i) => (
            <ChartTypeSelector chartType={chartType} key={`chartType-${i}`} />
          ))}
        </Section>
        <Section title="Attributes" gap={1.5} w={200}>
          {attributesSignal.value.map((attribute, i) => (
            <Attribute attribute={attribute} key={`attribute-${i}`} />
          ))}
        </Section>
      </Flex>
      <SimpleGrid w="full" h="fit-content" spacing={4} minChildWidth={350}>
        {dashboardSignal.value.map((chart, i) => (
          <ChartView chart={chart} key={`chart-${i}`} width={350} height={150} />
        ))}
      </SimpleGrid>
      {/* <VStack w={300}>
        <Section title="Dashboard Info" gap={1.5} minH={200}>
          <ResultPlot width={300} height={20} target="score" />
          {currentScoreSignal.value.specificity !== 0 ? (
            <ResultPlot width={300} height={20} target="specificity" />
          ) : null}
          <ResultPlot width={300} height={20} target="interestingness" />
          <ResultPlot width={300} height={20} target="coverage" />
          <ResultPlot width={300} height={20} target="uniqueness" />
        </Section>
        <Section title="Recommend Chart" gap={1.5} minH={700}></Section>
      </VStack> */}
    </Flex>
  );
};
