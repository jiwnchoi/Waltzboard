import { Button, Center, Heading, Input, effect } from "@chakra-ui/react";
import { useSignal, useSignalEffect } from "@preact/signals-react";
import { Header } from "./components/Layout";
import { Main } from "./components/Main";
import { init, initializedSignal } from "./controller/init";

const App = () => {
  const userId = useSignal<string | null>(import.meta.env.DEV ? null : "test");
  useSignalEffect(() => {
    if (true) {
      init("test");
    }
  });
  return (
    <Center w="full" flexDir={"column"} p={0} m={0} overflowY={"hidden"}>
      <Header />
      {initializedSignal.value && <Main />}
      {!initializedSignal.value && (
        <Center
          w="full"
          minH={800}
          flexDir={"column"}
          overflow={"hidden"}
          p={0}
          m={0}
        >
          <Center flexDir={"column"} gap={8}>
            <Heading>Input User Auth Code</Heading>
            <Input
              w={400}
              bgColor={"white"}
              placeholder="User Auth Code"
              onChange={(e) => {
                userId.value = e.target.value;
              }}
            />
            <Button
              w={400}
              colorScheme="blue"
              disabled={userId.value === null}
              onClick={() => {
                init(String(userId.value));
              }}
            >
              Sign In
            </Button>
          </Center>
        </Center>
      )}
    </Center>
  );
};

export default App;
