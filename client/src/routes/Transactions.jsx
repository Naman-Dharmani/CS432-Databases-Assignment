import { Form, useLoaderData, useNavigate } from "react-router-dom";

// import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  // CardFooter,
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
// import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
// import {
//   Table,
//   TableBody,
//   TableCell,
//   TableHead,
//   TableHeader,
//   TableRow,
// } from "@/components/ui/table";
import { Textarea } from "@/components/ui/textarea";


async function loader({ params }) {
  return fetch(`${import.meta.env.VITE_URL}/user/1/transactions`);
}


async function action({ request, params }) {
  const formData = await request.formData();
  const data = Object.fromEntries(formData);

  const response = await fetch(
    `${import.meta.env.VITE_URL}/review/${data.review_id}`,
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
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
  const data = useLoaderData();
  const navigate = useNavigate();

  return (
    <div className="flex flex-col w-full">
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
                      src={
                        transaction.product_image ||
                        "/placeholder.svg"
                      }
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
                          <div className="pr-2 w-24">
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
                          <div className="p-2"><Button type="submit">Submit</Button></div>
                        </div>
                      </Form></TableCell>) : (
                    <TableCell>
                      <div className="flex flex-row items-center">
                        <div className="pr-2 w-24">
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
                  )
                  }

                </TableRow >
              ))}
            </TableBody >
          </Table >
        </CardContent >
      </Card >
    </div >
  );
}

Transactions.loader = loader;
Transactions.action = action;