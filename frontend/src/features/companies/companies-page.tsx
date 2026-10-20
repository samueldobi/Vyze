import { useQuery } from "@tanstack/react-query";

import { apiRequest } from "../../api/client";
import type { CompanyListResponse } from "../../api/types";

export function CompaniesPage() {
  const companies = useQuery({
    queryKey: ["companies"],
    queryFn: () => apiRequest<CompanyListResponse>("/api/v1/companies?page=1&page_size=25"),
  });

  return (
    <section>
      <header className="page-header compact">
        <div>
          <p className="eyebrow">Company records</p>
          <h1>Companies</h1>
          <p className="lede">A deduplicated view of organizations and their evidence.</p>
        </div>
      </header>

      {companies.isPending && <div className="state-card">Loading companies…</div>}
      {companies.isError && (
        <div className="state-card error" role="alert">
          Could not load companies. Confirm that the local API is running.
        </div>
      )}
      {companies.data?.total === 0 && (
        <div className="state-card">
          <h2>No companies yet</h2>
          <p>Company creation controls will be added next. The API is ready now.</p>
        </div>
      )}
      {companies.data && companies.data.total > 0 && (
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th scope="col">Company</th>
                <th scope="col">Region</th>
                <th scope="col">Sector</th>
                <th scope="col">Team size</th>
              </tr>
            </thead>
            <tbody>
              {companies.data.items.map((company) => (
                <tr key={company.id}>
                  <td>
                    <strong>{company.canonical_name}</strong>
                    <span>{company.normalized_domain ?? "Domain unknown"}</span>
                  </td>
                  <td>{company.headquarters_region ?? company.headquarters_country ?? "Unknown"}</td>
                  <td>{company.sector ?? "Unknown"}</td>
                  <td>
                    {company.employee_size_min !== null && company.employee_size_max !== null
                      ? `${company.employee_size_min}–${company.employee_size_max}`
                      : "Unknown"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}
