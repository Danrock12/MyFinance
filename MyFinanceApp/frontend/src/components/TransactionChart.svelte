<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { Chart, registerables } from 'chart.js';
  import ChartDataLabels from 'chartjs-plugin-datalabels';

  export let transactions: {
    id?: number;
    date: string;
    name?: string;
    amount: number;
    type: 'income' | 'expense' | 'transfer';
  }[] = [];

  let canvas: HTMLCanvasElement;
  let chart: Chart | null = null;
  let lastDataJSON = '';

  function createChart() {
    if (!canvas) {
      console.error('Canvas element not found!');
      return;
    }

    const dataJSON = JSON.stringify(transactions);
    if (dataJSON === lastDataJSON && chart) {
      return; // no changes
    }
    lastDataJSON = dataJSON;

    if (chart) {
      chart.destroy();
      chart = null;
    }

    Chart.register(...registerables, ChartDataLabels);

    // Use transaction label (e.g. date + name) for x-axis labels
    const labels = transactions.map(
      (tx) => `${tx.date}${tx.name ? ` - ${tx.name}` : ''}`
    );

    // Amounts: expenses as negative to show below zero, income positive, transfers zero or skipped
    const amounts = transactions.map((tx) =>
      tx.type === 'expense' ? -tx.amount : tx.amount
    );

    // Colors per transaction type
    const backgroundColors = transactions.map((tx) => {
      if (tx.type === 'income') return 'rgba(75, 192, 192, 0.7)';
      if (tx.type === 'expense') return 'rgba(255, 99, 132, 0.7)';
      if (tx.type === 'transfer') return 'rgba(201, 203, 207, 0.7)'; // gray
      return 'rgba(0, 0, 0, 0.7)';
    });

    chart = new Chart(canvas, {
      type: 'bar',
      data: {
        labels,
        datasets: [
          {
            label: 'Transaction Amount',
            data: amounts,
            backgroundColor: backgroundColors,
            borderColor: backgroundColors.map((c) => c.replace('0.7', '1')),
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          title: { display: true, text: 'All Transactions' },
          tooltip: {
            callbacks: {
              label: (ctx) => {
                const tx = transactions[ctx.dataIndex];
                return `${tx.name ?? 'Transaction'}: $${tx.amount.toFixed(2)}`;
              },
            },
          },
          datalabels: {
            color: '#000',
            font: {
              weight: 'bold',
              size: 12,
            },
            formatter: (value) => `$${Math.abs(value).toFixed(2)}`,
            anchor: 'end',
            align: 'top',
          },
        },
        scales: {
          x: {
            ticks: {
              maxRotation: 90,
              minRotation: 45,
              autoSkip: false,
              maxTicksLimit: 20,
              font: { size: 10 },
            },
          },
          y: {
            beginAtZero: true,
            ticks: {
              callback: (val) => `$${Math.abs(val)}`,
            },
          },
        },
      },
      plugins: [ChartDataLabels],
    });
  }

  onMount(() => {
    createChart();
  });

  $: transactions, createChart();

  onDestroy(() => {
    if (chart) {
      chart.destroy();
    }
  });
</script>

<style>
  .chart-container {
    position: relative;
    width: 100%;
    height: 400px;
    border: 1px solid red;
  }
</style>

<div class="chart-container">
  <canvas bind:this={canvas}></canvas>
</div>

