<script lang="ts">
  import { onMount } from 'svelte';
  import { getAllAccounts, createAccount, updateAccount } from '$lib/api';

  interface Account {
    id: number;
    name: string;
    starting_balance: number;
  }

  let name = '';
  let startingBalance: number = 0;
  let successMessage = '';
  let errorMessage = '';
  let accounts: Account[] = [];
  let savingIds = new Set<number>();

  onMount(async () => {
    try {
      accounts = await getAllAccounts();
    } catch (err) {
      errorMessage = 'Error fetching accounts';
      console.error(err);
    }
  });

  async function handleSubmit() {
    successMessage = '';
    errorMessage = '';

    try {
      const result = await createAccount(name, startingBalance);
      successMessage = `Account "${result.name}" created!`;
      name = '';
      startingBalance = 0;
      accounts = [...accounts, result]; // Add to list
    } catch (err) {
      errorMessage = err.message;
    }
  }

  async function handleInputChange(account: Account, field: 'name' | 'starting_balance', value: string | number) {
    account[field] = field === 'starting_balance' ? parseFloat(value as string) : (value as string);
  }

  async function saveAccount(account: Account) {
    savingIds.add(account.id);
    successMessage = '';
    errorMessage = '';

    try {
      const updated = await updateAccount(account.id, account.name, account.starting_balance);
      accounts = accounts.map(a => (a.id === updated.id ? updated : a));
      successMessage = `Account "${updated.name}" saved successfully!`;
    } catch (err) {
      errorMessage = err.message;
    } finally {
      savingIds.delete(account.id);
    }
  }
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

{#if successMessage}
  <p class="success">{successMessage}</p>
{/if}

{#if errorMessage}
  <p class="error">{errorMessage}</p>
{/if}

<h1>Your Accounts</h1>

<ul>
  {#each accounts as account (account.id)}
    <li>
      <input
        type="text"
        bind:value={account.name}
        on:input={(e) => handleInputChange(account, 'name', e.target.value)}
      />
      <input
        type="number"
        step="0.01"
        bind:value={account.starting_balance}
        on:input={(e) => handleInputChange(account, 'starting_balance', e.target.value)}
      />
      <button on:click={() => saveAccount(account)} disabled={savingIds.has(account.id)}>
        {savingIds.has(account.id) ? 'Saving...' : 'Save'}
      </button>
    </li>
  {/each}
</ul>

<style>
  .account-form {
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
</style>

