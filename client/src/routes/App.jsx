import Navbar from "../components/Navbar";
import { Outlet } from "react-router-dom";

function App() {
  return (
    <>
      <Navbar />
      <h1 className="text-3xl font-bold underline">Hello world!</h1>
      <Outlet />
    </>
  );
}

export default App;
