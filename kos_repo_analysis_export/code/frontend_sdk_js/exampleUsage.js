import KLFClient from "./klfClient.js";

const client = new KLFClient({
  serverUrl: "http://localhost:8000",
  token: "dev-token-123",
  onReply: (res) => console.log("Response from agent:", res),
});

async function run() {
  await client.sendIntent("agent.ping", {});
  await client.sendIntent("echo", { msg: "Hello!" });
}

run(); 