import { Box, Flex, FlexProps, Text } from '@chakra-ui/react';
import { AxisTop } from '@visx/axis';
import { LegendOrdinal } from '@visx/legend';
import { ScaleSVG } from '@visx/responsive';
import { scaleBand, scaleLinear, scaleOrdinal } from '@visx/scale';
import { BarStackHorizontal } from '@visx/shape';
import { Text as SVGText } from '@visx/text';
import { schemeCategory10 } from 'd3-scale-chromatic';
import {
  attributeDistSignal,
  chartTypeDistSignal,
  transformationDistSignal,
} from '../controller/train';
import {
  AttributeDist,
  ChartTypeDist,
  TransformationDist,
} from '../types/Space';

const BAR_HEIGHT = 20;
const SVG_WIDTH = 180;

type Data = ChartTypeDist | TransformationDist | AttributeDist;
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
    data: data,
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
      domain: [0, keys.length == 1 ? 1 : 1],
      nice: true,
      range: [margin.left, SVG_WIDTH - margin.left - margin.right],
    }),
    colorScale: scaleOrdinal<string, string>({
      domain: keys,
      range: schemeCategory10.slice(0, 4),
    }),
  };
}

const margin = { top: 20, bottom: 15, left: 15, right: 5 };

const StackedBarChart = ({
  title,
  svgProp,
}: {
  title: string;
  svgProp: SVGProp;
}) => {
  return (
    <Box>
      <Flex
        flexDir={'row'}
        justifyContent={'space-between'}
        px={1}
        verticalAlign={'center'}
      >
        <Text fontSize={'sm'} fontWeight={500} color={'gray.500'} mb={1} mt={1}>
          {title}
        </Text>
        {title != 'Chart Types' && (
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
                    <Text fontSize={'xs'} color={'gray.500'}>
                      {label.text}
                    </Text>
                  </Flex>
                ))}
              </Flex>
            )}
          </LegendOrdinal>
        )}
      </Flex>
      <ScaleSVG width={svgProp.width} height={22}>
        <AxisTop
          top={margin.top}
          scale={svgProp.xScale}
          stroke={'gray'}
          tickStroke="gray"
          strokeWidth={1}
          tickLabelProps={() => ({
            fill: 'gray',
            fontSize: 11,
            textAnchor: 'middle',
          })}
          numTicks={6}
        />
      </ScaleSVG>
      <Box w="full" h={120} overflowY={'scroll'}>
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
                        x={bar.x + bar.width + 6}
                        y={bar.y + bar.height / 2}
                        verticalAnchor="middle"
                        fill="gray"
                        fontSize={12}
                        textAnchor="start"
                      >
                        {bar.bar.data.name}
                      </SVGText>
                    ))}
                </>
              ))
            }
          </BarStackHorizontal>
        </ScaleSVG>
      </Box>
    </Box>
  );
};

const SpaceDistView = (props: FlexProps) => {
  const chartTypeProp = getSVGProp(chartTypeDistSignal.value, ['prob']);
  const transformationProp = getSVGProp(
    transformationDistSignal.value.filter((d) => d.name !== 'None'),
    ['x', 'y', 'z']
  );
  const attributeProp = getSVGProp(
    attributeDistSignal.value.filter((d) => d.name !== 'None'),
    ['x', 'y', 'z']
  );

  return (
    <Flex {...props} flexDir={'column'}>
      <StackedBarChart title="Chart Types" svgProp={chartTypeProp} />
      <StackedBarChart title="Transformations" svgProp={transformationProp} />
      <StackedBarChart title="Attributes" svgProp={attributeProp} />
    </Flex>
  );
};

export default SpaceDistView;
