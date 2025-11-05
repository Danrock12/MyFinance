<script lang="ts">
  import { formatMoney } from '$lib/formatMoney';

  export let transactions: Array<{ date: string; amount: number; type: 'income' | 'expense' | 'transfer' }> = [];
  export let initialBalance: number = 0; // Set this to your actual starting balance

  // Group transactions by month
  function groupByMonth(transactions) {
    const months = {};
    for (const tx of transactions) {
      const month = tx.date.slice(0, 7); // 'YYYY-MM'
      if (!months[month]) months[month] = [];
      months[month].push(tx);
    }
    return months;
  }

  const months = groupByMonth(transactions);
  const sortedMonths = Object.keys(months).sort();

  let monthlyRows = [];
  let lastEndingBalance = initialBalance;

  for (const month of sortedMonths) {
    const txs = months[month];
    let monthlyChange = 0;
    for (const tx of txs) {
      if (tx.type === 'income') monthlyChange += tx.amount;
      else if (tx.type === 'expense') monthlyChange -= tx.amount;
      // You can handle 'transfer' type as needed
    }
    const endBalance = lastEndingBalance + monthlyChange;
    monthlyRows.push({ month, monthlyChange, endBalance });
    lastEndingBalance = endBalance;
  }

  // Calculate totals for the bottom row
  let totalChange = monthlyRows.reduce((sum, row) => sum + row.monthlyChange, 0);
  let totalEndBalance = monthlyRows.length > 0 ? monthlyRows[monthlyRows.length - 1].endBalance : initialBalance;
</script>

<h1>Financial Report</h1>
<table>
  <thead>
    <tr>
      <th>Month</th>
      <th>Monthly Change</th>
      <th>End Balance</th>
    </tr>
  </thead>
  <tbody>
    {#each monthlyRows as row}
      <tr>
        <td>{row.month}</td>
        <td>{formatMoney(row.monthlyChange)}</td>
        <td>{formatMoney(row.endBalance)}</td>
      </tr>
    {/each}
  </tbody>
  <tfoot>
    <tr class="total-row">
      <td>Total</td>
      <td>{formatMoney(totalChange)}</td>
      <td>{formatMoney(totalEndBalance)}</td>
    </tr>
  </tfoot>
</table>
<style>
  hr {
    margin: 2em 0;
    border-color: var(--border);
  }
</style>