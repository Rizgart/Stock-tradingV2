import React from "react";
import ReactDOM from "react-dom/client";
import App from "@/app/App";
import { Providers } from "@/app/Providers";
import "@/shared/i18n";

const rootElement = document.getElementById("root");

if (!rootElement) {
  throw new Error("Root element with id 'root' was not found");
}

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <Providers>
      <App />
    </Providers>
  </React.StrictMode>
);
