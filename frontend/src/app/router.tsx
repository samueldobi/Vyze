import { createBrowserRouter } from "react-router-dom";

import { CompaniesPage } from "../features/companies/companies-page";
import { OverviewPage } from "../features/dashboard/overview-page";
import { HomePage } from "../features/home/home-page";
import { AppLayout } from "./layout";

export const router = createBrowserRouter([
  { path: "/", element: <HomePage /> },
  {
    path: "/workspace",
    element: <AppLayout />,
    children: [
      { index: true, element: <OverviewPage /> },
      { path: "companies", element: <CompaniesPage /> },
    ],
  },
]);
