import type { IUser } from "@/types/user";
import { makeAutoObservable } from "mobx";

class UserStore {
    telegramUser: TelegramWebApp.User | null = null;
    telegramInitData: string | null = null;
    backendUser: IUser | null = null;

    constructor() {
        makeAutoObservable(this);
    }

    setTelegramUser(user: TelegramWebApp.User | null) {
        this.telegramUser = user;
    }

    setInitData(data: string | null) {
        this.telegramInitData = data;
    }

    setBackendUser(user: IUser) {
        this.backendUser = user;
    }

    get isAuthorized() {
        return !!this.backendUser;
    }
}

export default new UserStore();
