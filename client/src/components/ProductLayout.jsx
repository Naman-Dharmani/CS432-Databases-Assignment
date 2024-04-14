import { Outlet } from "react-router-dom";

async function action({ request }) {
  switch (request.method) {
    case "DELETE": {
      const reqData = await request.json();
      return fetch(`${import.meta.env.VITE_URL}/product/${reqData.id}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("bs_jwt")}`,
        },
      });
    }
  }

  return { ok: true };
}

export default function ProductLayout() {
  return <Outlet />;
}

ProductLayout.action = action;
