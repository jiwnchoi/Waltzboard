import { Divider, Flex, Icon, Text } from '@chakra-ui/react';
import {
  RiCalendar2Line,
  RiCheckboxCircleFill,
  RiCheckboxCircleLine,
  RiFontSize,
  RiHashtag,
  RiHeartAddFill,
  RiHeartAddLine,
} from 'react-icons/ri';
import {
  toggleAttributeIgnore,
  toggleAttributePrefer,
} from '../controller/attribute';
import {
  dayTransformationsSignal,
  toggleTransformationIgnore,
  toggleTransformationPrefer,
} from '../controller/transformation';
import type { Attribute } from '../types/Attribute';
const AttributeSelector = ({ attribute }: { attribute: Attribute }) => {
  return (
    <Flex
      flexDir={'column'}
      bgColor="gray.50"
      py={1}
      px={2}
      borderRadius="md"
      gap={1}
    >
      <Flex flexDir={'row'} align="center">
        <Icon
          as={
            attribute.type === 'Q'
              ? RiHashtag
              : attribute.type === 'N'
              ? RiFontSize
              : attribute.type === 'T'
              ? RiCalendar2Line
              : undefined
          }
          boxSize={3.5}
          color="gray.900"
          mr={1.5}
        />
        <Text
          fontSize={'sm'}
          color="gray.700"
          fontWeight={400}
          textOverflow="ellipsis"
          overflow={'hidden'}
          whiteSpace="nowrap"
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
      {attribute.type === 'T' && (
        <>
          <Divider />
          {dayTransformationsSignal.value.map((t, i) => (
            <Flex flexDir={'row'} align="center">
              <Text
                fontSize={'sm'}
                color="gray.700"
                fontWeight={400}
                textOverflow="ellipsis"
                whiteSpace="nowrap"
              >
                {t.name}
              </Text>
              <Icon
                as={t.ignore ? RiCheckboxCircleLine : RiCheckboxCircleFill}
                boxSize={3.5}
                color="blue.400"
                ml={'auto'}
                mr={1}
                cursor="pointer"
                onClick={() => toggleTransformationIgnore(t)}
              />
              <Icon
                as={t.prefer ? RiHeartAddFill : RiHeartAddLine}
                boxSize={3.5}
                color="pink.400"
                cursor="pointer"
                onClick={() => toggleTransformationPrefer(t)}
              />
            </Flex>
          ))}
        </>
      )}
    </Flex>
  );
};

export default AttributeSelector;
