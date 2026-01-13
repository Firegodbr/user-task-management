import { createContext, useContext, useEffect, useState } from "react";
import { parseJwt, isTokenExpired } from "../lib/parseJwt";
import type { JwtPayload } from "../lib/parseJwt";
import api from "../lib/api";

type AuthContextType = {
  jwtToken: JwtPayload | null;
  isAuthenticated: boolean;
  username: string | undefined;
  login: (token: string) => void;
  logout: () => Promise<void>;
  checkAuth: () => void;
};

const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [jwtToken, setJwtToken] = useState<JwtPayload | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Check if user is authenticated on mount
  const checkAuth = () => {
    // We can't read httpOnly cookies, but we can check if the access_token
    // response header was set by parsing the token returned from login
    // For now, we check localStorage for the parsed JWT payload (not the token itself)
    const storedPayload = localStorage.getItem("jwt_payload");
    if (!storedPayload) {
      setIsAuthenticated(false);
      setJwtToken(null);
      return;
    }

    try {
      const payload: JwtPayload = JSON.parse(storedPayload);
      if (isTokenExpired(payload.exp)) {
        localStorage.removeItem("jwt_payload");
        setIsAuthenticated(false);
        setJwtToken(null);
        return;
      }
      setJwtToken(payload);
      setIsAuthenticated(true);
    } catch {
      localStorage.removeItem("jwt_payload");
      setIsAuthenticated(false);
      setJwtToken(null);
    }
  };

  useEffect(() => {
    checkAuth();
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
        username: jwtToken?.sub,
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
