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
import AttributeSelector from './AttributeSelector';
import { ChartTypeSelector } from './ChartTypeSelector';
import ChartView from './ChartView';
import { HSection, Section } from './Layout';
import { ResultPlot } from './ResultPlot';
import WeightSlider from './WeightSlider';
import RecommendedChartView from './RecommendedChartView';
import { ScoreDistView } from './ScoreDistView';
import { aggregationsSignal } from '../controller/aggregation';
import { AggregationSelector } from './AggregationSelector';
import SpaceDistView from './SpaceDistView';

export const Main = () => {
  console.log('main');
  return (
    <Flex w="full" minH="80vh" flexDir={'row'} justifyContent="space-between" px={4} gap={4}>
      <Flex flexDir={'column'} w={150} gap={2} h="fit-content">
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
        <Section title="Chart Types" gap={1.5} maxH={240}>
          {chartTypesSignal.value.map((chartType, i) => (
            <ChartTypeSelector chartType={chartType} key={`chartType-${i}`} />
          ))}
          <Box minH={10}></Box>
        </Section>
        <Section title="Aggregations" gap={1.5} maxH={120}>
          {aggregationsSignal.value.map((aggregation, i) => (
            <AggregationSelector aggregation={aggregation} key={`attribute-${i}`} />
          ))}
          <Box minH={8}></Box>
        </Section>

        <Section title="Attributes" gap={1.5} maxH={240}>
          {attributesSignal.value.map((attribute, i) => (
            <AttributeSelector attribute={attribute} key={`attribute-${i}`} />
          ))}
          <Box minH={8}></Box>
        </Section>
      </Flex>
      <Flex flexDir={'column'} w={300} h="fit-content" gap={2}>
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
        <Section title="Score Distributions">
          <ScoreDistView width={300} height={300} />
        </Section>
        <Section title="Space Distributions">
          <SpaceDistView width={300} svgWidth={300} svgHeight={300} />
        </Section>
      </Flex>
      <Flex flexDir={'column'} w={'full'} h="fit-content" gap={2}>
        <HSection title="Recommendation" gap={1.5}>
          {recommendedChartsSignal.value.map((chart, i) => (
            <RecommendedChartView chart={chart} key={`chart-rec-${i}`} width={250} height={100} />
          ))}
        </HSection>
        <HSection
          title="Dashboard"
          gap={2}
          bgColor={'white'}
          w="full"
          h="fit-content"
          maxH={'100vh'}
        >
          {dashboardSignal.value.length ? (
            <SimpleGrid w="full" h="fit-content" spacing={2} minChildWidth={300}>
              {dashboardSignal.value.map((chart, i) => (
                <ChartView chart={chart} key={`chart-${i}`} width={300} height={150} />
              ))}
            </SimpleGrid>
          ) : (
            <Box>No Dashboard</Box>
          )}
        </HSection>
      </Flex>
    </Flex>
  );
};
