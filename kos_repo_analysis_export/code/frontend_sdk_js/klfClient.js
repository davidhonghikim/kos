export default class KLFClient {
  constructor({ serverUrl, token, onReply }) {
    this.serverUrl = serverUrl;
    this.token = token;
    this.onReply = onReply || (() => {});
  }

  async sendIntent(intent, payload, from = "ui.frontend", to = "agent.local") {
    const envelope = {
      id: crypto.randomUUID(),
      intent,
      from,
      to,
      issued_at: Math.floor(Date.now() / 1000),
      payload,
    };

    const res = await fetch(`${this.serverUrl}/admin/klf/send`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${this.token}`,
      },
      body: JSON.stringify(envelope),
    });

    const data = await res.json();
    this.onReply(data);
    return data;
  }

  setToken(newToken) {
    this.token = newToken;
  }

  updateServer(url) {
    this.serverUrl = url;
  }
} 