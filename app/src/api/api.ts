import axios, { type AxiosInstance } from "axios";

const API_URL = import.meta.env.VITE_API_URL;

const api: AxiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export default api