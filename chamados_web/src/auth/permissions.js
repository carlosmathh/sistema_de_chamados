export function isClient(user) {
  return user?.role === "client";
}

export function isSupport(user) {
  return user?.role === "support";
}

export function isJuniorOrMid(user) {
  return isSupport(user) && ["junior", "mid_level"].includes(user?.position_team);
}

export function isSeniorOrEngineer(user) {
  return isSupport(user) && ["senior", "engineer"].includes(user?.position_team);
}
