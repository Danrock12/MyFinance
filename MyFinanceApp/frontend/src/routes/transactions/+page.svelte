<script lang="ts">
  import { onMount } from 'svelte';
  import { formatMoney } from '$lib/formatMoney';

  type Transaction = {
    id: number;
    date: string;
    name: string;
    tag: string;
    type: 'income' | 'expense' | 'transfer';
    amount: number;
    credit_card_used: boolean;
    credit_card_name?: string;
    account_id?: number;
    transfer_from_account?: { id: number; name: string };
    transfer_to_account?: { id: number; name: string };
    account?: { id: number; name: string };
  };

  type Account = {
    id: number;
    name: string;
  };

  let date = '';
  let name = '';
  let tag = '';
  let type: 'income' | 'expense' | 'transfer' = 'income';
  let amount: number = 0;
  let creditCardUsed = false;
  let creditCardName = '';
  let selectedAccountId: number | null = null;
  let transferFromAccountId: number | null = null;
  let transferToAccountId: number | null = null;

  let accounts: Account[] = [];
  let transactions: Transaction[] = [];
  let errorMessage = '';
  let successMessage = '';
  let filter = 'all';

  async function fetchAccounts() {
    const res = await fetch('http://localhost:8000/accounts/');
    accounts = await res.json();
  }

  async function fetchTransactions() {
    const res = await fetch('http://localhost:8000/transactions/');
    transactions = await res.json();
  }

  async function handleSubmit() {
    errorMessage = '';
    successMessage = '';

    let payload: any = {
      date,
      name,
      tag,
      type,
      amount,
      credit_card_used: creditCardUsed,
      credit_card_name: creditCardUsed ? creditCardName : null,
    };

    if (type === 'transfer') {
      payload.transfer_from_account_id = transferFromAccountId;
      payload.transfer_to_account_id = transferToAccountId;
      payload.account_id = null;
    } else {
      payload.account_id = creditCardUsed ? null : selectedAccountId;
      payload.transfer_from_account_id = null;
      payload.transfer_to_account_id = null;
    }

    const res = await fetch('http://localhost:8000/transactions/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const err = await res.json();
      errorMessage = err.detail || 'Failed to create transaction';
      return;
    }

    successMessage = 'Transaction added!';
    await fetchTransactions();

    // Reset form
    name = '';
    tag = '';
    amount = 0;
    creditCardUsed = false;
    creditCardName = '';
    selectedAccountId = null;
    transferFromAccountId = null;
    transferToAccountId = null;
  }

  async function handleDelete(transactionId: number) {
    const confirmed = confirm('Are you sure you want to delete this transaction?');
    if (!confirmed) return;

    const res = await fetch(`http://localhost:8000/transactions/${transactionId}`, {
      method: 'DELETE',
    });

    if (!res.ok) {
      const err = await res.json();
      errorMessage = err.detail || 'Failed to delete transaction';
      return;
    }

    successMessage = 'Transaction deleted!';
    await fetchTransactions();
  }

  $: filteredTransactions = (() => {
    if (filter === 'all') return transactions;
    const daysBack = Number(filter);
    const cutoff = new Date();
    cutoff.setDate(cutoff.getDate() - daysBack);
    return transactions.filter(tx => new Date(tx.date) >= cutoff);
  })();

  onMount(() => {
    fetchAccounts();
    fetchTransactions();
  });
</script>

