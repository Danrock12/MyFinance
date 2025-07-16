export async function getTransactions() {
    const res = await fetch("http://localhost:8000/transactions");
    return res.json();
}

export async function getAccounts() {
  const res = await fetch("http://localhost:8000/accounts");
  return res.json();
}

export async function testBackendConnection() {
  const res = await fetch("http://localhost:8000/test-connection");
  return res.json();
}
