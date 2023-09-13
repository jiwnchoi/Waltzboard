import {
  Button,
  Collapse,
  Flex,
  FlexProps,
  Heading,
  Icon,
  Link,
  Text,
} from '@chakra-ui/react';
import { useSignal } from '@preact/signals-react';
import { AiFillGithub } from 'react-icons/ai';
import { BsPlusSquareDotted } from 'react-icons/bs';
import { FiExternalLink } from 'react-icons/fi';
import { GiWheat } from 'react-icons/gi';
import { RiArrowDownSLine, RiArrowUpSLine } from 'react-icons/ri';
import { toggleAppendPanel } from '../controller/append';

const Header = () => (
  <Flex align="center" justifyContent="space-between" px={4} py={2} w="full">
    <Flex alignItems={'center'}>
      <Icon as={GiWheat} mr={1} boxSize={6} color="gray.500" />
      <Heading size="md" variant={'layout'} alignItems="center">
        Gleaner
      </Heading>
    </Flex>
    <Flex alignItems={'center'} gap={4}>
      <Link href="https://idclab.skku.edu" isExternal>
        <Button variant={'layout'} leftIcon={<FiExternalLink />} p={0} m={0}>
          <Text
            variant={'layout'}
            fontFamily="Rajdhani"
            fontWeight={900}
            fontSize="lg"
          >
            IDC
          </Text>
          <Text
            variant={'layout'}
            fontFamily="Rajdhani"
            fontSize="lg"
            fontWeight={500}
          >
            Lab
          </Text>
        </Button>
      </Link>
      <Link href="https://github.com/jason-choi/gleaner" isExternal>
        <Button variant={'layout'} leftIcon={<AiFillGithub />} p={0} m={0}>
          GitHub
        </Button>
      </Link>
    </Flex>
  </Flex>
);

const Footer = () => {
  return (
    <Flex
      mt="auto"
      align="center"
      py={4}
      px={4}
      flexDir="column"
      alignItems="start"
      position={'relative'}
      bottom={0}
      w="full"
    >
      <Link href="https://idclab.skku.edu" isExternal>
        <Flex>
          <Text
            variant={'layout'}
            fontFamily="Rajdhani"
            fontWeight={900}
            fontSize="xl"
          >
            IDC
          </Text>
          <Text variant={'layout'} fontFamily="Rajdhani" fontSize="xl">
            Lab
          </Text>
        </Flex>
      </Link>

      <Link href="https://skku.edu" isExternal>
        <Text variant={'layout'} fontSize="sm">
          Sungkyunkwan University
        </Text>
      </Link>
      <Link href="https://sw.skku.edu" isExternal>
        <Text variant={'layout'} fontSize="sm">
          College of Computing and Informatics
        </Text>
      </Link>
    </Flex>
  );
};

interface SectionProps extends FlexProps {
  title: string;
  collapsed?: boolean;
  innerOverflowX?:
    | 'scroll'
    | 'hidden'
    | 'visible'
    | 'auto'
    | 'initial'
    | 'inherit'
    | undefined;
  innerOverflowY?:
    | 'scroll'
    | 'hidden'
    | 'visible'
    | 'auto'
    | 'initial'
    | 'inherit'
    | undefined;
}
const Section = (props: SectionProps) => {
  const show = useSignal<boolean | undefined>(!props.collapsed);

  const toggleShow = () => {
    show.value = !show.value;
  };

  return (
    <Flex
      {...props}
      flexDir={'column'}
      w="full"
      p={2}
      bgColor="white"
      borderRadius="md"
      boxShadow="sm"
    >
      <Flex
        flexDir={'row'}
        justifyContent={'space-between'}
        alignItems={'center'}
      >
        <Heading variant={'section'}>{props.title}</Heading>
        {show.value ? (
          <Icon as={RiArrowDownSLine} boxSize={4} onClick={toggleShow} />
        ) : (
          <Icon as={RiArrowUpSLine} boxSize={4} onClick={toggleShow} />
        )}
      </Flex>
      <Collapse in={show.value} animateOpacity>
        <Flex
          flexDir={'column'}
          w="full"
          gap={props.gap}
          maxH={props.maxH}
          overflowX={props.innerOverflowX}
          overflowY={props.innerOverflowY}
        >
          {props.children}
        </Flex>
      </Collapse>
    </Flex>
  );
};

const MainSection = (props: SectionProps) => {
  return (
    <Flex
      {...props}
      flexDir={'column'}
      w="full"
      p={2}
      bgColor="white"
      borderRadius="md"
      boxShadow="sm"
    >
      <Flex
        flexDir={'row'}
        justifyContent={'space-between'}
        alignItems={'center'}
      >
        <Heading variant={'section'}>{props.title}</Heading>
        <Button
          colorScheme="blue"
          size={'xs'}
          leftIcon={<BsPlusSquareDotted />}
          onClick={toggleAppendPanel}
        >
          <Text>Append Chart</Text>
        </Button>
      </Flex>
      <Flex
        flexDir={'column'}
        w="full"
        gap={props.gap}
        maxH={props.maxH}
        overflowX={props.innerOverflowX}
        overflowY={props.innerOverflowY}
      >
        {props.children}
      </Flex>
    </Flex>
  );
};

export { Footer, Header, MainSection, Section };

