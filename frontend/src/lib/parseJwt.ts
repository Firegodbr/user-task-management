export interface JwtPayload {
  sub: string; // username is stored in "sub" claim
  role: string;
  exp: number;
  iat: number;
  type: string;
}

export function parseJwt(token: string): JwtPayload {
  const base64Payload = token.split(".")[1];
  // Handle base64url encoding
  const base64 = base64Payload.replace(/-/g, "+").replace(/_/g, "/");
  const payload = atob(base64);
  return JSON.parse(payload);
}

export const isTokenExpired = (exp: number): boolean => {
  return Date.now() >= exp * 1000;
};