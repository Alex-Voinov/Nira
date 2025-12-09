import api from "@/api/api";
import userStore from "@/stores/userStore";
import type { IUser } from "@/types/user";

class UserService {

    initFromTelegram() {
        if (!window.Telegram?.WebApp) return;

        const tg = window.Telegram.WebApp;
        tg.ready();

        userStore.setInitData(tg.initData);
        userStore.setTelegramUser(tg.initDataUnsafe?.user || null);
    }

    async register(userData: IUser) {
        const response = await api.post("/registration", userData);
        userStore.setBackendUser(response.data);
        return response.data;
    }
}

export default new UserService();