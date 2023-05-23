import { Box, Button, Center, Flex, Input, Select, SimpleGrid, Text } from '@chakra-ui/react';
import { VegaLite } from 'react-vega';
import { attributesSignal } from '../controller/attribute';
import { chartTypesSignal } from '../controller/chartType';
import { configSignal } from '../controller/config';
import { dashboardSignal } from '../controller/dashboard';
import { inferDashboard, isInferingSignal } from '../controller/infer';
import {
  isRecommendingSignal,
  recommendChart,
  recommendedChartsSignal,
} from '../controller/recommend';
import { selectedTaskTypeSignal, taskTypesSignal } from '../controller/taskType';
import { isTrainedSignal, isTrainingSignal, trainGleaner } from '../controller/train';
import Attribute from './AttributeSelector';
import { ChartTypeSelector } from './ChartTypeSelector';
import ChartView from './ChartView';
import { Section } from './Layout';
import { ResultPlot } from './ResultPlot';
import WeightSlider from './WeightSlider';
import RecommendedChartView from './RecommendedChartView';

export const Main = () => {
  console.log('main');
  return (
    <Flex w="full" minH="80vh" flexDir={'row'} justifyContent="space-between" px={4} gap={4}>
      <Flex flexDir={'column'} w={200} gap={2} h="fit-content">
        <Flex flexDir={'row'} justifyContent={'space-between'} align="center" gap={2}>
          <Button
            boxShadow={'sm'}
            colorScheme="blue"
            color="white"
            loadingText="Training..."
            size="xs"
            w="full"
            isLoading={isTrainingSignal.value}
            onClick={() => {
              isTrainingSignal.value = true;
              trainGleaner();
            }}
          >
            {'Train'}
          </Button>
          <Button
            boxShadow={'sm'}
            colorScheme="orange"
            color="white"
            loadingText="Gleaning..."
            size="xs"
            w="full"
            isLoading={isInferingSignal.value}
            isDisabled={!isTrainedSignal.value}
            onClick={() => {
              isInferingSignal.value = true;
              inferDashboard();
              recommendChart();
            }}
          >
            {'Glean'}
          </Button>
        </Flex>
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
          <WeightSlider title="diversity" />
          <WeightSlider title="parsimony" />
        </Section>
        <Section title="Configuration" gap={1.5} w={200}>
          <Flex flexDir={'row'} justifyContent={'space-between'} align="center">
            <Text fontSize={'xs'}># of Charts</Text>
            <Input
              size={'xs'}
              width={12}
              variant={'outline'}
              defaultValue={configSignal.peek().nChart}
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
      {dashboardSignal.value.length ? (
        <SimpleGrid w="full" h="fit-content" spacing={4} minChildWidth={350}>
          {dashboardSignal.value.map((chart, i) => (
            <ChartView chart={chart} key={`chart-${i}`} width={300} height={150} />
          ))}
        </SimpleGrid>
      ) : (
        <Box>No Dashboard</Box>
      )}
      <Flex flexDir={'column'} w={250} gap={2} h="fit-content">
        <Section title="Score Distributions" gap={1.5}>
          <ResultPlot width={250} height={20} target="score" />
          <ResultPlot width={250} height={20} target="specificity" />
          <ResultPlot width={250} height={20} target="interestingness" />
          <ResultPlot width={250} height={20} target="coverage" />
          <ResultPlot width={250} height={20} target="diversity" />
          <ResultPlot width={250} height={20} target="parsimony" />
        </Section>
        <Section title="Chart Recommendation" gap={1.5}>
          {recommendedChartsSignal.value.map((chart, i) => (
            <RecommendedChartView chart={chart} key={`chart-rec-${i}`} width={220} height={120} />
          ))}
        </Section>
      </Flex>
    </Flex>
  );
};
