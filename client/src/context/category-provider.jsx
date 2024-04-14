import { createContext, useContext, useEffect, useState } from "react";

const initialState = {
  categories: {},
  subcategories: {},
};

const CategoryDataProviderContext = createContext(initialState);

export default function CategoryDataProvider({ children, ...props }) {
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
    <CategoryDataProviderContext.Provider value={categoryData} {...props}>
      {children}
    </CategoryDataProviderContext.Provider>
  );
}

export const useCategoryData = () => {
  const context = useContext(CategoryDataProviderContext);

  if (context === undefined)
    throw new Error(
      "useCategoryData must be used within a CategoryDataProvider",
    );

  return context;
};
