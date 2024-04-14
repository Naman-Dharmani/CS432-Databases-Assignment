import { Form, useLoaderData } from "react-router-dom";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Textarea } from "@/components/ui/textarea";

async function loader() {
  return fetch(`${import.meta.env.VITE_URL}/user/transactions`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("bs_jwt")}`,
    },
  });
}

async function action({ request }) {
  const formData = await request.formData();
  const data = Object.fromEntries(formData);

  const response = await fetch(
    `${import.meta.env.VITE_URL}/review/${data.review_id}`,
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("bs_jwt")}`,
      },
      body: JSON.stringify(data),
    },
  );

  if (response.ok) {
    // return redirect("/products");
    return response.json();
  } else {
    throw new Error("Error updating product details");
  }
}

export default function Transactions() {
  // const navigate = useNavigate();
  const data = useLoaderData();

  return (
    <div className="flex w-full flex-col">
      <Card>
        <CardHeader>
          <CardTitle>Transactions</CardTitle>
          <CardDescription>View all transactions</CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Product Image</TableHead>
                <TableHead>Product Title</TableHead>
                <TableHead>Quantity</TableHead>
                <TableHead>Price</TableHead>
                <TableHead>Buyer</TableHead>
                <TableHead>Seller</TableHead>
                <TableHead>Date-Time</TableHead>
                <TableHead>Rating and Review</TableHead>
                {/* <TableHead>Review</TableHead> */}
                {/* <TableHead>Status</TableHead> */}
                {/* <TableHead>Actions</TableHead> */}
              </TableRow>
            </TableHeader>
            <TableBody>
              {data?.map((transaction) => (
                <TableRow key={transaction.transaction_id}>
                  <TableCell>
                    <img
                      alt="product"
                      className="aspect-square rounded-md object-contain"
                      height="64"
                      src={transaction.product_image || "/placeholder.svg"}
                      width="64"
                    />
                  </TableCell>
                  <TableCell>{transaction.product_title}</TableCell>
                  <TableCell>{transaction.quantity}</TableCell>
                  <TableCell>{transaction.selling_price}</TableCell>
                  <TableCell>{transaction.buyer_name}</TableCell>
                  <TableCell>{transaction.seller_name}</TableCell>
                  <TableCell>{transaction.transaction_date}</TableCell>
                  {transaction.buyer_id === 1 ? (
                    <TableCell>
                      <Form method="post">
                        <div className="flex flex-row items-center">
                          <div className="">
                            <Input
                              type="hidden"
                              name="review_id"
                              value={transaction.review_id}
                            />
                          </div>
                          <div className="w-24 pr-2">
                            <Input
                              type="number"
                              name="rating"
                              placeholder="Rating"
                              defaultValue={transaction.rating}
                            />
                          </div>
                          <div className="p-2">
                            <Textarea
                              name="review"
                              placeholder="Review"
                              defaultValue={transaction.review}
                            />
                          </div>
                          <div className="p-2">
                            <Button type="submit">Submit</Button>
                          </div>
                        </div>
                      </Form>
                    </TableCell>
                  ) : (
                    <TableCell>
                      <div className="flex flex-row items-center">
                        <div className="w-24 pr-2">
                          <Input
                            type="number"
                            name="rating"
                            placeholder="Rating"
                            defaultValue={transaction.rating}
                            readOnly
                          />
                        </div>
                        <div className="p-2">
                          <Textarea
                            name="review"
                            placeholder="Review"
                            defaultValue={transaction.review}
                            readOnly
                          />
                        </div>
                      </div>
                    </TableCell>
                  )}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}

Transactions.loader = loader;
Transactions.action = action;
