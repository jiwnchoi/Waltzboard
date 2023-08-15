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

const BAR_HEIGHT = 15;
const SVG_WIDTH = 300;

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
      domain: [0, 1],
      nice: true,
      range: [margin.left, SVG_WIDTH - margin.left - margin.right],
    }),
    colorScale: scaleOrdinal<string, string>({
      domain: keys,
      range: schemeCategory10.slice(0, 4),
    }),
  };
}

const margin = { top: 15, bottom: 15, left: 12, right: 12 };

const StackedBarChart = ({ svgProp }: { svgProp: SVGProp }) => {
  return (
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
                  key={`bar-stack-horizontal-${barStack.index}-${bar.index}`}
                  x={bar.x}
                  y={bar.y}
                  width={bar.width}
                  height={bar.height}
                  fill={bar.color}
                />
              ))}
              {i == barStacks.length - 1 &&
                barStack.bars.map((bar) => (
                  <SVGText
                    key={`bar-label-${barStack.index}`}
                    x={bar.x + bar.width + 10}
                    y={bar.y + bar.height / 2}
                    verticalAnchor="middle"
                    fill="gray"
                    fontSize={11}
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
  );
};

const SpaceDistView = (props: FlexProps) => {
  const chartTypeProp = getSVGProp(chartTypeDistSignal.value, ['prob']);
  const aggregationProp = getSVGProp(aggregationDistSignal.value, ['prob']);
  const attributeProp = getSVGProp(attributeDistSignal.value, ['x', 'y', 'z']);

  return (
    <Flex {...props} flexDir={'column'}>
      <Box mb={2} />
      <StackedBarChart svgProp={chartTypeProp} />
      <StackedBarChart svgProp={aggregationProp} />
      <StackedBarChart svgProp={attributeProp} />
    </Flex>
  );
};

export default SpaceDistView;
