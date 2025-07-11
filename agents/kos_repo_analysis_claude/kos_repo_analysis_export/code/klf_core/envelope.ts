import { KLFEnvelope, KLFIntent } from "./types";
import { v4 as uuidv4 } from "uuid";

export function createEnvelope(
  intent: KLFIntent,
  payload: any,
  from: string,
  to: string,
  meta: Partial<KLFEnvelope["meta"]> = {}
): KLFEnvelope {
  return {
    id: uuidv4(),
    intent,
    from,
    to,
    issued_at: Date.now(),
    payload,
    meta,
  };
}

export function isValidEnvelope(env: any): env is KLFEnvelope {
  return (
    typeof env.id === "string" &&
    typeof env.intent === "string" &&
    typeof env.from === "string" &&
    typeof env.to === "string" &&
    typeof env.issued_at === "number" &&
    typeof env.payload !== "undefined"
  );
} 