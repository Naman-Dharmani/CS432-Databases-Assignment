import { Outlet } from "react-router-dom";

import { useAuthContext } from "@/context/auth-provider";
import Navbar from "@/components/Navbar";

export default function Root() {
  const { authUser } = useAuthContext();

  return (
    <div className="flex min-h-screen w-full flex-col">
      <Navbar isLoggedIn={authUser ? true : false} />
      <main className="w-full">
        <Outlet />
      </main>
    </div>
  );
}
