import {
  Flex,
  FlexProps,
  Slider,
  SliderFilledTrack,
  SliderThumb,
  SliderTrack,
  Text,
} from '@chakra-ui/react';
import { weightSignal } from '../controller/oracleWeight';
import { unSelectTaskType } from '../controller/taskType';

interface WeightSliderProps extends FlexProps {
  title:
    | 'coverage'
    | 'diversity'
    | 'interestingness'
    | 'specificity'
    | 'parsimony';
}

const WeightSlider = (props: WeightSliderProps) => {
  return (
    <Flex flexDir="column">
      <Flex flexDir={'row'} justifyContent={'space-between'}>
        <Text fontSize={'sm'} color={'gray.500'} fontWeight={500}>
          {props.title[0].toUpperCase() + props.title.slice(1)}
        </Text>
        <Text fontSize={'sm'} fontWeight={600}>
          {weightSignal.value[props.title]}
        </Text>
      </Flex>
      <Slider
        aria-label={`slider-ex-${props.title}`}
        value={weightSignal.value[props.title]}
        min={0}
        max={2}
        step={1}
        width={'full'}
        onChange={(value) => {
          weightSignal.value[props.title] = value;
          weightSignal.value = { ...weightSignal.value };
          unSelectTaskType();
        }}
      >
        <SliderTrack>
          <SliderFilledTrack color={'blue.400'} />
        </SliderTrack>
        <SliderThumb borderColor={'blue.500'} />
      </Slider>
    </Flex>
  );
};

export default WeightSlider;
