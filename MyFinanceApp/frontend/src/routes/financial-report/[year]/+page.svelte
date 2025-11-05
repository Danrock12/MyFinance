<script lang="ts">
  import { formatMoney } from '$lib/formatMoney';

  export let report: {
    account_name: string;
    monthly_balances: Record<number, number>;
  }[] = [];

  export let totals: { monthly: number[] } = { monthly: [] };
  export let year: number;

  const START_YEAR = 2025;
  const currentYear = new Date().getFullYear();

  let selectedYear = year;

  const years = Array.from({ length: currentYear - START_YEAR + 1 }, (_, i) => START_YEAR + i);

  const months = [
    'JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE',
    'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER'
  ];

  // Get current month index (0-based)
  const currentMonthIdx = new Date().getMonth();

  // Optional: client side load on year change 
  async function loadReport(selectedYear: number) {
    try {
      const res = await fetch(`http://localhost:8000/api/financial-report/${selectedYear}`);
      if (!res.ok) throw new Error(`Failed to load report: ${res.status}`);
      const data = await res.json();
      report = data.report;
      totals = data.totals || { monthly: [] };
      year = selectedYear;
    } catch (e) {
      console.error(e);
      report = [];
      totals = { monthly: [] };
    }
  }

  $: if (selectedYear !== year) {
    loadReport(selectedYear);
  }
</script>

<h1 class="text-2xl font-bold mb-4">Financial Report {year}</h1>

<div class="mb-4">
  <label for="year" class="mr-2 font-medium">Year:</label>
  <select id="year" bind:value={selectedYear} class="border px-2 py-1">
    {#each years as y}
      <option value={y}>{y}</option>
    {/each}
  </select>
</div>

{#if report.length === 0}
  <p>No data available for this year.</p>
{:else}
  <table class="table-auto w-full border-collapse text-sm">
    <thead>
      <tr class="bg-gray-200">
        <th class="border px-3 py-2">ACCOUNT</th>
        {#each months as month}
          <th class="border px-3 py-2">{month}</th>
        {/each}
      </tr>
    </thead>
    <tbody>
      {#each report as row}
        <tr>
          <td class="border px-2 py-1">{row.account_name}</td>
          {#each months as _, i}
            <td class="border px-2 py-1">
              {i <= currentMonthIdx
                ? formatMoney(row.monthly_balances[i] ?? 0)
                : ''}
            </td>
          {/each}
        </tr>
      {/each}
    </tbody>
    <tfoot>
      <tr class="total-row">
        <td class="border px-2 py-1">TOTAL</td>
        {#each totals.monthly.slice(0, months.length) as total, i}
          <td class="border px-2 py-1">
            {i <= currentMonthIdx
              ? formatMoney(total)
              : ''}
          </td>
        {/each}
      </tr>
    </tfoot>
  </table>
  {/if}
