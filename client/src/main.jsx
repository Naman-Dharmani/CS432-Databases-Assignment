import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

import { GoogleOAuthProvider } from "@react-oauth/google";
import AuthProvider from "@/context/auth-provider";
import ThemeProvider from "@/components/theme-provider";
import CategoryDataProvider from "@/context/category-provider";

import ErrorPage from "@/components/error-page";
import Root from "@/components/Root";
import AuthLayout from "@/components/AuthLayout";
import ProductLayout from "@/components/ProductLayout";
import Home from "@/routes/Home";
import LoginForm from "@/routes/Login";
import Logout from "./routes/Logout";
import ProductList from "@/routes/ProductList.jsx";
import AddProduct from "@/routes/AddProduct";
import ProductInfo from "@/routes/ProductInfo";
import EditProduct from "@/routes/EditProduct";
import Transactions from "@/routes/Transactions";
import Settings from "@/routes/Settings.jsx";
import "./index.css";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    errorElement: <ErrorPage />,
    children: [
      {
        path: "/login",
        action: LoginForm.action,
        element: <LoginForm />,
      },
      {
        path: "/logout",
        element: <Logout />,
      },
      {
        element: <AuthLayout />,
        children: [
          {
            index: true,
            loader: Home.loader,
            element: <Home />,
          },
          {
            path: "/products",
            loader: ProductList.loader,
            element: <ProductList />,
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
              {
                index: true,
                loader: ProductInfo.loader,
                element: <ProductInfo />,
              },
              {
                path: "/product/:prod_id/edit",
                loader: EditProduct.loader,
                action: EditProduct.action,
                element: <EditProduct />,
              },
            ],
          },
          {
            path: "/transactions",
            loader: Transactions.loader,
            action: Transactions.action,
            element: <Transactions />,
          },
          {
            path: "/settings",
            loader: Settings.loader,
            action: Settings.action,
            element: <Settings />,
          },
        ],
      },
    ],
  },
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <GoogleOAuthProvider clientId="398750733330-4lmmbnofvkrfgarvk2qn6sdoiqid4dbe.apps.googleusercontent.com">
      <AuthProvider>
        <ThemeProvider defaultTheme="dark" storageKey="portal-ui-theme">
          <CategoryDataProvider>
            <RouterProvider router={router} />
          </CategoryDataProvider>
        </ThemeProvider>
      </AuthProvider>
    </GoogleOAuthProvider>
  </React.StrictMode>,
);
