import { Link, useFetcher, useLoaderData, useNavigate } from "react-router-dom";
import moment from "moment";
import {
  ChevronLeft,
  ChevronRight,
  File,
  Home,
  LineChart,
  ListFilter,
  MoreHorizontal,
  Package,
  Package2,
  PanelLeft,
  PlusCircle,
  Search,
  Settings,
  ShoppingCart,
  Users2,
} from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Input } from "@/components/ui/input";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";

async function loader({ request }) {
  const url = new URL(request.url);
  const page_num = url.searchParams.get("page");

  return fetch(`${import.meta.env.VITE_URL}/products?page=${page_num || 1}`);
}

export default function ProductList() {
  const data = useLoaderData();
  const navigate = useNavigate();
  const fetcher = useFetcher();

  const activeProducts = data.products
    .filter((product) => product.status === "Available")
    .map((product) => (
      <TableRow key={product.prod_id}>
        <TableCell className="hidden sm:table-cell">
          <img
            alt={product.product_images[0]?.image_caption}
            className="aspect-square rounded-md object-contain"
            height="64"
            src={product.product_images[0]?.image_url || "/placeholder.svg"}
            width="64"
          />
        </TableCell>
        <TableCell className="font-medium">{product.prod_title}</TableCell>
        <TableCell className="hidden md:table-cell">
          {product.subcategory.subcategory_name}
        </TableCell>
        <TableCell>
          <Badge variant="outline">{product.status}</Badge>
        </TableCell>
        <TableCell className="hidden md:table-cell">
          {product.listed_price}
        </TableCell>
        <TableCell className="hidden md:table-cell">
          {product.quantity}
        </TableCell>
        <TableCell className="hidden  md:table-cell">
          {moment(product.date_listed).format("YYYY-MM-DD hh:mm A")}
        </TableCell>
        <TableCell>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button aria-haspopup="true" size="icon" variant="ghost">
                <MoreHorizontal className="h-4 w-4" />
                <span className="sr-only">Toggle menu</span>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuLabel>Actions</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem
                onClick={() => navigate(`/product/${product.prod_id}/edit`)}
              >
                Edit
              </DropdownMenuItem>
              <DropdownMenuItem
                onClick={() => {
                  fetcher.submit(
                    { id: product.prod_id },
                    {
                      method: "DELETE",
                      action: `/product/${product.prod_id}`,
                      encType: "application/json",
                    },
                  );
                }}
              >
                Delete
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </TableCell>
      </TableRow>
    ));

  const soldProducts = data.products
    .filter((product) => product.status === "Sold")
    .map((product) => (
      <TableRow key={product.prod_id}>
        <TableCell className="hidden sm:table-cell">
          <img
            alt={product.product_images[0]?.image_caption}
            className="aspect-square rounded-md object-contain"
            height="64"
            src={product.product_images[0]?.image_url || "/placeholder.svg"}
            width="64"
          />
        </TableCell>
        <TableCell className="font-medium">{product.prod_title}</TableCell>
        <TableCell className="hidden md:table-cell">
          {product.subcategory.subcategory_name}
        </TableCell>
        <TableCell>
          <Badge variant="outline">{product.status}</Badge>
        </TableCell>
        <TableCell className="hidden md:table-cell">
          {product.listed_price}
        </TableCell>
        <TableCell className="hidden md:table-cell">
          {product.quantity}
        </TableCell>
        <TableCell className="hidden  md:table-cell">
          {moment(product.date_listed).format("YYYY-MM-DD hh:mm A")}
        </TableCell>
        <TableCell>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button aria-haspopup="true" size="icon" variant="ghost">
                <MoreHorizontal className="h-4 w-4" />
                <span className="sr-only">Toggle menu</span>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuLabel>Actions</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem
                onClick={() => navigate(`/product/${product.prod_id}/edit`)}
              >
                Edit
              </DropdownMenuItem>
              <DropdownMenuItem
                onClick={() => {
                  fetcher.submit(
                    { id: product.prod_id },
                    {
                      method: "DELETE",
                      action: `/product/${product.prod_id}`,
                      encType: "application/json",
                    },
                  );
                }}
              >
                Delete
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </TableCell>
      </TableRow>
    ));

  const archivedProducts = data.products
    .filter((product) => product.status === "Archived")
    .map((product) => (
      <TableRow key={product.prod_id}>
        <TableCell className="hidden sm:table-cell">
          <img
            alt={product.product_images[0]?.image_caption}
            className="aspect-square rounded-md object-contain"
            height="64"
            src={product.product_images[0]?.image_url || "/placeholder.svg"}
            width="64"
          />
        </TableCell>
        <TableCell className="font-medium">{product.prod_title}</TableCell>
        <TableCell className="hidden md:table-cell">
          {product.subcategory.subcategory_name}
        </TableCell>
        <TableCell>
          <Badge variant="outline">{product.status}</Badge>
        </TableCell>
        <TableCell className="hidden md:table-cell">
          {product.listed_price}
        </TableCell>
        <TableCell className="hidden md:table-cell">
          {product.quantity}
        </TableCell>
        <TableCell className="hidden  md:table-cell">
          {moment(product.date_listed).format("YYYY-MM-DD hh:mm A")}
        </TableCell>
        <TableCell>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button aria-haspopup="true" size="icon" variant="ghost">
                <MoreHorizontal className="h-4 w-4" />
                <span className="sr-only">Toggle menu</span>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuLabel>Actions</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem
                onClick={() => navigate(`/product/${product.prod_id}/edit`)}
              >
                Edit
              </DropdownMenuItem>
              <DropdownMenuItem
                onClick={() => {
                  fetcher.submit(
                    { id: product.prod_id },
                    {
                      method: "DELETE",
                      action: `/product/${product.prod_id}`,
                      encType: "application/json",
                    },
                  );
                }}
              >
                Delete
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </TableCell>
      </TableRow>
    ));

  const page_info = {
    start: (data?.page_num - 1) * data?.per_page + 1,
    end: Math.min(data?.total, data?.page_num * data?.per_page),
  };

  return (
    <div className="flex min-h-screen w-full flex-col bg-muted/40">
      <div className="flex flex-col sm:gap-4 sm:px-7 sm:py-4">
        <div className="grid flex-1 items-start gap-4 p-4 sm:px-6 sm:py-0 md:gap-8">
          <Tabs defaultValue="all">
            <div className="flex items-center">
              <TabsList>
                <TabsTrigger value="all">All</TabsTrigger>
                <TabsTrigger value="active">Active</TabsTrigger>
                <TabsTrigger value="sold" className="hidden sm:flex">
                  Sold
                </TabsTrigger>
                <TabsTrigger value="archived" className="hidden sm:flex">
                  Archived
                </TabsTrigger>
              </TabsList>
              <div className="ml-auto flex items-center gap-2">
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="outline" size="sm" className="h-8 gap-1">
                      <ListFilter className="h-3.5 w-3.5" />
                      <span className="sr-only sm:not-sr-only sm:whitespace-nowrap">
                        Filter
                      </span>
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuLabel>Filter by</DropdownMenuLabel>
                    <DropdownMenuSeparator />
                    <DropdownMenuCheckboxItem checked>
                      Active
                    </DropdownMenuCheckboxItem>
                    <DropdownMenuCheckboxItem>
                      Archived
                    </DropdownMenuCheckboxItem>
                  </DropdownMenuContent>
                </DropdownMenu>
                <Button size="sm" variant="outline" className="h-8 gap-1">
                  <File className="h-3.5 w-3.5" />
                  <span className="sr-only sm:not-sr-only sm:whitespace-nowrap">
                    Export
                  </span>
                </Button>
                <Button
                  size="sm"
                  className="h-8 gap-1"
                  onClick={() => navigate("/product/new")}
                >
                  <PlusCircle className="h-3.5 w-3.5" />
                  <span className="sr-only sm:not-sr-only sm:whitespace-nowrap">
                    Add Product
                  </span>
                </Button>
              </div>
            </div>
            <TabsContent value="all">
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle>Products</CardTitle>
                    <div className="flex gap-3">
                      <Button
                        variant="outline"
                        size="icon"
                        className="h-9 w-9"
                        onClick={() =>
                          navigate(`/products?page=${data?.page_num - 1}`)
                        }
                        disabled={!data?.has_prev}
                      >
                        <ChevronLeft className="h-5 w-5" />
                        <span className="sr-only">Previous Page</span>
                      </Button>
                      <Button
                        variant="outline"
                        size="icon"
                        className="h-9 w-9"
                        onClick={() =>
                          navigate(`/products?page=${data?.page_num + 1}`)
                        }
                        disabled={!data?.has_next}
                      >
                        <ChevronRight className="h-5 w-5" />
                        <span className="sr-only">Next Page</span>
                      </Button>
                    </div>
                  </div>
                  <CardDescription>
                    Manage your products and view their sales.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <Table className="text-center">
                    <TableHeader>
                      <TableRow>
                        <TableHead className="hidden w-[100px] sm:table-cell">
                          <span className="sr-only">Image</span>
                        </TableHead>
                        <TableHead className="text-center">Name</TableHead>
                        <TableHead className="text-center">
                          Subcategory
                        </TableHead>
                        <TableHead className="text-center">Status</TableHead>
                        <TableHead className="hidden text-center md:table-cell">
                          Price
                        </TableHead>
                        <TableHead className="hidden text-center md:table-cell">
                          Quantity
                        </TableHead>
                        <TableHead className="hidden text-center md:table-cell">
                          Created at
                        </TableHead>
                        <TableHead className="text-center">
                          <span className="sr-only">Actions</span>
                        </TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {data?.total > 0 &&
                        data.products.map((product) => (
                          <TableRow key={product.prod_id}>
                            <TableCell className="hidden sm:table-cell">
                              <img
                                alt={product.product_images[0]?.image_caption}
                                className="aspect-square rounded-md object-contain"
                                height="64"
                                src={
                                  product.product_images[0]?.image_url ||
                                  "/placeholder.svg"
                                }
                                width="64"
                              />
                            </TableCell>
                            <TableCell className="font-medium">
                              {product.prod_title}
                            </TableCell>
                            <TableCell className="hidden md:table-cell">
                              {product.subcategory.subcategory_name}
                            </TableCell>
                            <TableCell>
                              <Badge variant="outline">{product.status}</Badge>
                            </TableCell>
                            <TableCell className="hidden md:table-cell">
                              {product.listed_price}
                            </TableCell>
                            <TableCell className="hidden md:table-cell">
                              {product.quantity}
                            </TableCell>
                            <TableCell className="hidden  md:table-cell">
                              {moment(product.date_listed).format(
                                "YYYY-MM-DD hh:mm A",
                              )}
                            </TableCell>
                            <TableCell>
                              <DropdownMenu>
                                <DropdownMenuTrigger asChild>
                                  <Button
                                    aria-haspopup="true"
                                    size="icon"
                                    variant="ghost"
                                  >
                                    <MoreHorizontal className="h-4 w-4" />
                                    <span className="sr-only">Toggle menu</span>
                                  </Button>
                                </DropdownMenuTrigger>
                                <DropdownMenuContent align="end">
                                  <DropdownMenuLabel>Actions</DropdownMenuLabel>
                                  <DropdownMenuSeparator />
                                  <DropdownMenuItem
                                    onClick={() =>
                                      navigate(
                                        `/product/${product.prod_id}/edit`,
                                      )
                                    }
                                  >
                                    Edit
                                  </DropdownMenuItem>
                                  <DropdownMenuItem
                                    onClick={() => {
                                      fetcher.submit(
                                        { id: product.prod_id },
                                        {
                                          method: "DELETE",
                                          action: `/product/${product.prod_id}`,
                                          encType: "application/json",
                                        },
                                      );
                                    }}
                                  >
                                    Delete
                                  </DropdownMenuItem>
                                </DropdownMenuContent>
                              </DropdownMenu>
                            </TableCell>
                          </TableRow>
                        ))}
                    </TableBody>
                  </Table>
                </CardContent>
                <CardFooter>
                  <div className="text-xs text-muted-foreground">
                    {data?.total > 0 ? (
                      <>
                        Showing{" "}
                        <strong>
                          {page_info.start}-{page_info.end}
                        </strong>{" "}
                        of <strong>{data.total}</strong> products
                      </>
                    ) : (
                      <>No products found</>
                    )}
                  </div>
                </CardFooter>
              </Card>
            </TabsContent>
            <TabsContent value="active">
              <Card>
                <CardHeader>
                  <CardTitle>Active Products</CardTitle>
                  <CardDescription>
                    Manage your listed products.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <Table className="text-center">
                    <TableHeader>
                      <TableRow>
                        <TableHead className="hidden w-[100px] sm:table-cell">
                          <span className="sr-only">Image</span>
                        </TableHead>
                        <TableHead className="text-center">Name</TableHead>
                        <TableHead className="text-center">
                          Subcategory
                        </TableHead>
                        <TableHead className="text-center">Status</TableHead>
                        <TableHead className="hidden text-center md:table-cell">
                          Price
                        </TableHead>
                        <TableHead className="hidden text-center md:table-cell">
                          Quantity
                        </TableHead>
                        <TableHead className="hidden text-center md:table-cell">
                          Created at
                        </TableHead>
                        <TableHead className="text-center">
                          <span className="sr-only">Actions</span>
                        </TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>{activeProducts}</TableBody>
                  </Table>
                </CardContent>
                {activeProducts.length == 0 && (
                  <CardFooter>
                    <div className="text-xs text-muted-foreground">
                      No products found
                    </div>
                  </CardFooter>
                )}
              </Card>
            </TabsContent>
            <TabsContent value="sold">
              <Card>
                <CardHeader>
                  <CardTitle>Sold Products</CardTitle>
                  <CardDescription>
                    Manage your sold products and view their sales.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <Table className="text-center">
                    <TableHeader>
                      <TableRow>
                        <TableHead className="hidden w-[100px] sm:table-cell">
                          <span className="sr-only">Image</span>
                        </TableHead>
                        <TableHead className="text-center">Name</TableHead>
                        <TableHead className="text-center">
                          Subcategory
                        </TableHead>
                        <TableHead className="text-center">Status</TableHead>
                        <TableHead className="hidden text-center md:table-cell">
                          Price
                        </TableHead>
                        <TableHead className="hidden text-center md:table-cell">
                          Quantity
                        </TableHead>
                        <TableHead className="hidden text-center md:table-cell">
                          Created at
                        </TableHead>
                        <TableHead className="text-center">
                          <span className="sr-only">Actions</span>
                        </TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>{soldProducts}</TableBody>
                  </Table>
                </CardContent>
                {soldProducts.length == 0 && (
                  <CardFooter>
                    <div className="text-xs text-muted-foreground">
                      No products found
                    </div>
                  </CardFooter>
                )}
              </Card>
            </TabsContent>
            <TabsContent value="archived">
              <Card>
                <CardHeader>
                  <CardTitle>Archived Products</CardTitle>
                  <CardDescription>
                    Manage your archived products.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <Table className="text-center">
                    <TableHeader>
                      <TableRow>
                        <TableHead className="hidden w-[100px] sm:table-cell">
                          <span className="sr-only">Image</span>
                        </TableHead>
                        <TableHead className="text-center">Name</TableHead>
                        <TableHead className="text-center">
                          Subcategory
                        </TableHead>
                        <TableHead className="text-center">Status</TableHead>
                        <TableHead className="hidden text-center md:table-cell">
                          Price
                        </TableHead>
                        <TableHead className="hidden text-center md:table-cell">
                          Quantity
                        </TableHead>
                        <TableHead className="hidden text-center md:table-cell">
                          Created at
                        </TableHead>
                        <TableHead className="text-center">
                          <span className="sr-only">Actions</span>
                        </TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>{archivedProducts}</TableBody>
                  </Table>
                </CardContent>
                {archivedProducts.length == 0 && (
                  <CardFooter>
                    <div className="text-xs text-muted-foreground">
                      No products found
                    </div>
                  </CardFooter>
                )}
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  );
}

ProductList.loader = loader;
