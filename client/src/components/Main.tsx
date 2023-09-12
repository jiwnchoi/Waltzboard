import {
  Box,
  Button,
  Center,
  Collapse,
  Divider,
  Flex,
  Grid,
  GridItem,
  Select,
  Spinner,
  Text,
} from '@chakra-ui/react';
import { attributesSignal } from '../controller/attribute';
import { chartTypesSignal } from '../controller/chartType';
import { dashboardSignal } from '../controller/dashboard';
import { inferDashboard } from '../controller/infer';
import { init } from '../controller/init';
import {
  isDetailExpanded,
  isVariantsLoadingSignal,
  variantChartsSignal,
} from '../controller/details';
import { scoreDashboard } from '../controller/score';
import { isTrainingSignal, trainGleaner } from '../controller/train';
import { notDayTransformationsSignal } from '../controller/transformation';
import AttributeSelector from './AttributeSelector';
import { ChartTypeSelector } from './ChartTypeSelector';
import { ChartAppendView, ChartView } from './ChartView';
import { HSection, Section } from './Layout';
import {
  InsightsView,
  InspectionView,
  VariantChartView,
} from './ReasoningView';
import { ScoreDistView } from './ScoreDistView';
import SpaceDistView from './SpaceDistView';
import { TransformationSelector } from './TransformationSelector';
import WeightSlider from './WeightSlider';

export const NUM_DASHBOARD_COLUMN = 3;

export const Main = () => {
  console.log('main');
  return (
    <Flex w="full" flexDir={'row'} px={4} gap={4}>
      <Flex flexDir={'column'} gap={4}>
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
        </Flex>
      </Flex>
      <Flex flexDir={'column'} flexGrow={1} minW={0} h="full" gap={2}>
        <HSection
          title={`Best Dashboard Design (${dashboardSignal.value.length} Charts)`}
          gap={2}
          bgColor={'white'}
          flexGrow={1}
          minW={0}
          //   maxH={'calc(100vh - 66px)'}
          innerOverflowY="scroll"
          innerOverflowX="hidden"
        >
          {dashboardSignal.value.length ? (
            <Grid
              templateColumns={{
                xl: `repeat(${NUM_DASHBOARD_COLUMN}, minmax(280px, 1fr))`,
              }}
              w="full"
            >
              {dashboardSignal.value.map((chart, i) => {
                return (
                  <>
                    <ChartView
                      idx={i}
                      chart={chart}
                      key={`chart-${i}`}
                      width={280}
                      height={140}
                    />

                    {i % NUM_DASHBOARD_COLUMN == NUM_DASHBOARD_COLUMN - 1 && (
                      <GridItem colSpan={NUM_DASHBOARD_COLUMN}>
                        <Collapse
                          in={isDetailExpanded(i)}
                          animateOpacity
                          unmountOnExit
                        >
                          <Flex
                            flexDir={'row'}
                            bgColor={'gray.50'}
                            h={'280px'}
                            mb={2}
                            borderRadius={'md'}
                            px={2}
                            gap={4}
                          >
                            <InspectionView />
                            <InsightsView />
                            <Flex
                              minW={'200px'}
                              w={'full'}
                              flexDir={'column'}
                              bgColor={'white'}
                              borderRadius="md"
                              p={2}
                              my={2}
                            >
                              <Text fontSize={'md'} fontWeight={600}>
                                Chart Variants
                              </Text>
                              <Divider my={1} />
                              {isVariantsLoadingSignal.value && (
                                <Center w="full" minH={180}>
                                  <Spinner size="md" />
                                </Center>
                              )}
                              {variantChartsSignal.value.length == 0 && (
                                <Center w="full" minH={180}>
                                  <Text fontSize={'md'} fontWeight={600}>
                                    No variants
                                  </Text>
                                </Center>
                              )}

                              <Flex
                                w={'full'}
                                overflowX={'scroll'}
                                gap={3}
                                px={4}
                                hidden={isVariantsLoadingSignal.value}
                              >
                                {variantChartsSignal.value.map(
                                  (variantChart, j) => (
                                    <VariantChartView
                                      chart={variantChart}
                                      key={`variant-${j}`}
                                      chartHeight={125}
                                      chartWidth={250}
                                    />
                                  )
                                )}
                              </Flex>
                            </Flex>
                          </Flex>
                        </Collapse>
                      </GridItem>
                    )}
                    {i == dashboardSignal.value.length - 1 && (
                      <GridItem>
                        <ChartAppendView />
                      </GridItem>
                    )}
                  </>
                );
              })}
            </Grid>
          ) : (
            <Center w="full" minH={180}>
              <Spinner size="xl" />
            </Center>
          )}
        </HSection>
      </Flex>
      <Flex flexDir={'column'} minW={200} h="fit-content" gap={2}>
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
        <Section title="Score Distributions" width={250}>
          <ScoreDistView width={250} height={250} />
        </Section>
        <Section title="Space Distributions" width={250}>
          <SpaceDistView width={'full'} gap={4} minH={'calc(100vh - 378px)'} />
        </Section>
      </Flex>
    </Flex>
  );
};