<h1>Create Transaction</h1>
<form on:submit|preventDefault={handleSubmit} class="transaction-form">
  <label>Date:
    <input type="date" bind:value={date} required />
  </label>

  <label>Name:
    <input type="text" bind:value={name} required />
  </label>

  <label>Tag:
    <input type="text" bind:value={tag} required />
  </label>

  <label>Type:
    <select bind:value={type}>
      <option value="income">Income</option>
      <option value="expense">Expense</option>
      <option value="transfer">Transfer</option>
    </select>
  </label>

  <label>Amount:
    <input type="number" bind:value={amount} required step="0.01" />
  </label>

  {#if type === 'transfer'}
    <label>Transfer From Account:
      <select bind:value={transferFromAccountId} required>
        <option disabled selected value="">-- Choose from account --</option>
        {#each accounts as account}
          <option value={account.id}>{account.name}</option>
        {/each}
      </select>
    </label>

    <label>Transfer To Account:
      <select bind:value={transferToAccountId} required>
        <option disabled selected value="">-- Choose to account --</option>
        {#each accounts as account}
          <option value={account.id}>{account.name}</option>
        {/each}
      </select>
    </label>
  {:else}
    <label>
      Purchased on Credit Card?
      <input type="checkbox" bind:checked={creditCardUsed} />
    </label>

    {#if creditCardUsed}
      <label>Credit Card Name:
        <input type="text" bind:value={creditCardName} required />
      </label>
    {:else}
      <label>Select Account:
        <select bind:value={selectedAccountId} required>
          <option disabled selected value="">-- Choose account --</option>
          {#each accounts as account}
            <option value={account.id}>{account.name}</option>
          {/each}
        </select>
      </label>
    {/if}
  {/if}

  <button type="submit">Add Transaction</button>
</form>

{#if successMessage}
  <p class="success">{successMessage}</p>
{/if}
{#if errorMessage}
  <p class="error">{errorMessage}</p>
{/if}

<hr />

<h2>Filter Transactions</h2>
<select bind:value={filter}>
  <option value="all">All Transactions</option>
  <option value="30">Last 30 Days</option>
  <option value="60">Last 60 Days</option>
</select>

<ul>
  {#each filteredTransactions as tx}
    <li>
      <strong>{tx.date}</strong> / {tx.name} / {tx.tag} / {tx.type.charAt(0).toUpperCase() + tx.type.slice(1)} / {formatMoney(tx.amount)} /
      {#if tx.credit_card_used}
        Credit Card ({tx.credit_card_name})
      {:else if tx.type === 'transfer'}
        {tx.transfer_from_account?.name} → {tx.transfer_to_account?.name}
      {:else}
        {tx.account?.name}
      {/if}
      <button on:click={() => handleDelete(tx.id)}>🗑️ Delete</button>
    </li>
  {/each}
</ul>

<hr />

<h2>All Transactions</h2>
<table class="transaction-table">
  <thead>
    <tr>
      <th>Date</th>
      <th>Name</th>
      <th>Tag</th>
      <th>Type</th>
      <th>Amount</th>
      <th>Account / Details</th>
    </tr>
  </thead>
  <tbody>
    {#each transactions as tx}
      <tr>
        <td>{tx.date}</td>
        <td>{tx.name}</td>
        <td>{tx.tag}</td>
        <td>{tx.type.charAt(0).toUpperCase() + tx.type.slice(1)}</td>
        <td
          style="
            font-weight: bold;
            color: {tx.type === 'income' ? 'green' : tx.type === 'expense' ? 'red' : 'inherit'};
            font-style: {tx.type === 'transfer' ? 'italic' : 'normal'};
          "
        >
          {formatMoney(tx.amount)}
        </td>
        <td>
          {#if tx.credit_card_used}
            Credit Card ({tx.credit_card_name})
          {:else if tx.type === 'transfer'}
            {tx.transfer_from_account?.name} → {tx.transfer_to_account?.name}
          {:else}
            {tx.account?.name}
          {/if}
        </td>
      </tr>
    {/each}
  </tbody>
</table>

<style>
  .transaction-form {
    display: flex;
    flex-direction: column;
    max-width: 400px;
  }

  label {
    margin-bottom: 1em;
  }

  .success {
    color: green;
  }

  .error {
    color: red;
  }

  ul {
    list-style-type: none;
    padding-left: 0;
  }

  li {
    margin-bottom: 0.5em;
  }

  button {
    margin-left: 1em;
    color: red;
  }

  hr {
    margin: 2em 0;
  }

  .transaction-table {
    width: 100%;
    border-collapse: collapse;
  }

  .transaction-table th,
  .transaction-table td {
    border: 1px solid var(--border);
    padding: 0.5em 1em;
    text-align: left;
    background: var(--card);
    color: var(--foreground);
  }

  .transaction-table th {
    background: #fdfdfdb6;
    color: #000000;
    font-weight: 600;
  }

  .transaction-table tr:nth-child(even) td {
    background: #23272f;
  }

  .transaction-table tr:hover td {
    background: #282c34;
  }
</style>