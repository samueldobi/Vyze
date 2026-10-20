import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";

import { HomePage } from "../src/features/home/home-page";

describe("HomePage", () => {
  it("introduces Vyze and links to the workspace", () => {
    render(
      <MemoryRouter>
        <HomePage />
      </MemoryRouter>,
    );

    expect(
      screen.getByRole("heading", { name: "Find the right work. Know why it matters." }),
    ).toBeInTheDocument();
    expect(screen.getAllByRole("link", { name: "Open workspace" })[0]).toHaveAttribute(
      "href",
      "/workspace",
    );
  });
});
