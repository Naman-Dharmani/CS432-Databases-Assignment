import { useEffect, useState } from "react";
import { json, Outlet } from "react-router-dom";

import Navbar from "@/components/Navbar";
import { CategoryDataContext } from "@/context/category";

async function logout() {
  // send the user id for logging out
  if (Math.random() < 0.5) {
    return json({ ok: true }, { status: 200 });
  } else {
    throw new Error("failed logging out!");
  }
}

export default function Root() {
  const [categoryData, setCategoryData] = useState({});

  useEffect(() => {
    async function fetchData() {
      const categories = await (
        await fetch(`${import.meta.env.VITE_URL}/categories`)
      ).json();

      const subcategories = await (
        await fetch(`${import.meta.env.VITE_URL}/subcategories`)
      ).json();

      setCategoryData({ categories, subcategories });
    }
    fetchData();
  }, []);

  return (
    <CategoryDataContext.Provider value={categoryData}>
      <div className="flex min-h-screen w-full flex-col">
        <Navbar isLoggedIn={true} />
        <main className="w-full">
          <Outlet />
        </main>
      </div>
    </CategoryDataContext.Provider>
  );
}

Root.action = logout;
