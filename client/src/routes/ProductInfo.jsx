import { Form, useLoaderData } from "react-router-dom";

import { CircleX } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { useState } from "react";
import { HeartIcon } from "lucide-react";

async function loader({ params }) {
  return fetch(`${import.meta.env.VITE_URL}/product/${params.prod_id}`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("bs_jwt")}`,
    },
  });
}

export default function ProductInfo() {
  const data = useLoaderData();

  const [imageURL] = useState(
    data?.product_images[0]?.image_url || "/placeholder.svg",
  );

  return (
    <div className="flex min-h-screen w-full flex-col bg-muted/40">
      <div className="flex flex-col sm:gap-4 sm:py-4 sm:pl-14">
        <main className="grid flex-1 items-start gap-4 p-4 sm:px-6 sm:py-0 md:gap-8">
          {/* <Form method="post"> */}
          <div className="mx-auto grid max-w-[65rem] flex-1 auto-rows-max gap-4">
            <div className="flex items-center gap-4">
              {/* <Button
                  variant="outline"
                  size="icon"
                  className="h-7 w-7"
                  onClick={() => navigate(-1)}
                >
                  <ChevronLeft className="h-4 w-4" />
                  <span className="sr-only">Back</span>
                </Button> */}
              <h1 className="flex-1 shrink-0 whitespace-nowrap text-xl font-semibold tracking-tight sm:grow-0">
                Product Details
              </h1>
              {/* <Badge variant="outline" className="ml-auto sm:ml-0">
                  In stock
                </Badge> */}
              <div className="hidden items-center gap-2 md:ml-auto md:flex">
                {/* <Button
                    variant="outline"
                    size="sm"
                    onClick={() => navigate("/products", { replace: true })}
                    type="button"
                  >
                    Discard
                  </Button> */}
                <Button size="sm" type="submit">
                  <HeartIcon className="mr-2 h-4 w-4 fill-black" />
                  Interested
                </Button>
              </div>
            </div>
            <div className="grid gap-4 md:grid-cols-[1fr_250px] lg:grid-cols-3 lg:gap-8">
              <div className="grid auto-rows-max items-start gap-4 lg:col-span-2 lg:gap-8">
                <Card>
                  <CardHeader>
                    {/* <CardTitle>Product Details</CardTitle> */}
                  </CardHeader>
                  <CardContent>
                    <div className="grid gap-6">
                      <div className="grid gap-3">
                        <Label htmlFor="name">Title</Label>
                        <Input readOnly
                          id="name"
                          type="text"
                          className="w-full"
                          name="prod_title"
                          defaultValue={data?.prod_title}
                        />
                      </div>
                      <Card className="overflow-hidden">
                        <CardHeader>
                          <CardTitle>Product Images</CardTitle>
                        </CardHeader>
                        <CardContent>
                          <div className="grid gap-2">
                            {/* <div className="group relative"> */}
                            <img
                              alt={data?.product_images[0]?.image_caption}
                              className="aspect-square w-full rounded-md object-contain"
                              height="250"
                              width="250"
                              src={imageURL || "/placeholder.svg"}
                            />
                            {/* <button
                            size="icon"
                            className="absolute right-0 top-0 hidden -translate-y-1/2 translate-x-1/2 rounded-full bg-slate-800 p-0.5 group-hover:block dark:bg-slate-200"
                          >
                            <CircleX className="h-5 w-5 stroke-white dark:stroke-black" />
                          </button>
                        </div> */}
                            <div className="grid grid-cols-3 gap-2">
                              {data?.product_images.slice(1).map((image) => (
                                <div
                                  className="group relative"
                                  key={image.image_id}
                                >
                                  <img
                                    alt={image.image_caption}
                                    className="aspect-square w-full rounded-md object-cover"
                                    height="84"
                                    width="84"
                                    src={image.image_url}
                                  />
                                  <button
                                    size="icon"
                                    className="absolute right-0 top-0 hidden -translate-y-1/2 translate-x-1/2 rounded-full bg-slate-800 p-0.5 group-hover:block dark:bg-slate-200"
                                  >
                                    <CircleX className="h-5 w-5 stroke-white dark:stroke-black" />
                                  </button>
                                </div>
                              ))}
                              {/* <Dialog>
                            <DialogTrigger asChild>
                              <button className="flex aspect-square w-full items-center justify-center rounded-md border border-dashed">
                                <Upload className="h-4 w-4 text-muted-foreground" />
                                <span className="sr-only">Upload</span>
                              </button>
                            </DialogTrigger>
                            <DialogContent className="sm:max-w-lg">
                              <DialogHeader>
                                <DialogTitle>Edit URL</DialogTitle>
                                <DialogDescription>
                                  Make changes to your product image here. Click
                                  save when you are done.
                                </DialogDescription>
                              </DialogHeader>
                              <div className="grid gap-4 py-4">
                                <div className="grid grid-cols-4 items-center gap-4">
                                  <Label htmlFor="url" className="text-right">
                                    Image URL
                                  </Label>
                                  <Input readOnly
                                    id="url"
                                    value={imageURL}
                                    onChange={(e) =>
                                      setImageURL(e.target.value)
                                    }
                                    className="col-span-3"
                                  />
                                </div>
                              </div>
                              <DialogFooter>
                                <DialogClose asChild>
                                  <Button>Save changes</Button>
                                </DialogClose>
                              </DialogFooter>
                            </DialogContent>
                          </Dialog> */}
                            </div>
                          </div>
                        </CardContent>
                      </Card>
                      {/* <div className="flex gap-4">
                          <div className="grid flex-grow gap-3">
                            <Label htmlFor="listed_price">Listed Price</Label>
                            <Input readOnly
                              type="number"
                              id="listed_price"
                              name="listed_price"
                              min="0"
                              defaultValue={data?.listed_price}
                            />
                          </div>
                          <div className="grid flex-grow-0 gap-3">
                            <Label htmlFor="quantity">Quantity</Label>
                            <Input readOnly
                              type="number"
                              id="quantity"
                              name="quantity"
                              min="1"
                              defaultValue={data?.quantity}
                            />
                          </div>
                          <div className="hidden">
                            <Label htmlFor="image_url">Image URL</Label>
                            <Input readOnly id="image_url" name="image_url" readOnly />
                          </div>
                        </div> */}
                    </div>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader>
                    <CardTitle>Product Category</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid gap-6 sm:grid-cols-3">
                      <div className="grid gap-3">
                        <Label htmlFor="category">Category</Label>
                        {/* <Select
                            value={currentCategory}
                            onValueChange={(newCategory) => {
                              setCurrentCategory(newCategory);
                              setCurrentSubcategory(null);
                            }}
                          >
                            <SelectTrigger
                              id="category"
                              aria-label="Select category"
                            >
                              <SelectValue placeholder="Select category" />
                            </SelectTrigger>
                            <SelectContent>
                              {categoryData.categories.map((category) => (
                                <SelectItem
                                  value={category.category_name}
                                  key={category.category_id}
                                >
                                  {category.category_name}
                                </SelectItem>
                              ))}
                            </SelectContent>
                          </Select> */}
                        <Input readOnly value={data.category.category_name} />
                      </div>
                      <div className="grid gap-3">
                        <Label htmlFor="subcategory">Subcategory</Label>
                        {/* <Select
                            value={currentSubcategory}
                            onValueChange={setCurrentSubcategory}
                          >
                            <SelectTrigger
                              id="subcategory"
                              aria-label="Select subcategory"
                            >
                              <SelectValue placeholder="Select subcategory" />
                            </SelectTrigger>
                            <SelectContent>
                              {categoryData.subcategories
                                .filter(
                                  (subcategory) =>
                                    subcategory.category_id ===
                                    currentCategoryId,
                                )
                                .map((subcategory) => (
                                  <SelectItem
                                    value={subcategory.subcategory_name}
                                    key={subcategory.subcategory_id}
                                  >
                                    {subcategory.subcategory_name}
                                  </SelectItem>
                                ))}
                            </SelectContent>
                          </Select> */}
                        <Input readOnly
                          value={data.subcategory.subcategory_name}
                        />
                      </div>
                    </div>
                  </CardContent>
                </Card>
                {/* <Card>
                    <CardHeader>
                      <CardTitle>Stock</CardTitle>
                      <CardDescription>
                        Lipsum dolor sit amet, consectetur adipiscing elit
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <Table>
                        <TableHeader>
                          <TableRow>
                            <TableHead className="w-[100px]">SKU</TableHead>
                            <TableHead>Stock</TableHead>
                            <TableHead>Price</TableHead>
                            <TableHead className="w-[100px]">Size</TableHead>
                          </TableRow>
                        </TableHeader>
                        <TableBody>
                          <TableRow>
                            <TableCell className="font-semibold">
                              GGPC-001
                            </TableCell>
                            <TableCell>
                              <Label htmlFor="stock-1" className="sr-only">
                                Stock
                              </Label>
                              <Input readOnly
                                id="stock-1"
                                type="number"
                                defaultValue="100"
                              />
                            </TableCell>
                            <TableCell>
                              <Label htmlFor="price-1" className="sr-only">
                                Price
                              </Label>
                              <Input readOnly
                                id="price-1"
                                type="number"
                                defaultValue="99.99"
                              />
                            </TableCell>
                            <TableCell>
                              <ToggleGroup
                                type="single"
                                defaultValue="s"
                                variant="outline"
                              >
                                <ToggleGroupItem value="s">S</ToggleGroupItem>
                                <ToggleGroupItem value="m">M</ToggleGroupItem>
                                <ToggleGroupItem value="l">L</ToggleGroupItem>
                              </ToggleGroup>
                            </TableCell>
                          </TableRow>
                          <TableRow>
                            <TableCell className="font-semibold">
                              GGPC-002
                            </TableCell>
                            <TableCell>
                              <Label htmlFor="stock-2" className="sr-only">
                                Stock
                              </Label>
                              <Input readOnly
                                id="stock-2"
                                type="number"
                                defaultValue="143"
                              />
                            </TableCell>
                            <TableCell>
                              <Label htmlFor="price-2" className="sr-only">
                                Price
                              </Label>
                              <Input readOnly
                                id="price-2"
                                type="number"
                                defaultValue="99.99"
                              />
                            </TableCell>
                            <TableCell>
                              <ToggleGroup
                                type="single"
                                defaultValue="m"
                                variant="outline"
                              >
                                <ToggleGroupItem value="s">S</ToggleGroupItem>
                                <ToggleGroupItem value="m">M</ToggleGroupItem>
                                <ToggleGroupItem value="l">L</ToggleGroupItem>
                              </ToggleGroup>
                            </TableCell>
                          </TableRow>
                          <TableRow>
                            <TableCell className="font-semibold">
                              GGPC-003
                            </TableCell>
                            <TableCell>
                              <Label htmlFor="stock-3" className="sr-only">
                                Stock
                              </Label>
                              <Input readOnly
                                id="stock-3"
                                type="number"
                                defaultValue="32"
                              />
                            </TableCell>
                            <TableCell>
                              <Label htmlFor="price-3" className="sr-only">
                                Stock
                              </Label>
                              <Input readOnly
                                id="price-3"
                                type="number"
                                defaultValue="99.99"
                              />
                            </TableCell>
                            <TableCell>
                              <ToggleGroup
                                type="single"
                                defaultValue="s"
                                variant="outline"
                              >
                                <ToggleGroupItem value="s">S</ToggleGroupItem>
                                <ToggleGroupItem value="m">M</ToggleGroupItem>
                                <ToggleGroupItem value="l">L</ToggleGroupItem>
                              </ToggleGroup>
                            </TableCell>
                          </TableRow>
                        </TableBody>
                      </Table>
                    </CardContent>
                    <CardFooter className="justify-center border-t p-4">
                      <Button size="sm" variant="ghost" className="gap-1">
                        <PlusCircle className="h-3.5 w-3.5" />
                        Add Variant
                      </Button>
                    </CardFooter>
                  </Card> */}
              </div>
              <div className="grid auto-rows-max items-start gap-4 lg:gap-8">
                <Card>
                  <CardHeader>
                    <CardTitle>Product Seller</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid gap-6">
                      <div className="grid gap-3">
                        <Label htmlFor="seller">Seller</Label>
                        <Input readOnly
                          id="seller"
                          type="text"
                          className="w-full"
                          name="seller"
                          defaultValue={data?.seller.name}
                        />
                      </div>
                    </div>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader>
                    <CardTitle>Product Description</CardTitle>
                    {/* <CardDescription>
                        Lipsum dolor sit amet, consectetur adipiscing elit.
                      </CardDescription> */}
                  </CardHeader>
                  <CardContent>
                    <div className="flex flex-col gap-4">
                      <div className="grid gap-3">
                        <Label htmlFor="description">Description</Label>
                        <Textarea
                          readOnly
                          id="description"
                          name="description"
                          className="min-h-32"
                          defaultValue={data?.description}
                        />
                      </div>
                      <div className="grid gap-3">
                        <Label htmlFor="listed_price">Listed Price</Label>
                        <Input readOnly
                          type="number"
                          id="listed_price"
                          name="listed_price"
                          min="0"
                          defaultValue={data?.listed_price}
                        />
                      </div>
                      <div className="grid gap-3">
                        <Label htmlFor="quantity">Quantity</Label>
                        <Input readOnly
                          type="number"
                          id="quantity"
                          name="quantity"
                          min="1"
                          defaultValue={data?.quantity}
                        />
                      </div>
                    </div>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader>
                    <CardTitle>Product Status</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid gap-6">
                      <div className="grid gap-3">
                        <Label htmlFor="status">Status</Label>
                        <Input readOnly value={data?.status} />
                        {/* <Select name="status" defaultValue={data?.status}>
                            <SelectTrigger
                              id="status"
                              aria-label="Select status"
                            >
                              <SelectValue placeholder="Select status" />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectItem value="Available">
                                Available
                              </SelectItem>
                              <SelectItem value="Archived">Archived</SelectItem>
                              <SelectItem value="Sold">Sold</SelectItem>
                            </SelectContent>
                          </Select> */}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
            <div className="flex items-center justify-center gap-2 md:hidden">
              {/* <Button type="button" variant="outline" size="sm">
                  Discard
                </Button> */}
              <Button size="sm" type="submit">
                Interested
              </Button>
            </div>
          </div>
          {/* </Form> */}
        </main>
      </div>
    </div>
  );
}

ProductInfo.loader = loader;
