import { Flex, Icon, Text } from '@chakra-ui/react';
import {
  RiCheckboxCircleFill,
  RiCheckboxCircleLine,
  RiHeartAddFill,
  RiHeartAddLine,
} from 'react-icons/ri';
import { toggleChartTypeIgnore, toggleChartTypePrefer } from '../controller/chartType';

import type { ChartType } from '../types/ChartType';

export const ChartTypeSelector = ({ chartType }: { chartType: ChartType }) => {
  return (
    <Flex flexDir={'row'} align="center" bgColor="gray.50" py={1} px={2} borderRadius="md">
      <Text fontSize={'xs'} color="gray.700" fontWeight={400}>
        {chartType.name}
      </Text>
      <Icon
        as={chartType.ignore ? RiCheckboxCircleLine : RiCheckboxCircleFill}
        boxSize={3.5}
        color="blue.400"
        ml={'auto'}
        mr={1}
        cursor="pointer"
        onClick={() => toggleChartTypeIgnore(chartType)}
      />
      <Icon
        as={chartType.prefer ? RiHeartAddFill : RiHeartAddLine}
        boxSize={3.5}
        color={chartType.ignore ? 'gray.400' : 'red.400'}
        cursor="pointer"
        onClick={() => toggleChartTypePrefer(chartType)}
      />
    </Flex>
  );
};
