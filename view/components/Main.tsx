import {
  Box,
  Button,
  Center,
  Collapse,
  Drawer,
  DrawerBody,
  DrawerCloseButton,
  DrawerContent,
  DrawerHeader,
  Fade,
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
  Text,
  useDisclosure,
} from "@chakra-ui/react";
import { Fragment, useRef } from "react";
import { AiFillSetting } from "react-icons/ai";
import { RiAddCircleLine, RiLightbulbLine } from "react-icons/ri";
import t from "../../locales/default.json";
import {
  isAppendPanelOpen,
  isRecommendingSignal,
  recommendedChartViewSignal,
  toggleAppendPanel,
} from "../controller/append";
import { attributesSignal } from "../controller/attribute";
import { chartTypesSignal } from "../controller/chartType";
import { dashboardSignal } from "../controller/dashboard";
import {
  inspectionIndexSignal,
  isDetailExpanded,
  isVariantsLoadingSignal,
  variantChartsSignal,
} from "../controller/details";
import { inferDashboard, isLoading } from "../controller/infer";
import { configSignal, init, isInitializing } from "../controller/init";
import { scoreDashboard } from "../controller/score";
import { trainWaltzboard } from "../controller/train";
import { notDayTransformationsSignal } from "../controller/transformation";
import { ChartAppendView, RecommendChartView } from "./AppendChartView";
import AttributeSelector from "./AttributeSelector";
import { ChartTypeSelector } from "./ChartTypeSelector";
import { ChartView } from "./ChartView";
import {
  InsightsView,
  InspectionView,
  VariantChartView,
} from "./InspectionView";
import { Section } from "./Layout";
import { ScoreDistView } from "./ScoreDistView";
import SpaceDistView from "./SpaceDistView";
import { TransformationSelector } from "./TransformationSelector";
import WeightSlider from "./WeightSlider";

export const NUM_COL = 4;

const DesignDashboardButton = () => {
  return (
    <Button
      w={"full"}
      boxShadow={"sm"}
      borderRadius={"md"}
      colorScheme="blue"
      color="white"
      loadingText={t["btn-generating_dashboard"]}
      size="sm"
      p={4}
      isLoading={isLoading.value}
      onClick={() => {
        trainWaltzboard();
        inferDashboard();
        scoreDashboard();
      }}
    >
      <Box>{t["btn-design_dashboard"]}</Box>
    </Button>
  );
};
const HEIGHT = 1000;

