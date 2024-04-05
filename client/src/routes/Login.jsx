import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { json, Form, redirect, useActionData } from "react-router-dom";

async function action({ request }) {
  const formData = await request.formData();
  const data = Object.fromEntries(formData);

  // check if credentials are correct
  if (Math.random() < 0.5) {
    return redirect("/");
    // return json({ ok: true }, { status: 200 });
  } else {
    return json({ msg: "Invalid credentials" }, { status: 403 });
  }
}

export default function LoginForm() {
  // Check from the context if already logged in, redirect

  const errors = useActionData();

  return (
    <div className="mt-10 flex w-full items-center justify-center sm:mt-20 lg:mt-40">
      <Card className="mx-4 w-full max-w-sm sm:mx-0">
        <CardHeader>
          <CardTitle className="text-2xl">Login</CardTitle>
          <CardDescription>
            Enter your email below to login to your account.
          </CardDescription>
        </CardHeader>
        <Form method="post">
          <CardContent className="grid gap-4">
            <div className="grid gap-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                name="email"
                placeholder="m@example.com"
                required
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="password">Password</Label>
              <Input id="password" type="password" name="password" required />
            </div>
            {/* Error on submitting the form */}
            {errors?.msg && (
              <div>
                <p className="text-red-500 dark:text-red-300">
                  * <span className="italic">{errors.msg}</span>
                </p>
              </div>
            )}
          </CardContent>
          <CardFooter>
            <Button className="w-full" type="submit">
              Sign in
            </Button>
          </CardFooter>
        </Form>
      </Card>
    </div>
  );
}

LoginForm.action = action;
