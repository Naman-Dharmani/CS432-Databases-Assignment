import { Outlet } from "react-router-dom";

async function action({ request }) {
  switch (request.method) {
    case "PUT": {
      console.log("update request sent");
      break;
    }
    case "DELETE": {
      const reqData = await request.json();
      console.log(reqData);
      return fetch(`${import.meta.env.VITE_URL}/product/${reqData.id}`, {
        method: "DELETE",
      });
    }
  }

  return { ok: true };
}

export default function ProductInfo({ params }) {
  return <Outlet />;
}

ProductInfo.action = action;
