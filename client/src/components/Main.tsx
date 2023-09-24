import {
  Box,
  Button,
  Center,
  Collapse,
  Divider,
  Flex,
  Grid,
  GridItem,
  Icon,
  Input,
  Popover,
  PopoverArrow,
  PopoverBody,
  PopoverCloseButton,
  PopoverContent,
  PopoverHeader,
  PopoverTrigger,
  Select,
  Spinner,
  Tab,
  TabList,
  TabPanel,
  TabPanels,
  Tabs,
  Text,
} from '@chakra-ui/react';
import {
  isAppendPanelOpen,
  isRecommendingSignal,
  recommendedChartViewSignal,
} from '../controller/append';
import { attributesSignal } from '../controller/attribute';
import { chartTypesSignal } from '../controller/chartType';
import { dashboardSignal } from '../controller/dashboard';
import {
  isDetailExpanded,
  isVariantsLoadingSignal,
  variantChartsSignal,
} from '../controller/details';
import { inferDashboard } from '../controller/infer';
import { configSignal, init } from '../controller/init';
import { scoreDashboard } from '../controller/score';
import { isTrainingSignal, trainWaltzboard } from '../controller/train';
import { notDayTransformationsSignal } from '../controller/transformation';
import { ChartAppendView, RecommendChartView } from './AppendChartView';
import AttributeSelector from './AttributeSelector';
import { ChartTypeSelector } from './ChartTypeSelector';
import { ChartView } from './ChartView';
import { MainSection, Section } from './Layout';
import {
  InsightsView,
  InspectionView,
  VariantChartView,
} from './InspectionView';
import { ScoreDistView } from './ScoreDistView';
import SpaceDistView from './SpaceDistView';
import { TransformationSelector } from './TransformationSelector';
import WeightSlider from './WeightSlider';
import { AiFillSetting } from 'react-icons/ai';
import { useRef } from 'react';

export const NUM_COL = 4;

const Settings = () => {
  const initialFocusRef = useRef(null);
  return (
    <Popover
      initialFocusRef={initialFocusRef}
      placement="right-start"
      closeOnBlur={true}
      closeOnEsc={true}
      returnFocusOnClose={true}
    >
      <PopoverTrigger>
        <Button colorScheme={'blackAlpha'} variant={'solid'} size={'sm'}>
          <Icon as={AiFillSetting} />
        </Button>
      </PopoverTrigger>
      <PopoverContent
        bgColor={'white'}
        p={2}
        borderRadius={'md'}
        boxShadow={'md'}
      >
        <PopoverHeader fontWeight={700}>Configurations</PopoverHeader>
        <PopoverArrow bg="white" />
        <PopoverCloseButton />
        <PopoverBody>
          <Grid templateColumns={'1fr 2fr'} gap={2}>
            <GridItem>Dataset</GridItem>
            <GridItem>
              <Select
                size={'sm'}
                defaultValue={'Movies'}
                w="full"
                onChange={(e) => {
                  configSignal.value.dataset = e.target.value;
                }}
              >
                <option>Birdstrikes</option>
                <option>Movies</option>
                <option>Student Performance</option>
              </Select>
            </GridItem>
            <GridItem># of Epochs</GridItem>
            <GridItem>
              <Input
                size={'sm'}
                defaultValue={configSignal.value.n_epoch}
                onChange={(e) => {
                  configSignal.value.n_epoch = parseInt(e.target.value);
                }}
              />
            </GridItem>
            <GridItem>Robustness</GridItem>
            <GridItem>
              <Input
                size={'sm'}
                defaultValue={configSignal.value.robustness}
                onChange={(e) => {
                  configSignal.value.robustness = parseInt(e.target.value);
                }}
              />
            </GridItem>
            <GridItem colSpan={2}>
              <Button
                w={'full'}
                boxShadow={'sm'}
                borderRadius={'md'}
                colorScheme="blue"
                color="white"
                size="sm"
                onClick={init}
              >
                <Box>Set Configs</Box>
              </Button>
            </GridItem>
          </Grid>
        </PopoverBody>
      </PopoverContent>
    </Popover>
  );
};
export const Main = () => {
  return (
    <Flex w="full" flexDir={'row'} px={4} gap={4}>
      {/* Left Bar */}
      <Flex flexDir={'column'} minW={250} w={250}>
        <Flex gap={2}>
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
              trainWaltzboard();
              inferDashboard();
              scoreDashboard();
            }}
          >
            <Box>Design Dashboard</Box>
          </Button>
          <Settings />
        </Flex>
        <Tabs variant={'line'} colorScheme="blue" isFitted>
          <TabList p={0}>
            <Tab fontWeight={500}>Intent</Tab>
            <Tab
              fontWeight={500}
              isDisabled={dashboardSignal.value.length == 0}
            >
              Result
            </Tab>
          </TabList>
          <TabPanels>
            <IntentPanel />
            <ResultPanel />
          </TabPanels>
        </Tabs>
      </Flex>
      <MainSection
        title={`Best Dashboard Design (${dashboardSignal.value.length} Charts)`}
        gap={2}
        bgColor={'white'}
        innerOverflowY="scroll"
        innerOverflowX="hidden"
        maxH={'894px'}
        maxW={'1610px'}
      >
        <Flex direction={'column'}>
          <AppendChartPanel />
          {dashboardSignal.value.length === 0 && (
            <Center w="full" minH={180}>
              <Spinner size="xl" />
            </Center>
          )}
          {dashboardSignal.value.length !== 0 && (
            <Grid
              templateColumns={{
                xl: `repeat(${NUM_COL}, minmax(280px, 1fr))`,
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

                    {(i == dashboardSignal.value.length - 1 ||
                      i % NUM_COL == NUM_COL - 1) && <InspectionPanel i={i} />}
                  </>
                );
              })}
            </Grid>
          )}
        </Flex>
      </MainSection>
    </Flex>
  );
};

