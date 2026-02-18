// chamados_web/src/auth/auth.js
const TOKEN_KEY = "token";

export function getToken() {
  return localStorage.getItem(TOKEN_KEY) || "";
}

export function setToken(token) {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
}

export function getUserFromToken(tokenArg) {
  const token = tokenArg || getToken();
  if (!token) return null;

  try {
    // JWT = header.payload.signature
    const payload = token.split(".")[1];
    const json = JSON.parse(atob(payload.replace(/-/g, "+").replace(/_/g, "/")));
    return json; // { role, user_id, position_team, exp, ... }
  } catch {
    return null;
  }
}
