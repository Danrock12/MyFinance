<script lang="ts">
  import { onMount } from 'svelte';

  let report: {
    account_name: string;
    start: number;
    monthly: number[];
  }[] = [];

  let totals = { start: 0, monthly: [] as number[] };

  const START_YEAR = 2025;
  const currentYear = new Date().getFullYear();

  let selectedYear = currentYear;

  const years = Array.from({ length: currentYear - START_YEAR + 1 }, (_, i) => START_YEAR + i);

  const months = [
    'JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE',
    'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER'
  ];

  function format(val: number) {
    return `$${val?.toFixed(2)}`;
  }

  async function loadReport(year: number) {
    try {
      const res = await fetch(`/api/financial-report/${year}`);
      if (!res.ok) throw new Error(`Failed to fetch for ${year}: ${res.statusText}`);
      const data = await res.json();
      report = data.report;
      totals = data.totals;
    } catch (e) {
      console.error(e);
      report = [];
      totals = { start: 0, monthly: [] };
    }
  }

  $: if (selectedYear) {
    loadReport(selectedYear);
  }
</script>

<h1 class="text-2xl font-bold mb-4">Financial Report</h1>

<div class="mb-4">
  <label for="year" class="mr-2 font-medium">Year:</label>
  <select id="year" bind:value={selectedYear} class="border px-2 py-1">
    {#each years as y}
      <option value={y}>{y}</option>
    {/each}
  </select>
</div>

<table class="table-auto w-full border-collapse text-sm">
  <thead>
    <tr class="bg-gray-200">
      <th class="px-3 py-2 border">ACCOUNT</th>
      <th class="px-3 py-2 border">START</th>
      {#each months as month}
        <th class="px-3 py-2 border">{month}</th>
      {/each}
    </tr>
  </thead>
  <tbody>
    {#each report as row}
      <tr>
        <td class="border px-2 py-1">{row.account_name}</td>
        <td class="border px-2 py-1">{format(row.start)}</td>
        {#each row.monthly as val}
          <td class="border px-2 py-1">{format(val)}</td>
        {/each}
      </tr>
    {/each}
  </tbody>
  <tfoot>
    <tr class="font-bold bg-gray-100 border-t">
      <td class="border px-2 py-1">TOTAL</td>
      <td class="border px-2 py-1">{format(totals.start)}</td>
      {#each totals.monthly as total}
        <td class="border px-2 py-1">{format(total)}</td>
      {/each}
    </tr>
  </tfoot>
</table>
