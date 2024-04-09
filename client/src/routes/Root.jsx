import { json, Outlet } from "react-router-dom";

import Navbar from "@/components/Navbar";

async function logout() {
  // send the user id for logging out
  if (Math.random() < 0.5) {
    return json({ ok: true }, { status: 200 });
  } else {
    throw new Error("failed logging out!");
  }
}

export default function Root() {
  return (
    <div className="flex min-h-screen w-full flex-col">
      <Navbar isLoggedIn={true} />
      <main className="w-full">
        <Outlet />
      </main>
    </div>
  );
}

Root.action = logout;
