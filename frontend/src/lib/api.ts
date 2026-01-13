import axios, { AxiosError } from "axios";
import type { AxiosRequestConfig, InternalAxiosRequestConfig } from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
  withCredentials: true, // REQUIRED for cookies
});

/* ===============================
   CSRF Token Helper
================================ */

function getCsrfToken(): string | null {
  const match = document.cookie.match(/(?:^|;\s*)csrf_token=([^;]*)/);
  return match ? decodeURIComponent(match[1]) : null;
}

/* ===============================
   Request interceptor - Add CSRF
================================ */

api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // Add CSRF token for state-changing requests
    const csrfToken = getCsrfToken();
    if (csrfToken && ["post", "put", "patch", "delete"].includes(config.method?.toLowerCase() || "")) {
      config.headers.set("X-CSRF-Token", csrfToken);
    }
    return config;
  },
  (error) => Promise.reject(error)
);

/* ===============================
   Refresh coordination
================================ */

let isRefreshing = false;

type FailedRequest = {
  resolve: (value?: unknown) => void;
  reject: (error: unknown) => void;
};

let failedQueue: FailedRequest[] = [];

const processQueue = (error: unknown | null = null) => {
  failedQueue.forEach((p) => {
    if (error) p.reject(error);
    else p.resolve();
  });
  failedQueue = [];
};

/* ===============================
   Response interceptor
================================ */

api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as AxiosRequestConfig & {
      _retry?: boolean;
    };

    // Access token expired
    if (
      error.response?.status === 401 &&
      !originalRequest._retry &&
      !originalRequest.url?.includes("/auth/refresh")
    ) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        }).then(() => api(originalRequest));
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        // Refresh token is sent automatically via cookie
        // CSRF token is added by request interceptor
        await api.post("/auth/refresh");

        processQueue();
        return api(originalRequest);
      } catch (refreshError) {
        processQueue(refreshError);

        // Hard logout
        window.location.href = "/login";
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  }
);

export default api;
