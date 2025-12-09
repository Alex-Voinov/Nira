/* eslint-disable @typescript-eslint/no-namespace */

declare namespace TelegramWebApp {
  interface User {
    id: number;
    is_bot?: boolean;
    first_name: string;
    last_name?: string;
    username?: string;
    language_code?: string;
    photo_url?: string;
  }

  interface ThemeParams {
    bg_color?: string;
    text_color?: string;
    hint_color?: string;
    link_color?: string;
    button_color?: string;
    button_text_color?: string;
    secondary_bg_color?: string;
  }

  interface WebApp {
    initData: string;
    initDataUnsafe: {
      user?: User;
    };
    themeParams: ThemeParams;

    ready(): void;
    expand(): void;
  }
}

interface Window {
  Telegram?: {
    WebApp: TelegramWebApp.WebApp;
  };
}