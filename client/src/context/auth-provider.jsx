import { createContext, useContext, useState } from "react";

const initialState = {
  authUser: localStorage.getItem("bs_jwt"),
  setAuthUser: () => {},
};

const AuthProviderContext = createContext(initialState);

export default function AuthProvider({ children, ...props }) {
  const [authUser, setAuthUser] = useState(initialState.authUser);

  return (
    <AuthProviderContext.Provider value={{ authUser, setAuthUser }} {...props}>
      {children}
    </AuthProviderContext.Provider>
  );
}

export const useAuthContext = () => {
  const context = useContext(AuthProviderContext);

  if (context === undefined)
    throw new Error("useAuthContext must be used within a AuthProvider");

  return context;
};
