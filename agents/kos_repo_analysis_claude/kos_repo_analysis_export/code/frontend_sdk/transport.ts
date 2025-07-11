import { KLFEnvelope } from "../klf_core/types";

export async function sendOverHTTP(envelope: KLFEnvelope): Promise<any> {
  const res = await fetch("/api/klf", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(envelope.meta?.auth?.jwt ? { Authorization: `Bearer ${envelope.meta.auth.jwt}` } : {}),
    },
    body: JSON.stringify(envelope),
  });

  if (!res.ok) {
    throw new Error(`KLF transport error: ${res.status}`);
  }

  return await res.json();
} 