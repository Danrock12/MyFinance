<script lang="ts">
  import { onMount } from 'svelte';
  import { formatMoney } from '$lib/formatMoney';

  // Form state
  let name = '';
  let startingBalance: number = 0;
  let successMessage = '';
  let errorMessage = '';

  // List state
  type Account = {
    id: number;
    name: string;
    starting_balance: number;
  };

  let accounts: Account[] = [];

  // Edit state
  let editingAccount: Account | null = null;
  let editBalance: number = 0;

  // Overview state
  let accountTotals: Record<string, number> = {};
  let overviewDate: string = new Date().toLocaleDateString();

  // Create new account
  async function handleSubmit() {
    successMessage = '';
    errorMessage = '';

    try {
      const res = await fetch('http://localhost:8000/accounts/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name,
          starting_balance: startingBalance,
        }),
      });

      if (!res.ok) throw new Error('Failed to create account');

      const newAccount = await res.json();
      successMessage = `Account "${newAccount.name}" created!`;
      name = '';
      startingBalance = 0;

      await fetchAccounts();
      await fetchAccountTotals();
    } catch (err) {
      errorMessage = err.message;
    }
  }

  // Fetch existing accounts
  async function fetchAccounts() {
    try {
      const res = await fetch('http://localhost:8000/accounts/');
      if (!res.ok) throw new Error('Failed to fetch accounts');
      accounts = await res.json();
    } catch (err) {
      errorMessage = err.message;
    }
  }

  // Fetch financial report for overview
  async function fetchAccountTotals() {
    try {
      const year = new Date().getFullYear();
      const res = await fetch(`http://localhost:8000/api/financial-report/${year}`);
      if (!res.ok) return;
      const data = await res.json();
      const monthIdx = new Date().getMonth();
      accountTotals = {};
      for (const acc of data.report) {
        let balance: number = 0;
        if (Array.isArray(acc.monthly_balances)) {
          if (monthIdx >= 0 && monthIdx < acc.monthly_balances.length) {
            balance = acc.monthly_balances[monthIdx] ?? 0;
          }
        } else if (typeof acc.monthly_balances === 'object' && acc.monthly_balances !== null) {
          balance = acc.monthly_balances[monthIdx] ?? 0;
        }
        accountTotals[acc.account_name] = balance;
      }
    } catch (err) {
      // Silently fail for overview
    }
  }

  // Start editing
  function startEdit(account: Account) {
    editingAccount = account;
    editBalance = account.starting_balance;
  }

  // Edit handler
  async function handleEdit() {
    if (!editingAccount) return;
    try {
      const res = await fetch(`http://localhost:8000/accounts/${editingAccount.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: editingAccount.name,
          starting_balance: editBalance,
        }),
      });
      if (!res.ok) throw new Error('Failed to update account');
      await fetchAccounts();
      await fetchAccountTotals();
      editingAccount = null;
      successMessage = 'Account updated!';
    } catch (err) {
      errorMessage = err.message;
    }
  }

  // Delete handler
  async function handleDelete(accountId: number) {
    const confirmed = confirm('Are you sure you want to delete this account?');
    if (!confirmed) return;
    try {
      const res = await fetch(`http://localhost:8000/accounts/${accountId}`, {
        method: 'DELETE',
      });
      if (!res.ok) throw new Error('Failed to delete account');
      await fetchAccounts();
      await fetchAccountTotals();
      successMessage = 'Account deleted!';
    } catch (err) {
      errorMessage = err.message;
    }
  }

  onMount(async () => {
    await fetchAccounts();
    await fetchAccountTotals();
  });
</script>

<h1>Create a New Account</h1>

<form on:submit|preventDefault={handleSubmit} class="account-form">
  <label>
    Account Name:
    <input type="text" bind:value={name} required />
  </label>

  <label>
    Starting Balance:
    <input type="number" bind:value={startingBalance} required step="0.01" />
  </label>

  <button type="submit">Create Account</button>
</form>

{#if editingAccount}
  <form on:submit|preventDefault={handleEdit} class="account-form">
    <label>
      Edit Balance for {editingAccount.name}:
      <input type="number" bind:value={editBalance} required step="0.01" />
    </label>
    <button type="submit">Save</button>
    <button type="button" on:click={() => editingAccount = null}>Cancel</button>
  </form>
{/if}

{#if successMessage}
  <p class="success">{successMessage}</p>
{/if}

{#if errorMessage}
  <p class="error">{errorMessage}</p>
{/if}

<hr />

<h2>Account Overview (as of {overviewDate})</h2>
<ul>
  {#each accounts as account}
    <li>
      <strong>{account.name}</strong>:
      {#if accountTotals[account.name] !== undefined}
        {formatMoney(accountTotals[account.name])}
      {:else}
        Loading...
      {/if}
    </li>
  {/each}
</ul>

<hr />

<h2>Accounts Starting Balances</h2>

{#if accounts.length === 0}
  <p>No accounts found.</p>
{:else}
  <ul>
    {#each accounts as account}
      <li>
        <strong>{account.name}</strong>: {formatMoney(account.starting_balance)}
        <button on:click={() => startEdit(account)}>Edit</button>
        <button on:click={() => handleDelete(account.id)}>Delete</button>
      </li>
    {/each}
  </ul>
{/if}

<style>
  .account-form {
    display: flex;
    flex-direction: column;
    max-width: 400px;
    background: var(--card);
    color: var(--foreground);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.5em;
    margin-bottom: 2em;
  }

  label {
    margin-bottom: 1em;
  }

  input[type="text"],
  input[type="number"] {
    background: var(--background);
    color: var(--foreground);
    border: 2px solid #1b5e20; /* green outline */
    border-radius: 6px;
    padding: 0.5em;
    font-size: 1em;
    outline: none;
    transition: border-color 0.2s, box-shadow 0.2s;
  }

  input[type="text"]:focus,
  input[type="number"]:focus {
    border-color: #4caf50; /* lighter green on focus */
    box-shadow: 0 0 0 2px #4caf50;
  }

  button {
    margin-left: 0.5em;
    margin-top: 0.5em;
    background: #1b5e20;
    color: #fff;
    border: none;
    border-radius: 6px;
    padding: 0.5em 1em;
    font-weight: bold;
    cursor: pointer;
    transition: background 0.2s;
  }
  button:hover {
    background: #388e3c;
  }

  .success {
    color: #4caf50;
  }

  .error {
    color: #ff5252;
  }

  ul {
    list-style-type: none;
    padding-left: 0;
    background: var(--card);
    color: var(--foreground);
    border-radius: 10px;
    border: 1px solid var(--border);
    margin-top: 1em;
    padding: 1em;
  }

  li {
    margin: 0.5em 0;
    padding: 0.5em 0;
    border-bottom: 1px solid var(--border);
  }
  li:last-child {
    border-bottom: none;
  }

  hr {
    margin: 2em 0;
    border-color: var(--border);
  }
</style>