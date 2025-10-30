<script lang="ts">
  import { page } from '$app/stores';
  $: current = $page.url.pathname;
</script>

<nav class="menu-bar">
  <a href="/" aria-label="Home" class="icon-link">
    🏠
  </a>
  <a href="/accounts" class={current === '/accounts' ? 'active' : ''}>Accounts</a>
  <a href="/transactions" class={current === '/transactions' ? 'active' : ''}>Transactions</a>
  <a href="/financial-report" class={current === '/financial-report' ? 'active' : ''}>Financial Report</a>
  <!-- Add more tabs as needed -->
</nav>

<style>
  .menu-bar {
    display: flex;
    gap: 2em;
    align-items: center;
    background: var(--card);
    padding: 1em 2em;
    border-bottom: 2px solid var(--border);
    margin-bottom: 2em;
  }
  .icon-link {
    font-size: 1.5em;
    text-decoration: none;
    color: var(--accent);
    margin-right: 1em;
  }
  a {
    color: var(--foreground);
    text-decoration: none;
    font-weight: 500;
    padding: 0.25em 0.5em;
    border-radius: 6px;
    transition: background 0.2s;
  }
  a.active, a:hover {
    background: var(--accent);
    color: #fff;
  }
</style>