export const Main = () => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const btnRef = useRef(null);

  return (
    <>
      <Flex
        w="container.2xl"
        flexDir={"row"}
        px={4}
        gap={4}
        overflow={"hidden"}
      >
        {/* Left Bar */}
        <Flex flexDir={"column"} minW={250} w={250} gap={2}>
          <Flex gap={2}>
            <DesignDashboardButton />
            <Settings />
          </Flex>
          <IntentPanel />
        </Flex>
        <Flex
          flexDir={"column"}
          w="full"
          p={2}
          bgColor="white"
          borderRadius="md"
          boxShadow="sm"
          maxW={"1622px"}
          maxH={HEIGHT}
          minH={HEIGHT}
        >
          <Flex flexDir={"row"} justifyContent={"end"} alignItems={"center"}>
            <Button
              colorScheme="blue"
              size={"sm"}
              leftIcon={<RiLightbulbLine />}
              ref={btnRef}
              onClick={onOpen}
            >
              <Text>{t["btn-open_reasoning_panel"]}</Text>
            </Button>
          </Flex>

          <Flex
            flexDir={"column"}
            w="full"
            gap={2}
            maxH={HEIGHT}
            overflowX={"hidden"}
            overflowY={"scroll"}
          >
            <Flex direction={"column"}>
              {isLoading.value && (
                <Center w="full" minH={HEIGHT - 100}>
                  <Spinner size="xl" />
                </Center>
              )}
              {!isLoading.value && dashboardSignal.value.length === 0 && (
                <Center w="full" minH={HEIGHT - 100} flexDir={"column"} gap={4}>
                  <Text fontSize={"xl"} fontWeight={600}>
                    {t["text-no_dashboard"]}
                  </Text>
                  <Text fontSize={"md"} fontWeight={400}>
                    {t["text-no_dashboard_prompt"]}
                  </Text>
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
                      <Fragment key={`chart-container-${i}`}>
                        <ChartView
                          idx={i}
                          chart={chart}
                          key={`chart-${i}`}
                          width={380}
                          height={200}
                        />

                        {i % NUM_COL == NUM_COL - 1 && (
                          <InspectionPanel i={i} key={`detail-${i}`} />
                        )}
                        {i == dashboardSignal.value.length - 1 && (
                          <>
                            <GridItem key={`append-${i}`}>
                              <Center
                                w="full"
                                h="full"
                                minH={280}
                                flexDir={"column"}
                                onClick={toggleAppendPanel}
                                bgColor={
                                  isAppendPanelOpen.value ? "blue.500" : "white"
                                }
                                borderTopRadius={"md"}
                                borderBottomRadius={
                                  isAppendPanelOpen.value ? "0px" : "md"
                                }
                                color={
                                  isAppendPanelOpen.value ? "white" : "gray.500"
                                }
                                fontWeight={800}
                                gap={2}
                              >
                                <Icon as={RiAddCircleLine} boxSize={"64px"} />
                                {t["text-add_chart"]}
                              </Center>
                            </GridItem>
                            <InspectionPanel
                              key={`detail-${i + 1}`}
                              i={
                                i +
                                (NUM_COL -
                                  (dashboardSignal.value.length % NUM_COL))
                              }
                            />
                          </>
                        )}
                      </Fragment>
                    );
                  })}
                </Grid>
              )}

              <AppendChartPanel open={isAppendPanelOpen.value} />
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
    ref.current.scrollIntoView({ behavior: "smooth" });
  }
  return (
    <Fade in={open} ref={ref} unmountOnExit>
      <Flex
        flexDir={"row"}
        minH={"335px"}
        mb={2}
        borderRadius={"md"}
        borderTopLeftRadius={0}
        border={"2px"}
        borderColor={"blue.500"}
        p={2}
        gap={4}
      >
        <ChartAppendView />

        <Flex
          minW={"200px"}
          maxW={"full"}
          w={"full"}
          flexDir={"column"}
          bgColor={"white"}
          borderRadius="md"
          p={2}
        >
          <Text fontSize={"md"} fontWeight={600} mb={2}>
            {t["sect-chart_recommendation"]}
          </Text>

          {isRecommendingSignal.value && (
            <Center w="full" minH={180}>
              <Spinner size="md" />
            </Center>
          )}
          <Flex
            w={"full"}
            overflowX={"scroll"}
            gap={3}
            px={4}
            hidden={isRecommendingSignal.value}
          >
            {recommendedChartViewSignal.value.map((chart, j) => (
              <RecommendChartView
                chart={chart}
                key={`recommend-${j}`}
                chartWidth={300}
                chartHeight={200}
              />
            ))}
          </Flex>
        </Flex>
      </Flex>
    </Fade>
  );
};

const InspectionPanel = ({ i }: { i: number }) => {
  return (
    <GridItem colSpan={NUM_COL}>
      <Collapse in={isDetailExpanded(i)} unmountOnExit>
        <Flex
          flexDir={"row"}
          border={"2px"}
          borderColor={"blue.500"}
          h={"340px"}
          mb={2}
          borderRadius={"md"}
          borderTopLeftRadius={
            inspectionIndexSignal.value % NUM_COL === 0 ? "0px" : "md"
          }
          borderTopRightRadius={
            inspectionIndexSignal.value % NUM_COL === NUM_COL - 1 ? "0px" : "md"
          }
          px={2}
          gap={4}
        >
          <InspectionView />
          <InsightsView />
          <Flex
            minW={"200px"}
            w={"full"}
            flexDir={"column"}
            borderRadius="md"
            p={2}
            my={2}
          >
            <Text fontSize={"md"} fontWeight={600}>
              {t["sect-alternative_view"]}
            </Text>

            {isVariantsLoadingSignal.value && (
              <Center w="full" minH={200}>
                <Spinner size="md" />
              </Center>
            )}
            {!isVariantsLoadingSignal.value &&
              variantChartsSignal.value.length == 0 && (
                <Center w="full" minH={200}>
                  <Text fontSize={"md"} fontWeight={600}>
                    {t["text-no_alternative"]}
                  </Text>
                </Center>
              )}

            <Flex
              w={"full"}
              overflowX={"scroll"}
              gap={3}
              px={4}
              hidden={isVariantsLoadingSignal.value}
            >
              {variantChartsSignal.value.map((variantChart, j) => (
                <VariantChartView
                  chart={variantChart}
                  key={`variant-${j}`}
                  chartWidth={300}
                  chartHeight={200}
                />
              ))}
            </Flex>
          </Flex>
        </Flex>
      </Collapse>
    </GridItem>
  );
};

