import { useState } from "react";
import {
  Form,
  Navigate,
  json,
  Link,
  useActionData,
  useNavigate,
} from "react-router-dom";
import { useGoogleLogin } from "@react-oauth/google";
import { useAuthContext } from "@/context/auth-provider";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

async function action({ request }) {
  const formData = await request.formData();
  const data = Object.fromEntries(formData);
  console.log(data);

  // const res = fetch(`${import.meta.env.VITE_URL}/login`);

  // check if credentials are correct
  if (Math.random() < 0.5) {
    // return redirect("/");
    return json({ ok: true }, { status: 200 });
  } else {
    return json({ msg: "Invalid credentials" }, { status: 403 });
  }
}

async function getUserDetails(authCode) {
  const res = await fetch(`${import.meta.env.VITE_URL}/auth/google`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ code: authCode.code }),
  });

  console.log(res);

  if (res.status == 200) {
    return await res.json();
  } else {
    return { error: true, msg: "error fetching logged in user details" };
  }
}

export default function LoginForm() {
  const navigate = useNavigate();
  const errors = useActionData();
  const { authUser, setAuthUser } = useAuthContext();
  const [isError, setIsError] = useState(false);

  const handleAuthSuccess = async (authCode) => {
    if (authCode.hd === "iitgn.ac.in") {
      const authUserDetails = await getUserDetails(authCode);
      console.log(authUserDetails);
      if (authUserDetails.error) {
        localStorage.removeItem("bs_jwt");
        setAuthUser(null);
        setIsError({ msg: authUserDetails.msg });
      } else {
        localStorage.setItem("bs_jwt", authUserDetails.user.jwt);
        setAuthUser(authUserDetails.user);
        setIsError(null);
        navigate("/");
      }
    } else {
      localStorage.removeItem("bs_jwt");
      setAuthUser(null);
      setIsError({
        msg: "Host domain not authorized",
      });
    }
  };

  const handleAuthError = (error) => {
    console.log(error);
    setAuthUser(null);
    setIsError({
      msg: "OAuth Error. Retry",
    });
  };

  const googleLogin = useGoogleLogin({
    flow: "auth-code",
    onSuccess: handleAuthSuccess,
    onError: handleAuthError,
  });

  if (authUser) {
    return <Navigate to="/" />;
  }

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
          <CardContent>
            <div className="grid gap-4">
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
                <div className="flex items-center">
                  <Label htmlFor="password">Password</Label>
                  <Link
                    to="#"
                    className="ml-auto inline-block text-sm underline"
                  >
                    Forgot your password?
                  </Link>
                </div>
                <Input id="password" type="password" name="password" required />
              </div>
              {/* Error on submitting the form */}
              {(isError || errors?.msg) && (
                <div>
                  <p className="text-red-500 dark:text-red-300">
                    * <span className="italic">{isError || errors?.msg}</span>
                  </p>
                </div>
              )}
              <Button className="w-full" type="submit">
                Login
              </Button>
              <Button
                variant="outline"
                className="w-full"
                onClick={googleLogin}
              >
                Login with Google
              </Button>
            </div>
            <div className="mt-4 text-center text-sm">
              Don&apos;t have an account?{" "}
              <Link href="#" className="underline">
                Sign up
              </Link>
            </div>
          </CardContent>
        </Form>
      </Card>
    </div>
  );
}

LoginForm.action = action;
