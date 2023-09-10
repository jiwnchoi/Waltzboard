import {
  Box,
  Button,
  Center,
  Flex,
  Select,
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
import { ChartAppendView, ChartView } from './ChartView';
import { HSection, Section } from './Layout';
import RecommendedChartView from './RecommendedChartView';
import { ScoreDistView } from './ScoreDistView';
import SpaceDistView from './SpaceDistView';
import { TransformationSelector } from './TransformationSelector';
import WeightSlider from './WeightSlider';
import { init } from '../controller/init';

export const Main = () => {
  return (
    <Flex w="full" flexDir={'row'} px={4} gap={4}>
      <Flex flexDir={'column'} gap={4}>
        <Flex flexDir={'row'} justifyContent={'space-between'} w="full" gap={2}>
          <Flex flexGrow={1}>
            <Select
              size={'sm'}
              defaultValue={'Movies'}
              w="full"
              bgColor={'white'}
              boxShadow={'sm'}
              borderRadius={'md'}
              borderWidth={0}
              onChange={(e) => {
                console.log(e.target.value);
                init(e.target.value);
              }}
            >
              <option>Birdstrikes</option>
              <option>Movies</option>
              <option>Student Performance</option>
            </Select>
          </Flex>
          <Flex>
            <Button
              w={'full'}
              boxShadow={'sm'}
              borderRadius={'md'}
              colorScheme="blue"
              color="white"
              loadingText="Designing..."
              size="sm"
              p={4}
              isLoading={isTrainingSignal.value}
              onClick={() => {
                trainGleaner();
                inferDashboard();
                scoreDashboard();
              }}
            >
              <Box>Design Dashboard</Box>
            </Button>
          </Flex>
        </Flex>

        <Flex flexDir={'row'} gap={4} h="fit-content">
          <Flex flexDir={'column'} w={200} gap={2} h="fit-content">
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
            <Section
              title="Chart Types"
              gap={1.5}
              maxH={160}
              w="full"
              innerOverflowY={'scroll'}
            >
              {chartTypesSignal.value.map((chartType, i) => (
                <ChartTypeSelector
                  chartType={chartType}
                  key={`chartType-${i}`}
                />
              ))}
              <Box bgColor={'white'} minH={41} />
            </Section>
            <Section
              title="Transformations"
              gap={1.5}
              maxH={160}
              w="full"
              innerOverflowY={'scroll'}
            >
              {notDayTransformationsSignal.value.map((transformation, i) => (
                <TransformationSelector
                  transformation={transformation}
                  key={`attribute-${i}`}
                />
              ))}
              <Box bgColor={'white'} minH={41} />
            </Section>

            <Section
              title="Attributes"
              gap={1.5}
              minH={'36px'}
              maxH={'calc(100vh - 700px)'}
              pb={4}
              w="full"
              innerOverflowY={'scroll'}
            >
              {attributesSignal.value.map((attribute, i) => (
                <AttributeSelector
                  attribute={attribute}
                  key={`attribute-${i}`}
                />
              ))}
              <Box bgColor={'white'} minH={41} />
            </Section>
          </Flex>
          <Flex flexDir={'column'} minW={200} h="fit-content" gap={2}>
            <Section title="Score Distributions" width={250}>
              <ScoreDistView width={250} height={250} />
            </Section>
            <Section title="Space Distributions" width={250}>
              <SpaceDistView
                width={'full'}
                gap={4}
                minH={'calc(100vh - 378px)'}
              />
            </Section>
          </Flex>
        </Flex>
      </Flex>
      <Flex flexDir={'column'} flexGrow={1} minW={0} h="full" gap={2}>
        <HSection
          title="Recommendation"
          gap={1.5}
          w="full"
          innerOverflowX="scroll"
        >
          {recommendedChartsSignal.value.length ? (
            recommendedChartsSignal.value.map((chart, i) => (
              <RecommendedChartView
                chart={chart}
                key={`chart-rec-${i}`}
                minW={300}
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
          h={'calc(100vh - 319px)'}
          innerOverflowY="auto"
        >
          {dashboardSignal.value.length ? (
            <SimpleGrid
              w="full"
              maxH={'calc(100vh - 362px)'}
              spacing={2}
              minChildWidth={300}
            >
              <ChartAppendView />
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