const IntentPanel = () => {
  return (
    <Flex flexDir={"column"} w={"full"} px={0} gap={2} maxH={HEIGHT - 40}>
      <Section title={t["sect-weight-controller"]} gap={1.5} w="full">
        <WeightSlider title="specificity" />
        <WeightSlider title="interestingness" />
        <WeightSlider title="coverage" />
        <WeightSlider title="diversity" />
        <WeightSlider title="parsimony" />
      </Section>
      <Section
        title={t["sect-chart_types"]}
        gap={1.5}
        maxH={160}
        w="full"
        innerOverflowY={"scroll"}
      >
        {chartTypesSignal.value.map((chartType, i) => (
          <ChartTypeSelector chartType={chartType} key={`chartType-${i}`} />
        ))}
        <Box bgColor={"white"} minH={"36px"} />
      </Section>
      <Section
        title={t["sect-transformations"]}
        gap={1.5}
        maxH={160}
        w="full"
        innerOverflowY={"scroll"}
      >
        {notDayTransformationsSignal.value.map((transformation, i) => (
          <TransformationSelector
            transformation={transformation}
            key={`attribute-${i}`}
          />
        ))}
        <Box bgColor={"white"} minH={"36px"} />
      </Section>

      <Section
        title={t["sect-attributes"]}
        gap={1.5}
        minH={"36px"}
        maxH={"full"}
        h="full"
        pb={4}
        w="full"
        innerOverflowY={"scroll"}
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
    <DrawerContent borderRadius={"md"} maxW={270}>
      <DrawerCloseButton />
      <DrawerHeader />
      <DrawerBody borderRadius={20} p={"10px"}>
        <Flex flexDir={"column"} w={"250px"} px={0}>
          <Section title={t["sect-score_distribution_view"]} width={250}>
            <ScoreDistView width={250} height={250} />
          </Section>
          <Section
            title={t["sect-token_probability_list"]}
            width={250}
            h="full"
          >
            <SpaceDistView width={"250px"} gap={1} />
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
        <Button colorScheme={"blackAlpha"} variant={"solid"} size={"sm"}>
          <Icon as={AiFillSetting} />
        </Button>
      </PopoverTrigger>
      <PopoverContent
        bgColor={"white"}
        p={2}
        borderRadius={"md"}
        boxShadow={"md"}
      >
        <PopoverHeader fontWeight={700}>Configurations</PopoverHeader>
        <PopoverArrow bg="white" />
        <PopoverCloseButton />
        <PopoverBody>
          <Grid templateColumns={"1fr 2fr"} gap={2}>
            <GridItem>Dataset</GridItem>
            <GridItem>
              <Select
                size={"sm"}
                defaultValue={"Birdstrikes"}
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
            {Object.keys(configSignal.value)
              .filter((key) => key !== "dataset")
              .map((key) => (
                <Fragment key={key}>
                  <GridItem>{key}</GridItem>
                  <GridItem>
                    <Input
                      size={"sm"}
                      defaultValue={configSignal.value[key]!}
                      onChange={(e) => {
                        configSignal.value[key] = e.target.value;
                      }}
                    />
                  </GridItem>
                </Fragment>
              ))}
            <GridItem colSpan={2}>
              <Button
                w={"full"}
                boxShadow={"sm"}
                borderRadius={"md"}
                colorScheme="blue"
                color="white"
                size="sm"
                isLoading={isInitializing.value}
                onClick={() => {
                  init(configSignal.peek().userId! as string);
                }}
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
