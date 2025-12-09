import { useEffect, useState } from "react";
import userService from "@/services/userService";

export const useTelegramScript = () => {
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    if (document.getElementById("telegram-web-app")) return;

    const script = document.createElement("script");
    script.id = "telegram-web-app";
    script.src = "https://telegram.org/js/telegram-web-app.js";
    script.async = true;
    script.onload = () => {
      console.log("Telegram Web App script loaded");

      // Инициализация сервиса после загрузки скрипта
      userService.initFromTelegram();

      setLoaded(true); // ставим флаг, что TG готов
    };
    document.body.appendChild(script);

    return () => {
      document.body.removeChild(script);
    };
  }, []);

  return loaded;
};
