import { Flex, Icon, Text } from '@chakra-ui/react';
import {
  RiCheckboxCircleFill,
  RiCheckboxCircleLine,
  RiHeartAddFill,
  RiHeartAddLine,
} from 'react-icons/ri';
import {
  toggleTransformationIgnore,
  toggleTransformationPrefer,
} from '../controller/transformation';
import { Transformation } from '../types/Transformation';

export const TransformationSelector = ({
  transformation,
}: {
  transformation: Transformation;
}) => {
  return (
    <Flex
      flexDir={'row'}
      align="center"
      bgColor="gray.50"
      py={1}
      px={2}
      borderRadius="md"
    >
      <Text fontSize={'sm'} color="gray.700" fontWeight={400}>
        {transformation.name}
      </Text>
      <Icon
        as={transformation.ignore ? RiCheckboxCircleLine : RiCheckboxCircleFill}
        boxSize={3.5}
        color="blue.400"
        ml={'auto'}
        mr={1}
        cursor="pointer"
        onClick={() => toggleTransformationIgnore(transformation)}
      />
      <Icon
        as={transformation.prefer ? RiHeartAddFill : RiHeartAddLine}
        boxSize={3.5}
        color={transformation.ignore ? 'gray.400' : 'pink.400'}
        cursor="pointer"
        onClick={() => toggleTransformationPrefer(transformation)}
      />
    </Flex>
  );
};
