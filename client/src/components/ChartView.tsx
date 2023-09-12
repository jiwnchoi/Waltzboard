import {
  Badge,
  Box,
  Button,
  Center,
  Divider,
  Fade,
  Flex,
  GridItem,
  Icon,
  Select,
  Spacer,
  Text,
  useDisclosure,
} from '@chakra-ui/react';
import {
  batch,
  useComputed,
  useSignal,
  useSignalEffect,
} from '@preact/signals-react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { AiOutlinePlusCircle } from 'react-icons/ai';
import {
  RiArrowDownSLine,
  RiArrowUpSLine,
  RiDeleteBinLine,
  RiPushpinFill,
  RiPushpinLine,
} from 'react-icons/ri';
import { VegaLite } from 'react-vega';
import { Handler } from 'vega-tooltip';
import { URI } from '../../config';
import { attributesSignal } from '../controller/attribute';
import { chartTypesSignal } from '../controller/chartType';
import { removeChart, togglePinChart } from '../controller/dashboard';
import {
  inspectionIndexSignal,
  inspectionSignal,
  variantChartsSignal,
} from '../controller/details';
import { transformationsSignal } from '../controller/transformation';
import type { ChartView } from '../types/ChartView';

interface ChartViewProps {
  chart: ChartView;
  idx: number;
  width: number;
  height: number;
}

