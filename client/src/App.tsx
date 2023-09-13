import { Box, Center, Flex, Spinner } from '@chakra-ui/react';
import { Footer, Header } from './components/Layout';
import { Main } from './components/Main';
import { initializedSignal } from './controller/init';

const App = () => (
  <Center w="full" h="full" flexDir={'column'}>
    <Header />
    {initializedSignal.value ? (
      <Main />
    ) : (
      <Center minH={'80vh'} w="full" flexDir={'column'}>
        Loading ...
        <Spinner size="xl" />
      </Center>
    )}
  </Center>
);

export default App;
