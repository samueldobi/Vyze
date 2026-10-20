export interface HealthResponse {
  status: string;
  service: string;
}

export interface Company {
  id: string;
  canonical_name: string;
  normalized_domain: string | null;
  website_url: string | null;
  headquarters_country: string | null;
  headquarters_region: string | null;
  employee_size_min: number | null;
  employee_size_max: number | null;
  sector: string | null;
  funding_stage: string | null;
  funding_amount: string | null;
  funding_currency: string | null;
  funding_date: string | null;
  created_at: string;
  updated_at: string;
}

export interface CompanyListResponse {
  items: Company[];
  page: number;
  page_size: number;
  total: number;
  pages: number;
}
