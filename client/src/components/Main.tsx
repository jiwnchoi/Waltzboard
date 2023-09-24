import {
  Box,
  Button,
  Center,
  Collapse,
  Divider,
  Drawer,
  DrawerBody,
  DrawerCloseButton,
  DrawerContent,
  DrawerHeader,
  Flex,
  Grid,
  GridItem,
  Heading,
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
  Text,
  useDisclosure,
} from '@chakra-ui/react';
import { useRef } from 'react';
import { AiFillSetting } from 'react-icons/ai';
import { RiAddBoxLine, RiAddCircleLine, RiLightbulbLine } from 'react-icons/ri';
import {
  isAppendPanelOpen,
  isRecommendingSignal,
  recommendedChartViewSignal,
  toggleAppendPanel,
} from '../controller/append';
import { attributesSignal } from '../controller/attribute';
import { chartTypesSignal } from '../controller/chartType';
import { dashboardSignal } from '../controller/dashboard';
import {
  inspectionIndexSignal,
  isDetailExpanded,
  isVariantsLoadingSignal,
  variantChartsSignal,
} from '../controller/details';
import { inferDashboard, isLoading } from '../controller/infer';
import { configSignal, init } from '../controller/init';
import { scoreDashboard } from '../controller/score';
import { isTrainingSignal, trainWaltzboard } from '../controller/train';
import { notDayTransformationsSignal } from '../controller/transformation';
import { ChartAppendView, RecommendChartView } from './AppendChartView';
import AttributeSelector from './AttributeSelector';
import { ChartTypeSelector } from './ChartTypeSelector';
import { ChartView } from './ChartView';
import {
  InsightsView,
  InspectionView,
  VariantChartView,
} from './InspectionView';
import { Section } from './Layout';
import { ScoreDistView } from './ScoreDistView';
import SpaceDistView from './SpaceDistView';
import { TransformationSelector } from './TransformationSelector';
import WeightSlider from './WeightSlider';
import { Configs } from '../types/API';

export const NUM_COL = 4;

const DesignDashboardButton = () => (
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
);

export const Main = () => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const btnRef = useRef(null);

  return (
    <>
      <Flex
        w="container.2xl"
        flexDir={'row'}
        px={4}
        gap={4}
        overflow={'hidden'}
      >
        {/* Left Bar */}
        <Flex flexDir={'column'} minW={250} w={250} gap={2}>
          <Flex gap={2}>
            <DesignDashboardButton />
            <Settings />
          </Flex>
          <IntentPanel />
        </Flex>
        <Flex
          flexDir={'column'}
          w="full"
          p={2}
          bgColor="white"
          borderRadius="md"
          boxShadow="sm"
          maxW={'1622px'}
          maxH={'890px'}
          minH={'890px'}
        >
          <Flex
            flexDir={'row'}
            justifyContent={'space-between'}
            alignItems={'center'}
          >
            <Button
              colorScheme="blue"
              borderBottomRadius={isAppendPanelOpen.value ? '0px' : 'md'}
              size={'sm'}
              leftIcon={<RiAddCircleLine />}
              onClick={toggleAppendPanel}
            >
              <Text>Add a New Chart</Text>
            </Button>
            <Button
              colorScheme="orange"
              size={'sm'}
              leftIcon={<RiLightbulbLine />}
              ref={btnRef}
              onClick={onOpen}
            >
              <Text>Open Reasoning Panel</Text>
            </Button>
          </Flex>
          <Flex
            flexDir={'column'}
            w="full"
            gap={2}
            maxH={'890px'}
            overflowX={'hidden'}
            overflowY={'scroll'}
          >
            <Flex direction={'column'}>
              <AppendChartPanel open={isAppendPanelOpen.value} />
              {isLoading.value && (
                <Center w="full" minH={800}>
                  <Spinner size="xl" />
                </Center>
              )}
              {!isLoading.value && dashboardSignal.value.length === 0 && (
                <Center w="full" minH={800} flexDir={'column'} gap={4}>
                  <Text fontSize={'xl'} fontWeight={600}>
                    Dashboard is Empty!
                  </Text>
                  <Text fontSize={'md'} fontWeight={400}>
                    Specify your intent with the left panel and
                  </Text>
                  <Flex flexDir={'row'} gap={4} align={'center'}>
                    <Text fontSize={'md'} fontWeight={400}>
                      click
                    </Text>
                    <DesignDashboardButton />
                  </Flex>
                </Center>
              )}
              {!isLoading.value && dashboardSignal.value.length !== 0 && (
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

                        {i % NUM_COL == NUM_COL - 1 && (
                          <InspectionPanel i={i} />
                        )}
                        {i == dashboardSignal.value.length - 1 && (
                          <InspectionPanel
                            i={
                              i +
                              (NUM_COL -
                                (dashboardSignal.value.length % NUM_COL))
                            }
                          />
                        )}
                      </>
                    );
                  })}
                </Grid>
              )}
            </Flex>
          </Flex>
        </Flex>
      </Flex>
      <ResultPanel isOpen={isOpen} onClose={onClose} btnRef={btnRef} />
    </>
  );
};

