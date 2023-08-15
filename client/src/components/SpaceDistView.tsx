import { Box, Flex, FlexProps, Text } from '@chakra-ui/react';
import { AxisBottom } from '@visx/axis';
import { ScaleSVG } from '@visx/responsive';
import { scaleBand, scaleLinear, scaleOrdinal } from '@visx/scale';
import { BarStackHorizontal, Stack } from '@visx/shape';
import { Text as SVGText } from '@visx/text';
import { schemeCategory10 } from 'd3-scale-chromatic';
import {
  aggregationDistSignal,
  attributeDistSignal,
  chartTypeDistSignal,
} from '../controller/train';
import { AggregationDist, AttributeDist, ChartTypeDist } from '../types/Space';
import { LegendOrdinal } from '@visx/legend';

const BAR_HEIGHT = 15;
const SVG_WIDTH = 200;

type Data = ChartTypeDist | AggregationDist | AttributeDist;
type Key = 'x' | 'y' | 'z' | 'prob';

interface SVGProp {
  data: Data[];
  keys: Key[];
  xMax: number;
  yMax: number;
  height: number;
  width: number;
  yScale: any;
  xScale: any;
  colorScale: any;
}

function getSVGProp(data: Data[], keys: Key[]): SVGProp {
  return {
    data,
    keys,
    xMax: SVG_WIDTH - margin.left - margin.right,
    yMax: data.length * BAR_HEIGHT,
    height: data.length * BAR_HEIGHT + margin.top + margin.bottom,
    width: SVG_WIDTH,
    yScale: scaleBand<string>({
      domain: data.map((d) => d.name),
      padding: 0.1,
      range: [data.length * BAR_HEIGHT, 0],
    }),
    xScale: scaleLinear<number>({
      domain: [0, keys.length == 1 ? 1 : 2],
      nice: true,
      range: [margin.left, SVG_WIDTH - margin.left - margin.right],
    }),
    colorScale: scaleOrdinal<string, string>({
      domain: keys,
      range: schemeCategory10.slice(0, 4),
    }),
  };
}

const margin = { top: 15, bottom: 15, left: 10, right: 10 };

const StackedBarChart = ({ title, svgProp }: { title: string; svgProp: SVGProp }) => {
  return (
    <>
      <Flex flexDir={'row'} justifyContent={'space-between'} px={1} verticalAlign={'center'}>
        <Text fontSize={12} fontWeight={500} color={'gray.500'} mb={1} mt={1}>
          {title}
        </Text>
        {title == 'Attributes' && (
          <LegendOrdinal
            scale={svgProp.colorScale}
            direction="row"
            labelMargin="0 15px 0 0"
            shapeMargin="0 0 0 0"
            shapeHeight={10}
            shapeWidth={10}
            labelFormat={(label: any) => `${label.toUpperCase()} `}
          >
            {(labels) => (
              <Flex flexDir={'row'} gap={1}>
                {labels.map((label, i) => (
                  <Flex key={`legend-${i}`} alignItems={'center'} mb={1}>
                    <Box
                      bg={label.value}
                      h={2}
                      w={2}
                      mr={1}
                      borderRadius={'50%'}
                      border={'1px solid'}
                      borderColor={'gray.300'}
                    />
                    <Text fontSize={11} color={'gray.500'}>
                      {label.text}
                    </Text>
                  </Flex>
                ))}
              </Flex>
            )}
          </LegendOrdinal>
        )}
      </Flex>

      <ScaleSVG width={svgProp.width} height={svgProp.height}>
        <BarStackHorizontal<Data, Key>
          data={svgProp.data}
          keys={svgProp.keys}
          height={svgProp.yMax}
          y={(d: Data) => d.name}
          xScale={svgProp.xScale}
          yScale={svgProp.yScale}
          color={svgProp.colorScale}
        >
          {(barStacks) =>
            barStacks.map((barStack, i) => (
              <>
                {barStack.bars.map((bar) => (
                  <rect
                    key={`${title}-${barStack.index}-${bar.index}`}
                    x={bar.x}
                    y={bar.y}
                    width={bar.width}
                    height={bar.height}
                    fill={bar.color}
                  />
                ))}
                {i == barStacks.length - 1 &&
                  barStack.bars.map((bar, j) => (
                    <SVGText
                      key={`${title}-${i}-${j}`}
                      x={bar.x + bar.width + 10}
                      y={bar.y + bar.height / 2}
                      verticalAnchor="middle"
                      fill="gray"
                      fontSize={9}
                      textAnchor="start"
                    >
                      {bar.bar.data.name}
                    </SVGText>
                  ))}
              </>
            ))
          }
        </BarStackHorizontal>
        <AxisBottom
          top={svgProp.yMax}
          scale={svgProp.xScale}
          stroke={'#E2E2E2'}
          tickStroke="#E2E2E2"
          tickLabelProps={() => ({
            fill: 'gray',
            fontSize: 11,
            textAnchor: 'middle',
          })}
          numTicks={6}
        />
      </ScaleSVG>
    </>
  );
};

const SpaceDistView = (props: FlexProps) => {
  const chartTypeProp = getSVGProp(chartTypeDistSignal.value, ['prob']);
  const aggregationProp = getSVGProp(aggregationDistSignal.value, ['prob']);
  const attributeProp = getSVGProp(attributeDistSignal.value, ['x', 'y', 'z']);

  return (
    <Flex {...props} flexDir={'column'}>
      <StackedBarChart title="Chart Types" svgProp={chartTypeProp} />
      <StackedBarChart title="Aggregations" svgProp={aggregationProp} />
      <StackedBarChart title="Attributes" svgProp={attributeProp} />
    </Flex>
  );
};

export default SpaceDistView;
