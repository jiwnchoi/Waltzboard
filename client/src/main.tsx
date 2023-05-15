import { ChakraProvider, extendTheme } from '@chakra-ui/react';
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

import '@fontsource/rajdhani';
import 'pretendard/dist/web/variable/pretendardvariable.css';

const theme = extendTheme({
  fonts: {
    heading: 'Pretendard',
    body: 'Pretendard',
  },
  styles: {
    global: {
      body: {
        bg: 'gray.50',
      },
    },
  },
  components: {
    Text: {
      variants: {
        layout: {
          color: 'gray.500',
        },
      },
    },
    Heading: {
      variants: {
        layout: {
          fontWeight: 900,
          color: 'gray.500',
        },
        section: {
          fontSize: 'sm',
          fontWeight: 700,
          color: 'gray.700',
        },
      },
    },
    Button: {
      variants: {
        layout: {
          color: 'gray.500',
          backgroundColor: 'transparent',
        },
      },
    },
    Link: {
      baseStyle: {
        _hover: {
          textDecoration: 'none',
        },
      },
    },
  },
});

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <ChakraProvider theme={theme}>
      <App />
    </ChakraProvider>
  </React.StrictMode>
);
