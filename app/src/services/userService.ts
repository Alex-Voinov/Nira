import api from "@/api/api";
import { type IUser } from "@/types/user";

class UserService {

    private telegramInitData: string | null = null;
    private telegramUser: TelegramWebApp.User | null = null;

    initFromTelegram() {
        if (!window.Telegram?.WebApp) return;

        const tg = window.Telegram.WebApp;

        tg.ready();
        tg.expand();

        this.telegramInitData = tg.initData;
        this.telegramUser = tg.initDataUnsafe?.user || null;
    }

    getInitData() {
        return this.telegramInitData;
    }

    getTelegramUser() {
        return this.telegramUser;
    }

    async register(userData: IUser) {
        try {
            const response = await api.post("/registration", userData);
            return response.data;
        } catch (error) {
            throw error;
        }
    }

};

export default new UserService()