const ChartAppendView = () => {
  const { isOpen, onToggle } = useDisclosure();
  const isValid = useSignal(false);
  const currentState = useSignal<(string | null)[]>([
    null,
    null,
    null,
    null,
    null,
    null,
    null,
  ]);
  useSignalEffect(() => {
    const getIsValid = async () => {
      const res = await axios.get(
        `${URI}/is_valid?token=${JSON.stringify(currentState.value)}`
      );
      isValid.value = res.data.isValid;
      console.log(res.data.isValid);
    };
    getIsValid();
  });

  return (
    <Box w="full" h="246px">
      {!isOpen && (
        <Fade in={!isOpen}>
          <Center h="246px">
            <Icon
              as={AiOutlinePlusCircle}
              color={'gray.200'}
              boxSize={24}
              onClick={onToggle}
            />
          </Center>
        </Fade>
      )}
      {isOpen && (
        <Fade in={isOpen}>
          <Flex
            flexDir={'column'}
            w={'full'}
            p={4}
            h="full"
            bgColor={'gray.50'}
            borderRadius={'md'}
          >
            <Flex
              flexDir={'row'}
              justifyContent={'space-between'}
              align="center"
              mb={2}
            >
              <Text
                fontSize={'sm'}
                minW={'60px'}
                align={'center'}
                fontWeight={700}
              >
                Chart Type
              </Text>
              <Select
                bgColor={'white'}
                fontSize={'sm'}
                size="sm"
                ml="2"
                onChange={(e) => {
                  const oldCurrentState = [...currentState.peek()];
                  oldCurrentState[0] = e.target.value;
                  currentState.value = oldCurrentState;
                }}
              >
                <option key={`appendNone`} value={''}>
                  None
                </option>
                {chartTypesSignal.value.map((chartType) => (
                  <option
                    key={`append${chartType.mark}`}
                    value={chartType.mark}
                  >
                    {chartType.name}
                  </option>
                ))}
              </Select>
            </Flex>
            <Flex
              flexDir={'row'}
              justifyContent={'space-between'}
              align="center"
              mb={2}
            >
              <Text
                fontSize={'sm'}
                minW={'60px'}
                align={'center'}
                fontWeight={700}
              >
                X
              </Text>
              <Select
                bgColor={'white'}
                fontSize={'sm'}
                size="sm"
                ml="2"
                onChange={(e) => {
                  const oldCurrentState = [...currentState.peek()];
                  oldCurrentState[1] = e.target.value;
                  currentState.value = oldCurrentState;
                }}
              >
                <option key={`appendNone`} value={''}>
                  None
                </option>
                {attributesSignal.value.map((a) => (
                  <option key={`append${a.name}x`} value={a.name}>
                    {a.name}
                  </option>
                ))}
              </Select>
              <Select
                bgColor={'white'}
                fontSize={'sm'}
                ml="2"
                size="sm"
                maxW={'80px'}
                onChange={(e) => {
                  const oldCurrentState = [...currentState.peek()];
                  oldCurrentState[4] = e.target.value;
                  currentState.value = oldCurrentState;
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
              flexDir={'row'}
              justifyContent={'space-between'}
              align="center"
              mb={2}
            >
              <Text
                fontSize={'sm'}
                minW={'60px'}
                align={'center'}
                fontWeight={700}
              >
                Y
              </Text>
              <Select
                bgColor={'white'}
                fontSize={'sm'}
                size="sm"
                ml="2"
                onChange={(e) => {
                  const oldCurrentState = [...currentState.peek()];
                  oldCurrentState[2] = e.target.value;
                  currentState.value = oldCurrentState;
                }}
              >
                <option key={`appendNone`} value={''}>
                  None
                </option>
                {attributesSignal.value.map((a) => (
                  <option key={`append${a.name}x`} value={a.name}>
                    {a.name}
                  </option>
                ))}
              </Select>
              <Select
                bgColor={'white'}
                fontSize={'sm'}
                ml="2"
                size="sm"
                maxW={'80px'}
                onChange={(e) => {
                  const oldCurrentState = [...currentState.peek()];
                  oldCurrentState[5] = e.target.value;
                  currentState.value = oldCurrentState;
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
              flexDir={'row'}
              justifyContent={'space-between'}
              align="center"
              mb={2}
            >
              <Text
                fontSize={'sm'}
                minW={'60px'}
                align={'center'}
                fontWeight={700}
              >
                Z
              </Text>
              <Select
                bgColor={'white'}
                fontSize={'sm'}
                size="sm"
                ml="2"
                onChange={(e) => {
                  const oldCurrentState = [...currentState.peek()];
                  oldCurrentState[3] = e.target.value;
                  currentState.value = oldCurrentState;
                }}
              >
                <option key={`appendNone`} value={''}>
                  None
                </option>
                {attributesSignal.value.map((a) => (
                  <option key={`append${a.name}x`} value={a.name}>
                    {a.name}
                  </option>
                ))}
              </Select>
              <Select
                bgColor={'white'}
                fontSize={'sm'}
                ml="2"
                size="sm"
                maxW={'80px'}
                onChange={(e) => {
                  const oldCurrentState = [...currentState.peek()];
                  oldCurrentState[6] = e.target.value;
                  currentState.value = oldCurrentState;
                }}
              >
                {transformationsSignal.value.map((a) => (
                  <option key={`append${a.type}y`} value={a.type}>
                    {a.name}
                  </option>
                ))}
              </Select>
            </Flex>
            <Spacer />
            <Flex gap={2}>
              <Button
                w="full"
                colorScheme="orange"
                size="sm"
                onClick={() => {
                  onToggle();
                  currentState.value = [
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                  ];
                }}
              >
                Cancel
              </Button>
              <Button
                w="full"
                colorScheme="blue"
                size="sm"
                isDisabled={!isValid.value}
              >
                {isValid.value ? 'Append' : 'Please Input Valid Tuple'}
              </Button>
            </Flex>
          </Flex>
        </Fade>
      )}
    </Box>
  );
};

const ChartView = ({ idx, chart, width, height }: ChartViewProps) => {
  const showDetail = useComputed(() => {
    return inspectionIndexSignal.value === idx;
  });

  return (
    <GridItem>
      <Flex
        flexDir={'column'}
        w={'full'}
        h="fit-content"
        px={2}
        pt={2}
        bgColor={showDetail.value ? 'gray.50' : 'white'}
        borderTopRadius={4}
      >
        <Flex flexDir={'row'} justifyContent={'space-between'} align="center">
          <Icon
            mr={4}
            as={chart.isPinned ? RiPushpinFill : RiPushpinLine}
            boxSize={4}
            onClick={() => {
              togglePinChart(chart.key);
            }}
            _hover={{ cursor: 'pointer' }}
          />
          <Center w="full" verticalAlign={'center'} minH="42px">
            <Text w="full" fontSize={'sm'} textAlign="center">
              {chart.titleToken.map((t, index) =>
                t.isPrefered ? (
                  <Text key={index} as="span" fontWeight={800} color="pink.400">
                    {`${t.text} `}
                  </Text>
                ) : (
                  <Text key={index} as="span" fontWeight={500}>
                    {`${t.text} `}
                  </Text>
                )
              )}
            </Text>
          </Center>
          <Icon
            ml={4}
            as={RiDeleteBinLine}
            boxSize={4}
            onClick={() => {
              removeChart(chart.key);
            }}
            _hover={{ cursor: 'pointer' }}
          />
        </Flex>
        <Center height="full" px={4} mb={2}>
          <VegaLite
            height={height}
            width={width}
            spec={chart.spec}
            actions={false}
            tooltip={new Handler().call}
          />
        </Center>
        <Divider />
        <Flex
          as={motion.div}
          flexDir={'row'}
          justifyContent={'space-between'}
          align="center"
          bgColor={showDetail.value ? 'gray.50' : 'white'}
          borderTopRadius={4}
          p={2}
          pb={4}
          onClick={() => {
            const cur = inspectionIndexSignal.peek();
            if (cur !== idx) {
              inspectionIndexSignal.value = idx;
            } else {
              inspectionIndexSignal.value = -1;
            }
          }}
        >
          <Text fontSize={'sm'} textAlign="center" fontWeight={400} mr="auto">
            Inspection
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

export { ChartAppendView, ChartView };
