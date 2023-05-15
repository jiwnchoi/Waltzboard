import { Button, Collapse, Flex, FlexProps, Heading, Icon, Link, Text } from '@chakra-ui/react';
import { useSignal } from '@preact/signals-react';
import { AiFillGithub } from 'react-icons/ai';
import { GiWheat } from 'react-icons/gi';
import { RiArrowDownSLine, RiArrowUpSLine } from 'react-icons/ri';

const Header = () => {
  return (
    <Flex align="center" justifyContent="space-between" px={4} py={2}>
      <Flex alignItems={'center'}>
        <Icon as={GiWheat} mr={1} boxSize={6} color="gray.500" />
        <Heading size="md" variant={'layout'} alignItems="center">
          Gleaner
        </Heading>
      </Flex>
      <Link href="https://github.com/jason-choi/vis-tiller" isExternal>
        <Button variant={'layout'} leftIcon={<AiFillGithub />}>
          GitHub
        </Button>
      </Link>
    </Flex>
  );
};

const Footer = () => {
  return (
    <Flex mt="auto" align="center" py={4} px={4} flexDir="column" alignItems="start">
      <Link href="https://idclab.skku.edu" isExternal>
        <Flex>
          <Text variant={'layout'} fontFamily="Rajdhani" fontWeight={900} fontSize="xl">
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
      <Link href="https://cs.skku.edu" isExternal>
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
}
const Section = (props: SectionProps) => {
  const show = useSignal<boolean | undefined>(!props.collapsed);

  const toggleShow = () => {
    show.value = !show.value;
  };

  return (
    <Flex
      flexDir={'column'}
      w="full"
      h={props.height}
      minH={props.minH}
      gap={props.gap}
      p={2}
      bgColor="white"
      borderRadius="md"
      boxShadow="sm"
    >
      <Flex flexDir={'row'} justifyContent={'space-between'} alignItems={'center'}>
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
          bgColor="white"
          borderRadius="md"
          boxShadow="sm"
        >
          {props.children}
        </Flex>
      </Collapse>
    </Flex>
  );
};

export { Header, Footer, Section };
