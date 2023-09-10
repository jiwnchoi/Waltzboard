import {
  Badge,
  Button,
  Center,
  Collapse,
  Divider,
  Flex,
  Grid,
  GridItem,
  Icon,
  Select,
  Spacer,
  Text,
} from '@chakra-ui/react';
import { useSignal, useSignalEffect } from '@preact/signals-react';
import {
  RiArrowDownSLine,
  RiArrowUpSLine,
  RiDeleteBinLine,
  RiPushpinFill,
  RiPushpinLine,
} from 'react-icons/ri';
import { VegaLite } from 'react-vega';
import { Handler } from 'vega-tooltip';
import { attributesSignal } from '../controller/attribute';
import { chartTypesSignal } from '../controller/chartType';
import { removeChart, togglePinChart } from '../controller/dashboard';
import { inferResponseSignal } from '../controller/infer';
import { transformationsSignal } from '../controller/transformation';
import type { ChartView } from '../types/ChartView';

const StatisticFeatureBadge = ({ feature }: { feature: string | null }) => {
  if (feature === null) return null;
  return (
    <GridItem>
      <Badge>{feature.replace('has_', '')}</Badge>
    </GridItem>
  );
};
interface ChartViewProps {
  chart: ChartView;
  width: number;
  height: number;
}

const ChartAppendView = () => {
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
    console.log(currentState.value);
  });
  return (
    <Flex
      flexDir={'column'}
      w={'full'}
      p={2}
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
        <Text fontSize={'sm'} minW={'80px'} align={'center'} fontWeight={700}>
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
          <option key={`appendNone`} value={'none'}>
            None
          </option>
          {chartTypesSignal.value.map((chartType) => (
            <option key={`append${chartType.mark}`} value={chartType.mark}>
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
        <Text fontSize={'sm'} minW={'80px'} align={'center'} fontWeight={700}>
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
          <option key={`appendNone`} value={'none'}>
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
        <Text fontSize={'sm'} minW={'80px'} align={'center'} fontWeight={700}>
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
          <option key={`appendNone`} value={'none'}>
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
        <Text fontSize={'sm'} minW={'80px'} align={'center'} fontWeight={700}>
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
          <option key={`appendNone`} value={'none'}>
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
      <Button colorScheme="blue" size="sm">
        Append
      </Button>
    </Flex>
  );
};

const ChartView = ({ chart, width, height }: ChartViewProps) => {
  const showStatistics = useSignal(false);
  const toggleShowStatistics = () => {
    showStatistics.value = !showStatistics.value;
  };
  return (
    <Flex flexDir={'column'} w={'full'} h="fit-content" p={2}>
      <Flex
        flexDir={'row'}
        justifyContent={'space-between'}
        align="center"
        mb={2}
      >
        <Icon
          mr={4}
          as={chart.isPinned ? RiPushpinFill : RiPushpinLine}
          boxSize={4}
          onClick={() => {
            togglePinChart(chart.key);
          }}
          _hover={{ cursor: 'pointer' }}
        />
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
      <Divider mb={2} />
      <Flex flexDir={'row'} justifyContent={'space-between'} align="center">
        <Text fontSize={'sm'} textAlign="center" fontWeight={400} mr="auto">
          Inspectation Detail
        </Text>

        {showStatistics.value ? (
          <Icon
            as={RiArrowDownSLine}
            boxSize={4}
            onClick={toggleShowStatistics}
          />
        ) : (
          <Icon
            as={RiArrowUpSLine}
            boxSize={4}
            onClick={toggleShowStatistics}
          />
        )}
      </Flex>

      <Collapse in={showStatistics.value} animateOpacity>
        <Flex flexDir={'column'} gap={2} mt={2}>
          <Text fontSize={'sm'} minW={'80px'} align={'center'} fontWeight={700}>
            This chart contributes to{' '}
          </Text>
          {/* specificity interestingnenss coverage diversity parsimony */}
          {chart.chartResults &&
          Math.abs(
            inferResponseSignal.value.result.specificity -
              chart.chartResults.specificity
          ) > 0.05 ? (
            <Text as="p">
              <Text as="span">Specificity as</Text>
              <Text as="span" fontWeight={800} color="pink.400">
                {` ${(
                  inferResponseSignal.value.result.specificity -
                  chart.chartResults.specificity
                ).toFixed(2)} `}
              </Text>
            </Text>
          ) : null}
          {chart.chartResults &&
          Math.abs(
            inferResponseSignal.value.result.interestingness -
              chart.chartResults.interestingness
          ) > 0.05 ? (
            <Text as="p">
              <Text as="span">Interestingness as</Text>
              <Text as="span" fontWeight={800} color="pink.400">
                {` ${(
                  inferResponseSignal.value.result.interestingness -
                  chart.chartResults.interestingness
                ).toFixed(2)} `}
              </Text>
            </Text>
          ) : null}
          {chart.chartResults &&
          Math.abs(
            inferResponseSignal.value.result.coverage -
              chart.chartResults.coverage
          ) > 0.05 ? (
            <Text as="p">
              <Text as="span">Coverage as</Text>
              <Text as="span" fontWeight={800} color="pink.400">
                {` ${(
                  inferResponseSignal.value.result.coverage -
                  chart.chartResults.coverage
                ).toFixed(2)} `}
              </Text>
            </Text>
          ) : null}
          {chart.chartResults &&
          Math.abs(
            inferResponseSignal.value.result.diversity -
              chart.chartResults.diversity
          ) > 0.05 ? (
            <Text as="p">
              <Text as="span">Diversity as</Text>
              <Text as="span" fontWeight={800} color="pink.400">
                {` ${(
                  inferResponseSignal.value.result.diversity -
                  chart.chartResults.diversity
                ).toFixed(2)} `}
              </Text>
            </Text>
          ) : null}
          {chart.chartResults &&
          Math.abs(
            inferResponseSignal.value.result.parsimony -
              chart.chartResults.parsimony
          ) > 0.05 ? (
            <Text as="p">
              <Text as="span">Parsimony as</Text>
              <Text as="span" fontWeight={800} color="pink.400">
                {` ${(
                  inferResponseSignal.value.result.parsimony -
                  chart.chartResults.parsimony
                ).toFixed(2)} `}
              </Text>
            </Text>
          ) : null}

          {Object.keys(chart.statistics).map((key, i) => {
            if (chart.statistics[key].filter((f) => f !== null).length === 0)
              return null;
            return (
              <Flex gap={1} key={`stat-${i}`} align={'center'}>
                <Text
                  fontSize={'sm'}
                  textAlign="start"
                  fontWeight={400}
                  mr="auto"
                  textOverflow="ellipsis"
                  overflow={'hidden'}
                  whiteSpace="nowrap"
                  w={'50%'}
                >
                  {key
                    .replace("['", '')
                    .replace("']", '')
                    .replace("', '", ' & ')}
                </Text>
                <Grid templateColumns={'repeat(2, 1fr)'} gap={1} w={'50%'}>
                  {chart.statistics[key].map((feature) => (
                    <StatisticFeatureBadge feature={feature} />
                  ))}
                </Grid>
              </Flex>
            );
          })}
        </Flex>
      </Collapse>
    </Flex>
  );
};

export { ChartAppendView, ChartView };
