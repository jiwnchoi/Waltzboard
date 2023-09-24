import { Box, Center, Flex, Spinner } from '@chakra-ui/react';
import { Header } from './components/Layout';
import { Main } from './components/Main';
import { initializedSignal } from './controller/init';

const App = () => (
  <Center w="full" flexDir={'column'} p={0} m={0} overflowY={'hidden'}>
    <Header />
    {initializedSignal.value ? (
      <Main />
    ) : (
      <Center w="full" flexDir={'column'} overflow={'hidden'} p={0} m={0}>
        Loading ...
        <Spinner size="xl" />
      </Center>
    )}
  </Center>
);

export default App;