const AppendChartPanel = () => (
  <Collapse in={isAppendPanelOpen.value} animateOpacity unmountOnExit>
    <Flex
      flexDir={'row'}
      bgColor={'gray.100'}
      minH={'260px'}
      mb={2}
      borderRadius={'md'}
      p={2}
      gap={4}
    >
      <ChartAppendView />
      <Flex
        minW={'200px'}
        maxW={'full'}
        w={'full'}
        flexDir={'column'}
        bgColor={'white'}
        borderRadius="md"
        p={2}
      >
        <Text fontSize={'md'} fontWeight={600} mb={2}>
          Chart Recommendation
        </Text>

        {isRecommendingSignal.value && (
          <Center w="full" minH={180}>
            <Spinner size="md" />
          </Center>
        )}
        <Flex
          w={'full'}
          overflowX={'scroll'}
          gap={3}
          px={4}
          hidden={isRecommendingSignal.value}
        >
          {recommendedChartViewSignal.value.map((chart, j) => (
            <RecommendChartView
              chart={chart}
              key={`recommend-${j}`}
              chartWidth={250}
              chartHeight={125}
            />
          ))}
        </Flex>
      </Flex>
    </Flex>
  </Collapse>
);

const InspectionPanel = ({ i }: { i: number }) => (
  <GridItem colSpan={NUM_COL}>
    <Collapse in={isDetailExpanded(i)} animateOpacity unmountOnExit>
      <Flex
        flexDir={'row'}
        bgColor={'gray.100'}
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
            {variantChartsSignal.value.map((variantChart, j) => (
              <VariantChartView
                chart={variantChart}
                key={`variant-${j}`}
                chartHeight={125}
                chartWidth={250}
              />
            ))}
          </Flex>
        </Flex>
      </Flex>
    </Collapse>
  </GridItem>
);

const IntentPanel = () => (
  <TabPanel
    display={'flex'}
    flexDir={'column'}
    w={'full'}
    px={0}
    gap={2}
    h={930}
  >
    <Section title="Score Weight" gap={1.5} w="full">
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
        <ChartTypeSelector chartType={chartType} key={`chartType-${i}`} />
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
      maxH={220}
      h="full"
      pb={4}
      w="full"
      innerOverflowY={'scroll'}
    >
      {attributesSignal.value.map((attribute, i) => (
        <AttributeSelector attribute={attribute} key={`attribute-${i}`} />
      ))}
      <Box bgColor={'white'} minH={41} />
    </Section>
  </TabPanel>
);

const ResultPanel = () => (
  <TabPanel
    display={'flex'}
    flexDir={'column'}
    w={'full'}
    px={0}
    gap={2}
    h={930}
  >
    <Section title="Score Distributions" width={250}>
      <ScoreDistView width={250} height={250} />
    </Section>
    <Section title="Space Distributions" width={250} h="full">
      <SpaceDistView width={'full'} gap={4} />
    </Section>
  </TabPanel>
);
