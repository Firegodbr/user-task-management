import { createContext, useContext, useEffect, useState } from "react";
import { parseJwt, isTokenExpired } from "../lib/parseJwt";
import type { JwtPayload } from "../lib/parseJwt";

type AuthContextType = {
  jwtToken: JwtPayload | null;
  token: string | null;
  username: string | undefined;
  login: (token: string) => void;
  logout: () => void;
};

const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [token, setToken] = useState<string | null>(null);
  const [jwtToken, setJwtToken] = useState<JwtPayload | null>(null);

  useEffect(() => {
    const storedToken = localStorage.getItem("token");
    if (!storedToken) return;
    const payload = parseJwt(storedToken);
    if (isTokenExpired(payload.exp)) {
      localStorage.removeItem("token");
      return;
    }
    if (storedToken) {
      setToken(storedToken);
      setJwtToken(parseJwt(storedToken));
    }
  }, []);

  const login = (jwt: string) => {
    localStorage.setItem("token", jwt);
    setToken(jwt);
    setJwtToken(parseJwt(jwt));
  };

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
    setJwtToken(null);
  };

  return (
    <AuthContext.Provider
      value={{ token, jwtToken, username: jwtToken?.username, login, logout }}
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
