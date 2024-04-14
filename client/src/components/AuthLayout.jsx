import { Navigate, Outlet } from "react-router-dom";

import { useAuthContext } from "@/context/auth-provider";

export default function Root() {
  const { authUser } = useAuthContext();

  if (!authUser) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
}
