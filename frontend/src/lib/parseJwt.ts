export interface JwtPayload {
  username: string;
  role: string;
  exp: number;
}
export function parseJwt(token: string): JwtPayload {
  const base64Payload = token.split(".")[1];
  const payload = atob(base64Payload);
  console.log(payload);
  return JSON.parse(payload);
}

export const isTokenExpired = (exp: number) => {
  return Date.now() >= exp * 1000;
};