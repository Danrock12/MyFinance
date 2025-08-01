<script>
  import Accounts from '$lib/Accounts.svelte';
  import Transactions from '$lib/Transactions.svelte';

  let activeTab = 'accounts'; // default tab

  function selectTab(tab) {
    activeTab = tab;
  }
</script>

<nav>
  <button
    on:click={() => selectTab('accounts')}
    class:selected={activeTab === 'accounts'}
  >
    Accounts
  </button>
  <button
    on:click={() => selectTab('transactions')}
    class:selected={activeTab === 'transactions'}
  >
    Transactions
  </button>
</nav>

<style>
  button.selected {
    font-weight: bold;
    border-bottom: 2px solid blue;
  }
  nav {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
  }
</style>

{#if activeTab === 'accounts'}
  <Accounts />
{:else if activeTab === 'transactions'}
  <Transactions />
{/if}

