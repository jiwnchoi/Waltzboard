import { Flex, FlexProps, Text } from "@chakra-ui/react"
import { ScaleSVG } from "@visx/responsive";
import { BarStackHorizontal } from "@visx/shape";
import { AttributeDist } from "../types/Space";

interface SpaceDistViewProps extends FlexProps {
    svgWidth: number;
}

const SpaceDistView = ( props: SpaceDistViewProps ) => {

    return (
        <Flex {... props} >
            <Text fontSize={"sm"} color="gray.500">ChartType</Text>
            <ScaleSVG width={props.svgWidth}>
                <BarStackHorizontal<AttributeDist, string>>
            </ScaleSVG>
        </Flex>
    )


}

export default SpaceDistView;