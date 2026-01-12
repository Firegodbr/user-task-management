import axios from "axios";
import { isTokenExpired, parseJwt } from "./parseJwt";

const api = axios.create({
  baseURL: "http://localhost:8000", // Change the baseURL to point to localhost directly
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    const payload = parseJwt(token);
    if (isTokenExpired(payload.exp)) {
      localStorage.removeItem("token");
      window.location.href = "/login";
      return Promise.reject(new Error("Token expired"));
    }
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // token expired or invalid
      localStorage.removeItem("token");
      window.location.href = "/login"; // or call logout()
    }
    return Promise.reject(error);
  }
);

export default api;
