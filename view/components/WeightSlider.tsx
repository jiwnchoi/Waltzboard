import {
  Flex,
  FlexProps,
  Input,
  Slider,
  SliderFilledTrack,
  SliderThumb,
  SliderTrack,
  Text,
} from "@chakra-ui/react";
import { weightSignal } from "../controller/oracleWeight";
import { useRef } from "react";
import t from "../../locales/default.json";

interface WeightSliderProps extends FlexProps {
  title:
    | "coverage"
    | "diversity"
    | "interestingness"
    | "specificity"
    | "parsimony";
}

const WeightSlider = (props: WeightSliderProps) => {
  const ref = useRef<HTMLInputElement>(null);

  return (
    <Flex flexDir="column" mb={1}>
      <Flex flexDir={"row"} justifyContent={"space-between"}>
        <Text fontSize={"sm"} color={"gray.500"} fontWeight={500}>
          {t[`text-${props.title}` as keyof typeof t]}
        </Text>

        <Input
          ref={ref}
          size={"sm"}
          w={4}
          border={"none"}
          m={1}
          p={0}
          h={4}
          textAlign={"end"}
          defaultValue={weightSignal.value[props.title]}
          onKeyUp={(e) => {
            if (e.key === "Enter") {
              if (e.currentTarget.value === "") return;
              let n = parseInt(e.currentTarget.value);
              if (n > 2) n = 2;
              if (n < 0) n = 0;

              weightSignal.value[props.title] = n;
              e.currentTarget.value = String(n);
              weightSignal.value = { ...weightSignal.value };
            }
          }}
        />
      </Flex>
      <Flex mx={2}>
        <Slider
          aria-label={`slider-ex-${props.title}`}
          value={weightSignal.value[props.title]}
          min={0}
          max={2}
          step={1}
          width={"full"}
          onChange={(value) => {
            ref && ref.current && (ref.current.value = String(value));
            weightSignal.value[props.title] = value;
            weightSignal.value = { ...weightSignal.value };
          }}
        >
          <SliderTrack>
            <SliderFilledTrack color={"blue.400"} />
          </SliderTrack>
          <SliderThumb borderColor={"blue.500"} />
        </Slider>
      </Flex>
    </Flex>
  );
};

export default WeightSlider;
