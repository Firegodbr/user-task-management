import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",  // Change the baseURL to point to localhost directly
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
