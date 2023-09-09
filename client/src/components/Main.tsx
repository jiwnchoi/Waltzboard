import {
  Box,
  Button,
  Center,
  Flex,
  SimpleGrid,
  Spinner,
} from '@chakra-ui/react';
import { attributesSignal } from '../controller/attribute';
import { chartTypesSignal } from '../controller/chartType';
import { dashboardSignal } from '../controller/dashboard';
import { inferDashboard } from '../controller/infer';
import { recommendedChartsSignal } from '../controller/recommend';
import { scoreDashboard } from '../controller/score';
import { isTrainingSignal, trainGleaner } from '../controller/train';
import { notDayTransformationsSignal } from '../controller/transformation';
import AttributeSelector from './AttributeSelector';
import { ChartTypeSelector } from './ChartTypeSelector';
import ChartView from './ChartView';
import { HSection, Section } from './Layout';
import RecommendedChartView from './RecommendedChartView';
import { ScoreDistView } from './ScoreDistView';
import SpaceDistView from './SpaceDistView';
import { TransformationSelector } from './TransformationSelector';
import WeightSlider from './WeightSlider';

export const Main = () => {
  return (
    <Flex w="95vw" minH="80vh" flexDir={'row'} px={4} gap={4}>
      <Flex flexDir={'column'} w={200} gap={2} h="fit-content">
        <Button
          boxShadow={'sm'}
          colorScheme="blue"
          color="white"
          loadingText="Searching Dashboard..."
          size="xs"
          w="full"
          isLoading={isTrainingSignal.value}
          onClick={() => {
            trainGleaner();
            inferDashboard();
            scoreDashboard();
          }}
        >
          {'Search Dashboard'}
        </Button>
        <Section title="Score Weight" gap={1.5} w="full">
          {/* <Select
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
          </Select> */}

          <WeightSlider title="specificity" />
          <WeightSlider title="interestingness" />
          <WeightSlider title="coverage" />
          <WeightSlider title="diversity" />
          <WeightSlider title="parsimony" />
        </Section>
        <Section title="Chart Types" gap={1.5} maxH={240} w="full">
          {chartTypesSignal.value.map((chartType, i) => (
            <ChartTypeSelector chartType={chartType} key={`chartType-${i}`} />
          ))}
          <Box minH={10}></Box>
        </Section>
        <Section title="Transformations" gap={1.5} maxH={120} w="full">
          {notDayTransformationsSignal.value.map((transformation, i) => (
            <TransformationSelector
              transformation={transformation}
              key={`attribute-${i}`}
            />
          ))}
          <Box minH={8}></Box>
        </Section>

        <Section title="Attributes" gap={1.5} maxH={240} w="full">
          {attributesSignal.value.map((attribute, i) => (
            <AttributeSelector attribute={attribute} key={`attribute-${i}`} />
          ))}
          <Box minH={8}></Box>
        </Section>
      </Flex>
      <Flex flexDir={'column'} minW={200} h="fit-content" gap={2}>
        <Section title="Score Distributions" width={250}>
          <ScoreDistView width={250} height={250} />
        </Section>
        <Section title="Space Distributions" width={250}>
          <SpaceDistView width={'full'} />
        </Section>
      </Flex>
      <Flex flexDir={'column'} flexGrow={1} minW={0} h="fit-content" gap={2}>
        <HSection title="Recommendation" gap={1.5} w="full">
          {recommendedChartsSignal.value.length ? (
            recommendedChartsSignal.value.map((chart, i) => (
              <RecommendedChartView
                chart={chart}
                key={`chart-rec-${i}`}
                overflowX={'scroll'}
                minW={320}
                p={2}
                chartWidth={300}
                chartHeight={150}
              />
            ))
          ) : (
            <Center w="full" minH={180}>
              <Spinner size="xl" />
            </Center>
          )}
        </HSection>
        <HSection
          title="Dashboard"
          gap={2}
          bgColor={'white'}
          flexGrow={1}
          minW={0}
          h="fit-content"
          showScroll={false}
        >
          {dashboardSignal.value.length ? (
            <SimpleGrid
              w="full"
              h="fit-content"
              spacing={2}
              minChildWidth={300}
            >
              {dashboardSignal.value.map((chart, i) => (
                <ChartView
                  chart={chart}
                  key={`chart-${i}`}
                  width={300}
                  height={150}
                />
              ))}
            </SimpleGrid>
          ) : (
            <Center w="full" minH={180}>
              <Spinner size="xl" />
            </Center>
          )}
        </HSection>
      </Flex>
    </Flex>
  );
};
