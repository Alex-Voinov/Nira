import AppRouter from "@/pages/AppRouter"
import { useTelegramScript } from "@/hooks/useTelegramScript";

function App() {
  const tgReady = useTelegramScript();

  if (!tgReady) {
    // Пока Telegram скрипт не загружен — показываем спиннер или пустой экран
    return <div>Загрузка Telegram...</div>;
  }
  return (
    <AppRouter />
  )
}

export default App
