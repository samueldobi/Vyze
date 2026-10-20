import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";

import { apiRequest } from "../../api/client";
import type { HealthResponse } from "../../api/types";

export function OverviewPage() {
  const health = useQuery({
    queryKey: ["health"],
    queryFn: () => apiRequest<HealthResponse>("/api/v1/health"),
  });

  return (
    <section>
      <header className="page-header">
        <div>
          <p className="eyebrow">Opportunity workspace</p>
          <h1>Good opportunities start with clear evidence.</h1>
          <p className="lede">
            Review companies, roles, signals, and relationships from one private local workspace.
          </p>
        </div>
        <div className="connection" role="status">
          <span className={`status-dot ${health.isSuccess ? "online" : ""}`} />
          {health.isPending && "Checking API"}
          {health.isSuccess && "Local API connected"}
          {health.isError && "API unavailable"}
        </div>
      </header>

      <div className="metric-grid" aria-label="Workspace status">
        <article className="metric-card">
          <span>Companies</span>
          <strong>Ready</strong>
          <Link to="/workspace/companies">Open company records</Link>
        </article>
        <article className="metric-card muted">
          <span>Jobs</span>
          <strong>Next</strong>
          <p>Job workflows arrive in the next backend slice.</p>
        </article>
        <article className="metric-card muted">
          <span>Outreach</span>
          <strong>Later</strong>
          <p>Drafts will always require your review.</p>
        </article>
      </div>
    </section>
  );
}
