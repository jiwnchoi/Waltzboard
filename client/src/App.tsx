import { Box, Center, Flex, Spinner } from '@chakra-ui/react';
import { Footer, Header } from './components/Layout';
import { Main } from './components/Main';
import { initializedSignal } from './controller/init';

const App = () => (
  <Center flexDir={'column'} w="full">
    <Header />
    <Center w="100vw" justifyContent="center" alignItems={'center'}>
      {initializedSignal.value ? (
        <Main />
      ) : (
        <Center minH={'80vh'} w="full">
          Loading ...
          <Spinner size="xl" />
        </Center>
      )}
    </Center>
    <Footer />
  </Center>
);

export default App;
