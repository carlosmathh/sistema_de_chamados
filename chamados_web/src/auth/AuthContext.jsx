import { createContext, useContext, useMemo, useState } from "react";
import { clearToken, getToken, getUserFromToken, setToken } from "./auth";

const AuthContext = createContext(null);



export function AuthProvider({ children }) {

  
  const [token, setTokenState] = useState(getToken());
  const [user, setUser] = useState(getUserFromToken());

  const value = useMemo(() => {
    return {
      token,
      user,
      isAuthed: Boolean(token),
        loginWithToken: (newToken) => {
          setToken(newToken);
          setTokenState(newToken);
          setUser(getUserFromToken(newToken));
        },

      logout: () => {
        clearToken();
        setTokenState("");
        setUser(null);
      },
    };
  }, [token, user]);

  

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}

