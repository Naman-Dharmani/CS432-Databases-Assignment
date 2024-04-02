import { NavLink } from "react-router-dom";

function Navbar() {
  return (
    <>
      <div>
        <nav className="mb-6 flex items-center justify-between">
          <NavLink to="/">
            <img
              alt="MongoDB logo"
              className="inline h-10"
              src="https://d3cy9zhslanhfa.cloudfront.net/media/3800C044-6298-4575-A05D5C6B7623EE37/4B45D0EC-3482-4759-82DA37D8EA07D229/webimage-8A27671A-8A53-45DC-89D7BF8537F15A0D.png"
            ></img>
          </NavLink>

          <NavLink
            className="text-md inline-flex h-9 items-center justify-center whitespace-nowrap rounded-md border border-input bg-background px-3 font-medium ring-offset-background transition-colors hover:bg-slate-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50"
            to="/products"
          >
            Create Employee
          </NavLink>
        </nav>
      </div>
    </>
  );
}

export default Navbar;
