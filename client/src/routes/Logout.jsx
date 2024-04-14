import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuthContext } from "@/context/auth-provider";

export default function Logout() {
  const navigate = useNavigate();
  const { setAuthUser } = useAuthContext();

  useEffect(() => {
    // remove the localStorage jwt
    localStorage.removeItem("bs_jwt");
    setAuthUser(null);
    navigate("/login");
  }, [navigate, setAuthUser]);

  return null;
}
