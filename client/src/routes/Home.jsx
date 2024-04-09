import { Link, useLoaderData } from "react-router-dom";
import { HeartIcon } from "lucide-react";
import { Badge } from "@/components/ui/badge";

import { useCategoryData } from "@/context/category-provider";

async function loader({ request }) {
  const url = new URL(request.url);
  const page_num = url.searchParams.get("page");

  return fetch(`${import.meta.env.VITE_URL}/products?page=${page_num || 1}`);
}

export default function Home() {
  const data = useLoaderData();
  const categoryData = useCategoryData();

  return (
    <div className="bg-background">
      <div className="grid lg:grid-cols-5">
        <div className="hidden pb-12 lg:block">
          <div className="space-y-4 py-4">
            <div className="px-3 py-2">
              <h2 className="mb-2 px-4 text-lg font-semibold tracking-tight">
                Discover
              </h2>
              <div className="space-y-1">
                <button className="inline-flex h-9 w-full items-center justify-start whitespace-nowrap rounded-md bg-secondary px-4 py-2 text-sm font-medium text-secondary-foreground shadow-sm transition-colors hover:bg-secondary/80 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50">
                  <svg
                    className="mr-2 h-4 w-4"
                    fill="none"
                    stroke="currentColor"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <circle cx="12" cy="12" r="10" />
                    <polygon points="10 8 16 12 10 16 10 8" />
                  </svg>
                  Trending
                </button>
                <button className="inline-flex h-9 w-full items-center justify-start whitespace-nowrap rounded-md px-4 py-2 text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50">
                  <svg
                    className="mr-2 h-4 w-4"
                    fill="none"
                    stroke="currentColor"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <rect height="7" rx="1" width="7" x="3" y="3" />
                    <rect height="7" rx="1" width="7" x="14" y="3" />
                    <rect height="7" rx="1" width="7" x="14" y="14" />
                    <rect height="7" rx="1" width="7" x="3" y="14" />
                  </svg>
                  Browse
                </button>
                <button className="inline-flex h-9 w-full items-center justify-start whitespace-nowrap rounded-md px-4 py-2 text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50">
                  <HeartIcon className="mr-2 h-4 w-4" />
                  Interested
                </button>
              </div>
            </div>
            <div className="px-3 py-2">
              <h2 className="mb-2 px-4 text-lg font-semibold tracking-tight">
                Categories
              </h2>
              <div className="space-y-1">
                {categoryData.categories?.map((category) => (
                  <button
                    key={category.category_id}
                    className="inline-flex h-9 w-full items-center justify-start whitespace-nowrap rounded-md px-4 py-2 text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50"
                  >
                    {category.category_name}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
        <div className="col-span-3 lg:col-span-4 lg:border-l">
          <div className="h-full px-4 py-6 lg:px-8">
            <div
              className="h-full space-y-6"
              data-orientation="horizontal"
              dir="ltr"
            >
              <div
                aria-labelledby="radix-:r1cv:-trigger-music"
                className="mt-2 border-none p-0 outline-none ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                data-orientation="horizontal"
                data-state="active"
                id="radix-:r1cv:-content-music"
                role="tabpanel"
                style={{
                  animationDuration: "0s",
                }}
                tabIndex="0"
              >
                <div className="flex items-center justify-between">
                  <div className="space-y-1">
                    <h2 className="text-2xl font-semibold tracking-tight">
                      Listen Now
                    </h2>
                    <p className="text-sm text-muted-foreground">
                      Top picks for you.
                    </p>
                  </div>
                </div>
                <div
                  className="my-4 h-[1px] w-full shrink-0 bg-border"
                  data-orientation="horizontal"
                  role="none"
                />
                <div className="relative">
                  <div
                    className="relative overflow-hidden"
                    dir="ltr"
                    style={{
                      "--radix-scroll-area-corner-height": "0px",
                      "--radix-scroll-area-corner-width": "0px",
                      position: "relative",
                    }}
                  >
                    <style
                      dangerouslySetInnerHTML={{
                        __html:
                          "[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}",
                      }}
                    />
                    <div
                      className="h-full w-full rounded-[inherit]"
                      data-radix-scroll-area-viewport=""
                      style={{
                        overflow: "scroll",
                      }}
                    >
                      <div
                        style={{
                          display: "table",
                          minWidth: "100%",
                        }}
                      >
                        <div className="flex space-x-4 pb-4">
                          {data.products
                            .filter((product) => product.status === "Available")
                            .map((product) => (
                              <div
                                className="w-[250px] space-y-3"
                                key={product.prod_id}
                              >
                                <span data-state="closed">
                                  <div className="overflow-hidden rounded-md">
                                    <Link to={`/product/${product.prod_id}`}>
                                      <img
                                        alt={
                                          product.product_images[0]
                                            .image_caption
                                        }
                                        className="aspect-[3/4] h-auto w-auto object-cover transition-all hover:scale-105"
                                        height="330"
                                        src={
                                          product.product_images[0]
                                            ?.image_url || "./placeholder.svg"
                                        }
                                        style={{
                                          color: "transparent",
                                        }}
                                        width="250"
                                      />
                                    </Link>
                                  </div>
                                </span>
                                <div className="space-y-1 text-sm">
                                  <h3 className="font-medium leading-none">
                                    {product.prod_title}
                                    <Badge
                                      variant="outline"
                                      className="float-right"
                                    >
                                      {product.prod_condition}
                                    </Badge>
                                  </h3>
                                  <p className="text-xs text-muted-foreground">
                                    {product.description.slice(0, 25) + "..."}
                                  </p>
                                  <p className="mt-2 text-base">
                                    ₹{product.listed_price}
                                  </p>
                                </div>
                              </div>
                            ))}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div className="mt-6 space-y-1">
                  <h2 className="text-2xl font-semibold tracking-tight">
                    Made for You
                  </h2>
                  <p className="text-sm text-muted-foreground">
                    Your personal interests.
                  </p>
                </div>
                <div
                  className="my-4 h-[1px] w-full shrink-0 bg-border"
                  data-orientation="horizontal"
                  role="none"
                />
                <div className="relative">
                  <div
                    className="relative overflow-hidden"
                    dir="ltr"
                    style={{
                      "--radix-scroll-area-corner-height": "0px",
                      "--radix-scroll-area-corner-width": "0px",
                      position: "relative",
                    }}
                  >
                    <style
                      dangerouslySetInnerHTML={{
                        __html:
                          "[data-radix-scroll-area-viewport]{scrollbar-width:none;-ms-overflow-style:none;-webkit-overflow-scrolling:touch;}[data-radix-scroll-area-viewport]::-webkit-scrollbar{display:none}",
                      }}
                    />
                    <div
                      className="h-full w-full rounded-[inherit]"
                      data-radix-scroll-area-viewport=""
                      style={{
                        overflow: "scroll",
                      }}
                    >
                      <div
                        style={{
                          display: "table",
                          minWidth: "100%",
                        }}
                      >
                        <div className="flex space-x-4 pb-4">
                          <div className="w-[150px] space-y-3">
                            <span data-state="closed">
                              <div className="overflow-hidden rounded-md">
                                <img
                                  alt="Thinking Components"
                                  className="aspect-square h-auto w-auto object-cover transition-all hover:scale-105"
                                  height="150"
                                  width="150"
                                  src="/placeholder.svg"
                                  style={{
                                    color: "transparent",
                                  }}
                                />
                              </div>
                            </span>
                            <div className="space-y-1 text-sm">
                              <h3 className="font-medium leading-none">
                                Thinking Components
                              </h3>
                              <p className="text-xs text-muted-foreground">
                                Lena Logic
                              </p>
                            </div>
                          </div>
                          <div className="w-[150px] space-y-3">
                            <span data-state="closed">
                              <div className="overflow-hidden rounded-md">
                                <img
                                  alt="Functional Fury"
                                  className="aspect-square h-auto w-auto object-cover transition-all hover:scale-105"
                                  height="150"
                                  src="/placeholder.svg"
                                  style={{
                                    color: "transparent",
                                  }}
                                  width="150"
                                />
                              </div>
                            </span>
                            <div className="space-y-1 text-sm">
                              <h3 className="font-medium leading-none">
                                Functional Fury
                              </h3>
                              <p className="text-xs text-muted-foreground">
                                Beth Binary
                              </p>
                            </div>
                          </div>
                          <div className="w-[150px] space-y-3">
                            <span data-state="closed">
                              <div className="overflow-hidden rounded-md">
                                <img
                                  alt="React Rendezvous"
                                  className="aspect-square h-auto w-auto object-cover transition-all hover:scale-105"
                                  data-nimg="1"
                                  decoding="async"
                                  height="150"
                                  loading="lazy"
                                  src="/placeholder.svg"
                                  style={{
                                    color: "transparent",
                                  }}
                                  width="150"
                                />
                              </div>
                            </span>
                            <div className="space-y-1 text-sm">
                              <h3 className="font-medium leading-none">
                                React Rendezvous
                              </h3>
                              <p className="text-xs text-muted-foreground">
                                Ethan Byte
                              </p>
                            </div>
                          </div>
                          <div className="w-[150px] space-y-3">
                            <span data-state="closed">
                              <div className="overflow-hidden rounded-md">
                                <img
                                  alt="Stateful Symphony"
                                  className="aspect-square h-auto w-auto object-cover transition-all hover:scale-105"
                                  data-nimg="1"
                                  decoding="async"
                                  height="150"
                                  loading="lazy"
                                  src="/placeholder.svg"
                                  style={{
                                    color: "transparent",
                                  }}
                                  width="150"
                                />
                              </div>
                            </span>
                            <div className="space-y-1 text-sm">
                              <h3 className="font-medium leading-none">
                                Stateful Symphony
                              </h3>
                              <p className="text-xs text-muted-foreground">
                                Beth Binary
                              </p>
                            </div>
                          </div>
                          <div className="w-[150px] space-y-3">
                            <span data-state="closed">
                              <div className="overflow-hidden rounded-md">
                                <img
                                  alt="Async Awakenings"
                                  className="aspect-square h-auto w-auto object-cover transition-all hover:scale-105"
                                  data-nimg="1"
                                  decoding="async"
                                  height="150"
                                  loading="lazy"
                                  src="/placeholder.svg"
                                  style={{
                                    color: "transparent",
                                  }}
                                  width="150"
                                />
                              </div>
                            </span>
                            <div className="space-y-1 text-sm">
                              <h3 className="font-medium leading-none">
                                Async Awakenings
                              </h3>
                              <p className="text-xs text-muted-foreground">
                                Nina Netcode
                              </p>
                            </div>
                          </div>
                          <div className="w-[150px] space-y-3">
                            <span data-state="closed">
                              <div className="overflow-hidden rounded-md">
                                <img
                                  alt="The Art of Reusability"
                                  className="aspect-square h-auto w-auto object-cover transition-all hover:scale-105"
                                  height="150"
                                  src="/placeholder.svg"
                                  style={{
                                    color: "transparent",
                                  }}
                                  width="150"
                                />
                              </div>
                            </span>
                            <div className="space-y-1 text-sm">
                              <h3 className="font-medium leading-none">
                                The Art of Reusability
                              </h3>
                              <p className="text-xs text-muted-foreground">
                                Lena Logic
                              </p>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div
                aria-labelledby="radix-:r1cv:-trigger-podcasts"
                className="mt-2 h-full flex-col border-none p-0 ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 data-[state=active]:flex"
                data-orientation="horizontal"
                data-state="inactive"
                hidden
                id="radix-:r1cv:-content-podcasts"
                role="tabpanel"
                tabIndex="0"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

Home.loader = loader;
