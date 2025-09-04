import { createContext, useEffect, useState, useContext } from "react";
import api from "../Controllers/api";

const AuthContext = createContext(null);

export function useAuth() {
  return useContext(AuthContext);
}

export function AuthProvider({ children }) {
  const [loggedUser, setLoggedUser] = useState(null);

  useEffect(() => {

    (async () => {
      try {
        const { data } = await api.get("/accounts/me");
        setLoggedUser(data);
      } catch {
        setLoggedUser(null);
      }
    })();

  }, []);

  return (<AuthContext.Provider value={{ loggedUser, setLoggedUser }}>
    {children}
    </AuthContext.Provider>
  );
}
