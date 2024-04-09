import { Form, redirect, useLoaderData } from "react-router-dom";

import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";

async function loader({ request }) {
  return fetch(`${import.meta.env.VITE_URL}/user/1`);
}

async function action({ request, params }) {
  const formData = await request.formData();
  const data = Object.fromEntries(formData);

  console.log(data);

  const response = await fetch(`${import.meta.env.VITE_URL}/user/1`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (response.ok) {
    return redirect("/");
  } else {
    throw new Error("Error updating user details");
  }
}

export default function Settings() {
  const data = useLoaderData();

  return (
    <div className="hidden space-y-6 p-10 pb-16 md:block">
      <div className="space-y-0.5">
        <h2 className="text-2xl font-bold tracking-tight">Settings</h2>
        <p className="text-muted-foreground">
          Manage your account settings and set e-mail preferences.
        </p>
      </div>
      <div
        className="my-6 h-[1px] w-full shrink-0 bg-border"
        data-orientation="horizontal"
        role="none"
      />
      <div className="flex flex-col space-y-8 lg:flex-row lg:space-x-12 lg:space-y-0">
        <aside className="-mx-4 lg:w-1/5">
          <nav className="flex space-x-2 lg:flex-col lg:space-x-0 lg:space-y-1">
            <a
              className="inline-flex h-9 items-center justify-start whitespace-nowrap rounded-md bg-muted px-4 py-2 text-sm font-medium transition-colors hover:bg-muted hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50"
              href="/examples/forms"
            >
              Profile
            </a>
            <a
              className="inline-flex h-9 items-center justify-start whitespace-nowrap rounded-md px-4 py-2 text-sm font-medium transition-colors hover:bg-transparent hover:text-accent-foreground hover:underline focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50"
              href="/examples/forms/account"
            >
              Account
            </a>
            <a
              className="inline-flex h-9 items-center justify-start whitespace-nowrap rounded-md px-4 py-2 text-sm font-medium transition-colors hover:bg-transparent hover:text-accent-foreground hover:underline focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50"
              href="/examples/forms/appearance"
            >
              Appearance
            </a>
            <a
              className="inline-flex h-9 items-center justify-start whitespace-nowrap rounded-md px-4 py-2 text-sm font-medium transition-colors hover:bg-transparent hover:text-accent-foreground hover:underline focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50"
              href="/examples/forms/notifications"
            >
              Notifications
            </a>
            {/* <a
              className="inline-flex h-9 items-center justify-start whitespace-nowrap rounded-md px-4 py-2 text-sm font-medium transition-colors hover:bg-transparent hover:text-accent-foreground hover:underline focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50"
              href="/examples/forms/display"
            >
              Display
            </a> */}
          </nav>
        </aside>
        <div className="flex-1 lg:max-w-2xl">
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-medium">Profile</h3>
              <p className="text-sm text-muted-foreground">
                This is how others will see you on the site.
              </p>
            </div>
            <div
              className="h-[1px] w-full shrink-0 bg-border"
              data-orientation="horizontal"
              role="none"
            />
            <Form method="post" className="space-y-8">
              <div className="space-y-2">
                <label
                  className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                  htmlFor=":r1bq:-form-item"
                >
                  Name
                </label>
                <Input
                  type="text"
                  name="name"
                  placeholder="John Doe"
                  defaultValue={data?.name}
                />
                <p
                  className="text-[0.8rem] text-muted-foreground"
                  id=":r1bq:-form-item-description"
                >
                  This is your public display name.
                </p>
              </div>
              <div className="space-y-2">
                <label
                  className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                  htmlFor=":r1br:-form-item"
                >
                  Email
                </label>
                <Input
                  name="email"
                  placeholder="a@b.c"
                  defaultValue={data?.email}
                />
              </div>
              <div className="space-y-2">
                <label
                  className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                  htmlFor=":r1bq:-form-item"
                >
                  Phone No.
                </label>
                <Input
                  type="number"
                  name="phone_no"
                  placeholder="1234567890"
                  defaultValue={data?.phone_no}
                  min="0"
                  max="9999999999"
                />
                {/* <p
                  className="text-[0.8rem] text-muted-foreground"
                  id=":r1bq:-form-item-description"
                >
                  Phone No.
                </p> */}
              </div>
              <div className="space-y-2">
                <label
                  className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                  htmlFor=":r1bq:-form-item"
                >
                  Gender
                </label>
                <Select defaultValue={data?.gender} name="gender">
                  <SelectTrigger className="w-full">
                    <SelectValue placeholder="Select gender" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectGroup>
                      {/* <SelectLabel>Male</SelectLabel> */}
                      <SelectItem value="Male">Male</SelectItem>
                      <SelectItem value="Female">Female</SelectItem>
                      <SelectItem value="Other">Other</SelectItem>
                    </SelectGroup>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <label
                  className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                  htmlFor=":r1bt:-form-item"
                >
                  Residence
                </label>
                <Textarea
                  name="residence_location"
                  placeholder="Residence Location"
                  defaultValue={data?.residence_location}
                />
                {/* <p
                  className="text-[0.8rem] text-muted-foreground"
                  id=":r1bt:-form-item-description"
                >
                  You can <span>@mention</span> other users and organizations to
                  link to them.
                </p> */}
              </div>
              {/* <div>
                <div className="space-y-2">
                  <label
                    className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                    htmlFor=":r1bu:-form-item"
                  >
                    URLs
                  </label>
                  <p
                    className="text-[0.8rem] text-muted-foreground"
                    id=":r1bu:-form-item-description"
                  >
                    Add links to your website, blog, or social media profiles.
                  </p>
                  <input
                    aria-describedby=":r1bu:-form-item-description"
                    aria-invalid="false"
                    className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
                    defaultValue="https://shadcn.com"
                    id=":r1bu:-form-item"
                    name="urls.0.value"
                  />
                </div>
                <div className="space-y-2">
                  <label
                    className="sr-only text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                    htmlFor=":r1bv:-form-item"
                  >
                    URLs
                  </label>
                  <p
                    className="sr-only text-[0.8rem] text-muted-foreground"
                    id=":r1bv:-form-item-description"
                  >
                    Add links to your website, blog, or social media profiles.
                  </p>
                  <input
                    aria-describedby=":r1bv:-form-item-description"
                    aria-invalid="false"
                    className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
                    defaultValue="http://twitter.com/shadcn"
                    id=":r1bv:-form-item"
                    name="urls.1.value"
                  />
                </div>
                <button
                  className="mt-2 inline-flex h-8 items-center justify-center whitespace-nowrap rounded-md border border-input bg-background px-3 text-xs font-medium shadow-sm transition-colors hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50"
                  type="button"
                >
                  Add URL
                </button>
              </div> */}
              <Button type="submit">Update profile</Button>
            </Form>
          </div>
        </div>
      </div>
    </div>
  );
}

Settings.loader = loader;
Settings.action = action;
