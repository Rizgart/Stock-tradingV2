import { AppShell, Group, Text, Title } from "@mantine/core";
import { useTranslation } from "react-i18next";
import { ColorSchemeToggle } from "@/shared/components/ColorSchemeToggle";

export default function App() {
  const { t } = useTranslation();

  return (
    <AppShell
      header={{ height: 60 }}
      padding="md"
      withBorder={false}
      transitionDuration={0}
    >
      <AppShell.Header>
        <Group h="100%" px="md" justify="space-between">
          <Title order={3}>{t("app.title")}</Title>
          <ColorSchemeToggle />
        </Group>
      </AppShell.Header>
      <AppShell.Main>
        <Group align="flex-start" gap="xl">
          <Text fw={500}>{t("app.welcome")}</Text>
          <Text c="dimmed" size="sm">
            {t("app.placeholder")}
          </Text>
        </Group>
      </AppShell.Main>
    </AppShell>
  );
}
