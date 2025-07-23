<script>
  import { page } from '$app/stores';
</script>

<nav>
  <a href="/" class:active={$page.url.pathname === '/'}>Home</a>
  <a href="/transactions" class:active={$page.url.pathname === '/transactions'}>Transactions</a>
  <a href="/accounts" class:active={$page.url.pathname === '/accounts'}>Accounts</a>
</nav>

<style>
  nav a {
    margin-right: 1rem;
    text-decoration: none;
    color: black;
  }
  .active {
    font-weight: bold;
    color: blue;
  }
</style>

<h1>Welcome to your Finance App</h1>
<p>Select a tab to get started:</p>

