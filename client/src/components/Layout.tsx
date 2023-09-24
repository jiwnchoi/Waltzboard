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
import { FiExternalLink } from 'react-icons/fi';
import { IoIosBowtie } from 'react-icons/io';
import { RiArrowDownSLine, RiArrowUpSLine } from 'react-icons/ri';

const Header = () => (
  <Flex
    align="center"
    justifyContent="space-between"
    px={4}
    py={2}
    w="container.2xl"
  >
    <Flex alignItems={'center'}>
      {/* <Icon as={IoIosBowtie} mr={1} boxSize={6} color="gray.500" /> */}
      <Heading size="md" variant={'layout'} alignItems="center">
        Waltzboard
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
      <Link href="https://github.com/jason-choi/waltzboard" isExternal>
        <Button variant={'layout'} leftIcon={<AiFillGithub />} p={0} m={0}>
          GitHub
        </Button>
      </Link>
    </Flex>
  </Flex>
);

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

export { Header, Section };
