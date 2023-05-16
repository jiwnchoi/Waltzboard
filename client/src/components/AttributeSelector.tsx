import { Flex, Icon, Text } from '@chakra-ui/react';
import {
  RiCalendar2Line,
  RiCheckboxCircleFill,
  RiCheckboxCircleLine,
  RiFontSize,
  RiHashtag,
  RiHeartAddFill,
  RiHeartAddLine,
  RiKey2Line,
} from 'react-icons/ri';
import { toggleAttributeIgnore, toggleAttributePrefer } from '../controller/attribute';
import type { Attribute } from '../types/Attribute';

const Attribute = ({ attribute }: { attribute: Attribute }) => {
  return (
    <Flex flexDir={'row'} align="center" bgColor="gray.50" py={1} px={2} borderRadius="md">
      <Icon
        as={
          attribute.type === 'Q'
            ? RiHashtag
            : attribute.type === 'C'
            ? RiFontSize
            : attribute.type === 'N'
            ? RiKey2Line
            : attribute.type === 'T'
            ? RiCalendar2Line
            : undefined
        }
        boxSize={3.5}
        color="gray.900"
        mr={1.5}
      />
      <Text
        fontSize={'2xs'}
        color="gray.700"
        fontWeight={400}
        textOverflow="ellipsis"
        overflow={'hidden'}
        whiteSpace="nowrap"
        w={85}
      >
        {attribute.name}
      </Text>
      <Icon
        as={attribute.ignore ? RiCheckboxCircleLine : RiCheckboxCircleFill}
        boxSize={3.5}
        color="blue.400"
        ml={'auto'}
        mr={1}
        cursor="pointer"
        onClick={() => toggleAttributeIgnore(attribute)}
      />
      <Icon
        as={attribute.prefer ? RiHeartAddFill : RiHeartAddLine}
        boxSize={3.5}
        color="pink.400"
        cursor="pointer"
        onClick={() => toggleAttributePrefer(attribute)}
      />
    </Flex>
  );
};

export default Attribute;
