import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch, params }) => {
  const yearParam = params.year;
  const year = Number(yearParam) || new Date().getFullYear();

  // Adjust backend URL accordingly, for dev this is localhost:8000
  const backendUrl = `http://localhost:8000/api/financial-report/${year}`;

  const res = await fetch(backendUrl);

  if (!res.ok) {
    return {
      report: [],
      totals: { start: 0, monthly: [] },
      year,
    };
  }

  const data = await res.json();

  return {
    report: data.report || [],
    totals: data.totals || { start: 0, monthly: [] },
    year,
  };
};
