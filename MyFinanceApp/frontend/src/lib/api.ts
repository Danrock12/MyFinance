export async function getTransactions() {
    const res = await fetch("http://localhost:8000/transactions");
    return res.json();
}

export async function getAccounts() {
  const res = await fetch("http://localhost:8000/accounts");
  return res.json();
}

export async function createAccount(name: string, starting_balance: number) {
  const response = await fetch('http://127.0.0.1:8000/accounts/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, starting_balance }),
  });

  if (!response.ok) {
    throw new Error(`Failed to create account: ${response.statusText}`);
  }

  return await response.json();
}

export async function getAllAccounts() {
  const response = await fetch('http://127.0.0.1:8000/accounts/');
  if (!response.ok) throw new Error("Failed to fetch accounts");
  return response.json();
}

export async function updateAccount(id: number, name: string, starting_balance: number) {
  const response = await fetch(`http://127.0.0.1:8000/accounts/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, starting_balance }),
  });

  if (!response.ok) {
    throw new Error(`Failed to update account: ${response.statusText}`);
  }
  return await response.json();
}
