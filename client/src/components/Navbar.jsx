import { Link, NavLink, useNavigate, useSubmit } from "react-router-dom";

import {
  CircleUser,
  LifeBuoy,
  LogIn,
  LogOut,
  Menu,
  Package2,
  Search,
  Settings,
  User,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuShortcut,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Input } from "@/components/ui/input";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { ModeToggle } from "@/components/mode-toggle";

export default function Navbar({ isLoggedIn }) {
  const submit = useSubmit();
  const navigate = useNavigate();

  return (
    <>
      <header className="sticky top-0 z-50 flex h-16 w-full items-center gap-4 border-b border-border/40 bg-background/95 px-4 py-4 backdrop-blur supports-[backdrop-filter]:bg-background/65 md:px-6">
        {/* <div className="container"> */}
        {/* Left Section */}
        <NavLink
          to="/"
          className="hidden items-center gap-2 text-lg font-semibold md:flex md:text-base"
        >
          <Package2 className="h-6 w-6" />
          <span className="sr-only">Acme Inc</span>
        </NavLink>
        {isLoggedIn ? (
          <nav className="hidden flex-col gap-6 text-lg font-medium md:flex md:flex-row md:items-center md:gap-5 md:text-sm lg:gap-6">
            <NavLink
              to="/dashboard"
              className={({ isActive }) => (isActive ? "active" : "inactive")}
            >
              Dashboard
            </NavLink>
            <NavLink
              to="/transactions"
              className={({ isActive }) => (isActive ? "active" : "inactive")}
            >
              My Transactions
            </NavLink>
            <NavLink
              to="/products"
              className={({ isActive }) => (isActive ? "active" : "inactive")}
            >
              My Products
            </NavLink>
            <NavLink
              to="/customers"
              className={({ isActive }) => (isActive ? "active" : "inactive")}
            >
              Customers
            </NavLink>
            <NavLink
              to="/analytics"
              className={({ isActive }) => (isActive ? "active" : "inactive")}
            >
              Analytics
            </NavLink>
          </nav>
        ) : (
          <div className="flex w-full flex-row items-center justify-between">
            <div className="flex flex-grow justify-center">
              <p className="mx-auto hidden text-xl font-semibold">
                Welcome to Buy Sell Portal!
              </p>
            </div>
            <ModeToggle className="mr-2 hidden sm:inline-flex" />
            <Button variant="outline" asChild className="px-2 sm:px-4">
              <Link to="/login">
                <span className="hidden sm:inline">Login</span>
                <LogIn className="h-5 w-5 sm:ml-2" />
              </Link>
            </Button>
          </div>
        )}
        {/* Mobile View */}
        <Sheet>
          <SheetTrigger asChild>
            <Button
              variant="outline"
              size="icon"
              className="-order-1 shrink-0 md:hidden"
            >
              <Menu className="h-5 w-5" />
              <span className="sr-only">Toggle navigation menu</span>
            </Button>
          </SheetTrigger>
          <SheetContent side="left">
            <nav className="grid gap-6 text-lg font-medium">
              <NavLink
                to="/"
                className="flex items-center gap-2 text-lg font-semibold"
              >
                <Package2 className="h-6 w-6" />
                <span className="sr-only">Acme Inc</span>
              </NavLink>
              <NavLink
                to="/dashboard"
                className={({ isActive }) => (isActive ? "active" : "inactive")}
              >
                Dashboard
              </NavLink>
              <NavLink
                to="/transactions"
                className={({ isActive }) => (isActive ? "active" : "inactive")}
              >
                Transactions
              </NavLink>
              <NavLink
                to="/products"
                className={({ isActive }) => (isActive ? "active" : "inactive")}
              >
                My Products
              </NavLink>
              <NavLink
                to="/customers"
                className={({ isActive }) => (isActive ? "active" : "inactive")}
              >
                Customers
              </NavLink>
              <NavLink
                to="/analytics"
                className={({ isActive }) => (isActive ? "active" : "inactive")}
              >
                Analytics
              </NavLink>
              <ModeToggle />
            </nav>
          </SheetContent>
        </Sheet>
        {/* Right section */}
        {isLoggedIn && (
          <div className="flex w-full items-center gap-4 md:ml-auto md:gap-2 lg:gap-4">
            <form className="ml-auto flex-1 sm:flex-initial">
              <div className="relative">
                <Search className="absolute left-2.5 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                <Input
                  type="search"
                  placeholder="Search products..."
                  className="pl-8 sm:w-[300px] md:w-[200px] lg:w-[300px]"
                />
              </div>
            </form>
            <ModeToggle className="hidden md:inline-flex" />
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button
                  variant="secondary"
                  size="icon"
                  className="rounded-full"
                >
                  <CircleUser className="h-5 w-5" />
                  <span className="sr-only">Toggle user menu</span>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-56">
                <DropdownMenuLabel>My Account</DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuGroup>
                  <DropdownMenuItem>
                    <User className="mr-2 h-4 w-4" />
                    <span>Profile</span>
                    <DropdownMenuShortcut>⇧⌘P</DropdownMenuShortcut>
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={() => navigate("/settings")}>
                    <Settings className="mr-2 h-4 w-4" />
                    <span>Settings</span>
                    <DropdownMenuShortcut>⇧⌘S</DropdownMenuShortcut>
                  </DropdownMenuItem>
                </DropdownMenuGroup>
                <DropdownMenuSeparator />
                <DropdownMenuGroup>
                  <DropdownMenuItem>
                    <LifeBuoy className="mr-2 h-4 w-4" />
                    <span>Support</span>
                  </DropdownMenuItem>
                </DropdownMenuGroup>
                <DropdownMenuSeparator />
                <DropdownMenuItem
                  onClick={() =>
                    submit(null, { method: "post", action: "/logout" })
                  }
                >
                  <LogOut className="mr-2 h-4 w-4" />
                  <span>Log out</span>
                  <DropdownMenuShortcut>⇧⌘Q</DropdownMenuShortcut>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        )}
        {/* </div> */}
      </header>
    </>
  );
}
