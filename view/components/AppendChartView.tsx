import {
  Center,
  Flex,
  FlexProps,
  Select,
  Spacer,
  Text,
} from "@chakra-ui/react";
import { VegaLite } from "react-vega";
import { Handler } from "vega-tooltip";
import { inputChart, inputTuple } from "../controller/append";
import { attributesSignal } from "../controller/attribute";
import { chartTypesSignal } from "../controller/chartType";
import { appendChart } from "../controller/dashboard";
import { transformationsSignal } from "../controller/transformation";
import { ChartView } from "../types/ChartView";
import t from "../../locales/default.json";

interface ChartViewProps extends FlexProps {
  chart: ChartView;
  chartWidth: number;
  chartHeight: number;
}

export const ChartAppendPreview = () => {
  return (
    <Flex flexDir={"column"} w={270}>
      {inputChart.value && (
        <RecommendChartView
          chart={inputChart.value}
          chartWidth={300}
          chartHeight={200}
        />
      )}
      {!inputChart.value && (
        <Center w={"full"} h={130} textAlign={"center"} p={8}>
          {t["text-input_valid_chart"]}
        </Center>
      )}
      <Spacer />
    </Flex>
  );
};

export const ChartAppendView = () => {
  return (
    <Flex flexDir={"column"} p={2} bgColor={"white"} borderRadius={"md"}>
      <Text fontSize={"md"} fontWeight={600} mb={2}>
        {t["sect-chart_config"]}
      </Text>
      <Flex
        flexDir={"row"}
        justifyContent={"space-between"}
        align="top"
        gap={4}
      >
        <Flex flexDir={"column"} w={260}>
          <Flex
            flexDir={"row"}
            justifyContent={"space-between"}
            align="center"
            mb={2}
          >
            <Text
              fontSize={"sm"}
              minW={"60px"}
              align={"center"}
              fontWeight={700}
            >
              {t["text-chart_type"]}
            </Text>
            <Select
              bgColor={"white"}
              fontSize={"sm"}
              size="sm"
              ml="2"
              onChange={(e) => {
                const oldCurrentState = [...inputTuple.peek()];
                const v = ["None", "-"].includes(e.target.value)
                  ? null
                  : e.target.value;
                oldCurrentState[0] = v;
                inputTuple.value = oldCurrentState;
              }}
            >
              <option key={`appendNone`}>-</option>
              {chartTypesSignal.value.map((chartType) => (
                <option key={`append${chartType.mark}`} value={chartType.mark}>
                  {chartType.name}
                </option>
              ))}
            </Select>
          </Flex>
          <Flex
            flexDir={"row"}
            justifyContent={"space-between"}
            align="center"
            mb={2}
          >
            <Text
              fontSize={"sm"}
              minW={"60px"}
              align={"center"}
              fontWeight={700}
            >
              X
            </Text>
            <Select
              bgColor={"white"}
              fontSize={"sm"}
              size="sm"
              ml="2"
              onChange={(e) => {
                const oldCurrentState = [...inputTuple.peek()];
                const v = ["None", "-"].includes(e.target.value)
                  ? null
                  : e.target.value;
                oldCurrentState[1] = v;
                inputTuple.value = oldCurrentState;
              }}
            >
              <option key={`appendNone`}>{t["token-none"]}</option>
              {attributesSignal.value.map((a) => (
                <option key={`append${a.name}x`} value={a.name}>
                  {a.name}
                </option>
              ))}
            </Select>
            <Select
              bgColor={"white"}
              fontSize={"sm"}
              ml="2"
              size="sm"
              maxW={"80px"}
              onChange={(e) => {
                const oldCurrentState = [...inputTuple.peek()];
                const v = ["None", "-"].includes(e.target.value)
                  ? null
                  : e.target.value;
                oldCurrentState[4] = v;
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
            flexDir={"row"}
            justifyContent={"space-between"}
            align="center"
            mb={2}
          >
            <Text
              fontSize={"sm"}
              minW={"60px"}
              align={"center"}
              fontWeight={700}
            >
              Y
            </Text>
            <Select
              bgColor={"white"}
              fontSize={"sm"}
              size="sm"
              ml="2"
              onChange={(e) => {
                const oldCurrentState = [...inputTuple.peek()];
                const v = ["None", "-"].includes(e.target.value)
                  ? null
                  : e.target.value;
                oldCurrentState[2] = v;
                inputTuple.value = oldCurrentState;
              }}
            >
              <option key={`appendNone`}>{t["token-none"]}</option>
              {attributesSignal.value.map((a) => (
                <option key={`append${a.name}x`} value={a.name}>
                  {a.name}
                </option>
              ))}
            </Select>
            <Select
              bgColor={"white"}
              fontSize={"sm"}
              ml="2"
              size="sm"
              maxW={"80px"}
              onChange={(e) => {
                const oldCurrentState = [...inputTuple.peek()];
                const v = ["None", "-"].includes(e.target.value)
                  ? null
                  : e.target.value;
                oldCurrentState[5] = v;
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
            flexDir={"row"}
            justifyContent={"space-between"}
            align="center"
            mb={2}
          >
            <Text
              fontSize={"sm"}
              minW={"60px"}
              align={"center"}
              fontWeight={700}
            >
              Z
            </Text>
            <Select
              bgColor={"white"}
              fontSize={"sm"}
              size="sm"
              ml="2"
              onChange={(e) => {
                const oldCurrentState = [...inputTuple.peek()];
                const v = ["None", "-"].includes(e.target.value)
                  ? null
                  : e.target.value;
                oldCurrentState[3] = v;
                inputTuple.value = oldCurrentState;
              }}
            >
              <option key={`appendNone`}>{t["token-none"]}</option>
              {attributesSignal.value.map((a) => (
                <option key={`append${a.name}x`} value={a.name}>
                  {a.name}
                </option>
              ))}
            </Select>
            <Select
              bgColor={"white"}
              fontSize={"sm"}
              ml="2"
              size="sm"
              maxW={"80px"}
              onChange={(e) => {
                const oldCurrentState = [...inputTuple.peek()];
                const v = ["None", "-"].includes(e.target.value)
                  ? null
                  : e.target.value;
                oldCurrentState[6] = v;
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
      flexDir={"column"}
      {...props}
      bgColor={"white"}
      borderRadius="md"
      mb={2}
      p={2}
      pt={0}
      _hover={{
        cursor: "pointer",
        bgColor: "gray.100",
      }}
      onClick={() => appendChart(props.chart)}
    >
      <Center w="full" verticalAlign={"center"} minH="42px">
        <Text w="full" fontSize={"sm"} textAlign="center">
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
            ),
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
