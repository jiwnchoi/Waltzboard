import { Center, Divider, Flex, GridItem, Icon, Text } from "@chakra-ui/react";
import { useComputed } from "@preact/signals-react";
import { motion } from "framer-motion";
import {
  RiArrowDownSLine,
  RiArrowUpSLine,
  RiDeleteBinLine,
  RiPushpinFill,
  RiPushpinLine,
} from "react-icons/ri";
import { VegaLite } from "react-vega";
import { Handler } from "vega-tooltip";
import { isAppendPanelOpen } from "../controller/append";
import { removeChart, togglePinChart } from "../controller/dashboard";
import { inspectionIndexSignal } from "../controller/details";
import type { ChartView } from "../types/ChartView";
import t from "../../locales/default.json";

interface ChartViewProps {
  chart: ChartView;
  idx: number;
  width: number;
  height: number;
}

const ChartView = ({ idx, chart, width, height }: ChartViewProps) => {
  const showDetail = useComputed(() => {
    return inspectionIndexSignal.value === idx;
  });
  return (
    <GridItem>
      <Flex
        flexDir={"column"}
        w={"full"}
        h="fit-content"
        pt={2}
        borderTopRadius={4}
      >
        <Divider />
        <Flex
          flexDir={"row"}
          justifyContent={"space-between"}
          align="center"
          px={2}
        >
          <Icon
            mr={4}
            as={chart.isPinned ? RiPushpinFill : RiPushpinLine}
            boxSize={4}
            onClick={() => {
              togglePinChart(chart.key);
            }}
            _hover={{ cursor: "pointer" }}
          />
          <Center w="full" verticalAlign={"center"} minH="42px">
            <Text w="full" fontSize={"sm"} textAlign="center">
              {chart.titleToken.map((t, index) =>
                t.isPrefered ? (
                  <Text key={index} as="span" fontWeight={800} color="pink.400">
                    {`${t.text} `}
                  </Text>
                ) : (
                  <Text key={index} as="span" fontWeight={500}>
                    {`${t.text} `}
                  </Text>
                ),
              )}
            </Text>
          </Center>
          <Icon
            ml={4}
            as={RiDeleteBinLine}
            boxSize={4}
            onClick={() => {
              removeChart(chart);
            }}
            _hover={{ cursor: "pointer" }}
          />
        </Flex>
        <Center height="full" px={4} mb={2}>
          <VegaLite
            height={height}
            width={width}
            spec={chart.spec}
            // renderer="svg"
            actions={false}
            tooltip={new Handler().call}
          />
        </Center>

        <Flex
          as={motion.div}
          flexDir={"row"}
          justifyContent={"space-between"}
          color={showDetail.value ? "white" : "black"}
          bgColor={showDetail.value ? "blue.500" : "transparent"}
          align="center"
          borderTopRadius={4}
          p={2}
          pb={2}
          onClick={() => {
            const cur = inspectionIndexSignal.peek();
            isAppendPanelOpen.value = false;
            if (cur !== idx) {
              inspectionIndexSignal.value = idx;
              isAppendPanelOpen.value = false;
            } else {
              inspectionIndexSignal.value = -1;
            }
          }}
        >
          <Text
            fontSize={"sm"}
            textAlign="center"
            fontWeight={showDetail.value ? 800 : 500}
            mr="auto"
            px={2}
          >
            {t["text-show_details"]}
          </Text>

          {showDetail.value ? (
            <Icon as={RiArrowDownSLine} boxSize={4} />
          ) : (
            <Icon as={RiArrowUpSLine} boxSize={4} />
          )}
        </Flex>
      </Flex>
    </GridItem>
  );
};

export { ChartView };
