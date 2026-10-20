import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { CompaniesPage } from "../src/features/companies/companies-page";

function renderPage() {
  const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return render(
    <QueryClientProvider client={queryClient}>
      <CompaniesPage />
    </QueryClientProvider>,
  );
}

afterEach(() => vi.restoreAllMocks());

describe("CompaniesPage", () => {
  it("shows the empty state", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(JSON.stringify({ items: [], page: 1, page_size: 25, total: 0, pages: 0 }), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }),
    );

    renderPage();

    expect(await screen.findByRole("heading", { name: "No companies yet" })).toBeInTheDocument();
  });

  it("shows an API error state", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(new Response(null, { status: 503 }));

    renderPage();

    expect(await screen.findByRole("alert")).toHaveTextContent("Could not load companies");
  });
});
