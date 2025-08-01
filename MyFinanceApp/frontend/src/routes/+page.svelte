<script>
  // No logic needed for simple links
</script>

<style>
  :global(body) {
    background: #181a20;
    color: #f1f1f1;
    margin: 0;
    font-family: 'Inter', system-ui, sans-serif;
  }
  .main {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: inherit;
  }
  h1 {
    font-size: 2.5rem;
    margin-bottom: 3rem;
    font-weight: 700;
    letter-spacing: 1px;
    color: #fff;
    text-shadow: 0 2px 16px #0008;
  }
  .container {
    display: flex;
    gap: 2rem;
    justify-content: center;
    align-items: center;
  }
  .box {
    border: 2px solid #282c34;
    border-radius: 12px;
    padding: 2rem 3rem;
    text-align: center;
    font-size: 1.5rem;
    background: #23272f;
    color: #f1f1f1;
    cursor: pointer;
    transition: box-shadow 0.2s, border-color 0.2s, background 0.2s;
    min-width: 180px;
    box-shadow: 0 2px 12px #0004;
  }
  .box:hover {
    box-shadow: 0 4px 24px #0070f355;
    border-color: #0070f3;
    background: #1a1d23;
  }
  a {
    text-decoration: none;
    color: inherit;
    display: block;
  }
</style>

<div class="main">
  <h1>Welcome to MyFinanceProject</h1>
  <div class="container">
    <a href="/accounts" class="box">
      Accounts
    </a>
    <a href="/transactions" class="box">
      Transactions
    </a>
  </div>
</div>