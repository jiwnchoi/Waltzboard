import { Flex, Icon, Text } from '@chakra-ui/react';
import {
  RiCheckboxCircleFill,
  RiCheckboxCircleLine,
  RiHeartAddFill,
  RiHeartAddLine,
} from 'react-icons/ri';
import { toggleAggregationIgnore, toggleAggregationPrefer } from '../controller/aggregation';
import { Aggregation } from '../types/Aggregation';

export const AggregationSelector = ({ aggregation }: { aggregation: Aggregation }) => {
  return (
    <Flex flexDir={'row'} align="center" bgColor="gray.50" py={1} px={2} borderRadius="md">
      <Text fontSize={'xs'} color="gray.700" fontWeight={400}>
        {aggregation.name}
      </Text>
      <Icon
        as={aggregation.ignore ? RiCheckboxCircleLine : RiCheckboxCircleFill}
        boxSize={3.5}
        color="blue.400"
        ml={'auto'}
        mr={1}
        cursor="pointer"
        onClick={() => toggleAggregationIgnore(aggregation)}
      />
      <Icon
        as={aggregation.prefer ? RiHeartAddFill : RiHeartAddLine}
        boxSize={3.5}
        color={aggregation.ignore ? 'gray.400' : 'pink.400'}
        cursor="pointer"
        onClick={() => toggleAggregationPrefer(aggregation)}
      />
    </Flex>
  );
};
