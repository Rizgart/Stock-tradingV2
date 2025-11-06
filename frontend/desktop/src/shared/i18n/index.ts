import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import en from "@/assets/locales/en/translation.json";
import sv from "@/assets/locales/sv/translation.json";

void i18n
  .use(initReactI18next)
  .init({
    resources: {
      en: { translation: en },
      sv: { translation: sv },
    },
    lng: "sv",
    fallbackLng: "en",
    interpolation: {
      escapeValue: false,
    },
  });

export default i18n;
