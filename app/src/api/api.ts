import axios, { type AxiosInstance } from "axios";
import userService from "@/services/userService";

const api: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  withCredentials: true,
});

api.interceptors.request.use((config) => {
  const initData = userService.getInitData();

  if (initData) {
    config.headers["x-telegram-init-data"] = initData;
  }

  return config;
});

export default api