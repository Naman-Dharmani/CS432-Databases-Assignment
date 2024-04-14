import { useRouteError } from "react-router-dom";

export default function ErrorPage() {
  const error = useRouteError();
  console.error(error);

  return (
    <div className="my-auto flex w-full flex-col content-center items-center">
      <h1 className="mb-6 text-3xl font-bold">Oops!</h1>
      <p>Sorry, an unexpected error has occurred.</p>
      <p className="text-slate-500">
        <i>{error.statusText || error.message}</i>
      </p>
    </div>
  );
}
