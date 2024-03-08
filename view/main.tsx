import { ChakraProvider, extendTheme } from "@chakra-ui/react";
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

import "@fontsource/rajdhani";
import "pretendard/dist/web/variable/pretendardvariable.css";

const theme = extendTheme({
  fonts: {
    heading: "Pretendard Variable",
    body: "Pretendard Variable",
  },
  styles: {
    global: {
      body: {
        bg: "gray.100",
      },
    },
  },
  components: {
    Text: {
      variants: {
        layout: {
          color: "gray.500",
        },
      },
    },
    Heading: {
      variants: {
        layout: {
          fontWeight: 900,
          color: "gray.500",
        },
        section: {
          fontSize: "md",
          fontWeight: 700,
          color: "gray.700",
        },
      },
    },
    Button: {
      variants: {
        layout: {
          color: "gray.500",
          backgroundColor: "transparent",
        },
      },
    },
    Link: {
      baseStyle: {
        _hover: {
          textDecoration: "none",
        },
      },
    },
  },
});

theme.sizes.container["2xl"] = "1920px";

function setScalingFactor() {
  const vw = window.innerWidth;
  const vh = window.innerHeight;
  const referenceWidth = 1920;
  const referenceHeight = 1080;
  const scaleX = vw / referenceWidth;
  const scaleY = vh / referenceHeight;
  const scale = scaleX;
  (document.body.style as any).zoom = scale * 100 + "%";
}
window.addEventListener("load", setScalingFactor);
window.addEventListener("resize", setScalingFactor);

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <ChakraProvider theme={theme}>
      <App />
    </ChakraProvider>
  </React.StrictMode>,
);