const AppendChartPanel = ({ open }: { open: boolean }) => {
  const ref = useRef<HTMLDivElement>(null);
  if (ref.current) {
    ref.current.scrollIntoView({ behavior: 'smooth' });
  }
  return (
    <Collapse in={open} animateOpacity unmountOnExit ref={ref}>
      <Flex
        flexDir={'row'}
        minH={'260px'}
        mb={2}
        borderRadius={'md'}
        borderTopLeftRadius={0}
        border={'2px'}
        borderColor={'blue.500'}
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
            Recommended Charts
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
};

const InspectionPanel = ({ i }: { i: number }) => (
  <GridItem colSpan={NUM_COL}>
    <Collapse in={isDetailExpanded(i)} animateOpacity unmountOnExit>
      <Flex
        flexDir={'row'}
        border={'2px'}
        borderColor={'blue.500'}
        h={'280px'}
        mb={2}
        borderRadius={'md'}
        borderTopLeftRadius={
          inspectionIndexSignal.value % NUM_COL === 0 ? '0px' : 'md'
        }
        borderTopRightRadius={
          inspectionIndexSignal.value % NUM_COL === NUM_COL - 1 ? '0px' : 'md'
        }
        px={2}
        gap={4}
      >
        <InspectionView />
        <InsightsView />
        <Flex
          minW={'200px'}
          w={'full'}
          flexDir={'column'}
          borderRadius="md"
          p={2}
          my={2}
        >
          <Text fontSize={'md'} fontWeight={600}>
            Alternatives View
          </Text>

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

const IntentPanel = () => {
  return (
    <Flex flexDir={'column'} w={'full'} px={0} gap={2} maxH={'850px'}>
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
        <Box bgColor={'white'} minH={'36px'} />
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
        <Box bgColor={'white'} minH={'36px'} />
      </Section>

      <Section
        title="Attributes"
        gap={1.5}
        minH={'36px'}
        maxH={'full'}
        h="full"
        pb={4}
        w="full"
        innerOverflowY={'scroll'}
      >
        {attributesSignal.value.map((attribute, i) => (
          <AttributeSelector attribute={attribute} key={`attribute-${i}`} />
        ))}
      </Section>
    </Flex>
  );
};

interface DisclosureProps {
  isOpen: boolean;
  onClose: () => void;
  btnRef: any;
}
const ResultPanel = ({ isOpen, onClose, btnRef }: DisclosureProps) => (
  <Drawer
    isOpen={isOpen}
    placement="right"
    onClose={onClose}
    finalFocusRef={btnRef}
  >
    {/* <DrawerOverlay /> */}
    <DrawerContent borderRadius={'md'} minH={1080}>
      <DrawerCloseButton />
      <DrawerHeader>Reasoning Panel</DrawerHeader>
      <DrawerBody borderRadius={20}>
        <Flex flexDir={'column'} w={'250px'} px={0}>
          <Section title="Score Distributions View" width={250}>
            <ScoreDistView width={250} height={250} />
          </Section>
          <Section title="Token Probability List" width={250} h="full">
            <SpaceDistView width={'250px'} gap={4} />
          </Section>
        </Flex>
      </DrawerBody>
    </DrawerContent>
  </Drawer>
);

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
            {Object.keys(configSignal.value).map((key) => (
              <>
                {key !== 'dataset' && (
                  <>
                    <GridItem>{key}</GridItem>
                    <GridItem>
                      <Input
                        size={'sm'}
                        defaultValue={configSignal.value[key as keyof Configs]}
                        onChange={(e) => {
                          configSignal.value[key as keyof Configs] =
                            e.target.value;
                        }}
                      />
                    </GridItem>
                  </>
                )}
              </>
            ))}
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
