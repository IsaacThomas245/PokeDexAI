const BASE_URL = import.meta.env.VITE_API_URL;

async function sendChatMessage(message) {
  const res = await fetch(`${BASE_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message })
  });

  if (!res.ok) {
    throw new Error("Backend error");
  }

  return await res.json();
}

export default { sendChatMessage };
