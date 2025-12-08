import api from "@/api/api";
import { type IUser } from "@/types/user";

class UserService {

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
