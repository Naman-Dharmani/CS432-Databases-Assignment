import React from "react";
import ReactDOM from "react-dom/client";
import {
  createBrowserRouter,
  RouterProvider,
  Navigate,
} from "react-router-dom";

import { ThemeProvider } from "@/components/theme-provider";
import CategoryDataProvider from "@/context/category-provider";

import ErrorPage from "@/error-page";
import Root from "@/routes/Root";
import Home from "@/routes/Home";
import LoginForm from "@/routes/Login";
import Transactions from "@/routes/Transactions";
import AddProduct from "@/routes/AddProduct";
import EditProduct from "@/routes/EditProduct";
import ProductLayout from "@/routes/ProductLayout";
import ProductInfo from "@/routes/ProductInfo";
import ProductList from "@/routes/ProductList.jsx";
import Settings from "@/routes/Settings.jsx";
import "./index.css";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    errorElement: <ErrorPage />,
    children: [
      {
        index: true,
        loader: Home.loader,
        element: <Home />,
      },
      {
        path: "/login",
        action: LoginForm.action,
        element: <LoginForm />,
      },
      {
        path: "/logout",
        action: Root.action,
        element: <Navigate to="/" replace={true} />,
      },
      {
        path: "/dashboard",
        element: <div>Dashboard</div>,
      },
      {
        path: "/product/new",
        action: AddProduct.action,
        element: <AddProduct />,
      },
      {
        path: "/product/:prod_id",
        action: ProductLayout.action,
        element: <ProductLayout />,
        children: [
          { index: true, loader: ProductInfo.loader, element: <ProductInfo /> },
          {
            path: "/product/:prod_id/edit",
            loader: EditProduct.loader,
            action: EditProduct.action,
            element: <EditProduct />,
          },
        ],
      },
      {
        path: "/products",
        loader: ProductList.loader,
        element: <ProductList />,
      },
      {
        path: "/transactions",
        loader: Transactions.loader,
        action: Transactions.action,
        element: <Transactions />,
      },
      {
        path: "/customers",
        element: <ProductList />,
      },
      {
        path: "/settings",
        loader: Settings.loader,
        action: Settings.action,
        element: <Settings />,
      },
    ],
  },
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <ThemeProvider defaultTheme="dark" storageKey="portal-ui-theme">
      <CategoryDataProvider>
        <RouterProvider router={router} />
      </CategoryDataProvider>
    </ThemeProvider>
  </React.StrictMode>,
);
