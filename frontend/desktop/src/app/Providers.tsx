import { PropsWithChildren } from "react";
import { Provider as ReduxProvider } from "react-redux";
import {
  MantineProvider,
  ColorSchemeScript,
  createTheme,
} from "@mantine/core";
import { Notifications } from "@mantine/notifications";
import { store } from "./store";

const theme = createTheme({
  fontFamily: "'Inter', sans-serif",
  headings: { fontFamily: "'Inter', sans-serif" },
});

export function Providers({ children }: PropsWithChildren) {
  return (
    <ReduxProvider store={store}>
      <ColorSchemeScript defaultColorScheme="dark" />
      <MantineProvider theme={theme} defaultColorScheme="dark" withCssVariables>
        <Notifications position="top-right" />
        {children}
      </MantineProvider>
    </ReduxProvider>
  );
}
