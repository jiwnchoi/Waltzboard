import { Center, Flex, Spinner } from '@chakra-ui/react';
import { Footer, Header } from './components/Layout';
import { Main } from './components/Main';
import { initializedSignal } from './controller/init';

const App = () => {
  return (
    <Flex flexDir={'column'}>
      <Header />
      {initializedSignal.value ? (
        <>
          <Main />
          <Footer />
        </>
      ) : (
        <Center minH={'80vh'} flexDir="column" gap={10}>
          Building Design Space ...
          <Spinner size="xl" />
        </Center>
      )}
    </Flex>
  );
};

export default App;
