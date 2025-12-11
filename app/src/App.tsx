import AppRouter from "@/pages/AppRouter"
import { useTelegramScript } from "@/hooks/useTelegramScript";
import Loader from "./components/Loader";

function App() {
  const tgReady = useTelegramScript();

  if (!tgReady) 
    return <Loader />;
  return <AppRouter />

}

export default App
