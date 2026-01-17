import { createContext, useContext, useEffect, useState } from "react";
import { parseJwt } from "../lib/parseJwt";
import type { JwtPayload } from "../lib/parseJwt";
import api from "../lib/api";

type AuthContextType = {
  jwtToken: JwtPayload | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (token: string) => void;
  logout: () => Promise<void>;
  checkAuth: () => Promise<void>;
};

const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [jwtToken, setJwtToken] = useState<JwtPayload | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  // Check if user is authenticated by verifying with backend
  const checkAuth = async () => {
    setIsLoading(true);
    // First check if we have a stored payload
    const storedPayload = localStorage.getItem("jwt_payload");
    if (!storedPayload) {
      setIsAuthenticated(false);
      setJwtToken(null);
      setIsLoading(false);
      return;
    }

    try {
      // Verify authentication with backend - this will automatically
      // refresh the token if needed via the api interceptor
      const response = await api.get("/auth/me");

      if (response.status === 200) {
        // Backend confirms we're authenticated
        const payload: JwtPayload = JSON.parse(storedPayload);
        setJwtToken(payload);
        setIsAuthenticated(true);
      }
    } catch {
      // Authentication failed or token refresh failed
      localStorage.removeItem("jwt_payload");
      setIsAuthenticated(false);
      setJwtToken(null);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    checkAuth();

    // Listen for logout events from api interceptor
    const handleLogoutEvent = () => {
      localStorage.removeItem("jwt_payload");
      setJwtToken(null);
      setIsAuthenticated(false);
      window.location.href = "/login";
    };

    window.addEventListener("auth:logout", handleLogoutEvent);

    return () => {
      window.removeEventListener("auth:logout", handleLogoutEvent);
    };
  }, []);

  const login = (jwt: string) => {
    // Parse and store only the payload (for display purposes)
    // The actual token is stored in httpOnly cookie by the server
    const payload = parseJwt(jwt);
    localStorage.setItem("jwt_payload", JSON.stringify(payload));
    setJwtToken(payload);
    setIsAuthenticated(true);
  };

  const logout = async () => {
    try {
      await api.post("/auth/logout");
    } catch (error) {
      console.error("Logout error:", error);
    } finally {
      localStorage.removeItem("jwt_payload");
      setJwtToken(null);
      setIsAuthenticated(false);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        jwtToken,
        isAuthenticated,
        isLoading,
        login,
        logout,
        checkAuth,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside AuthProvider");
  return ctx;
};
