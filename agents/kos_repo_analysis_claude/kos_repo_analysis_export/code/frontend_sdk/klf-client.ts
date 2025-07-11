import { createEnvelope, isValidEnvelope } from "../klf_core/envelope";
import { KLFIntent, KLFEnvelope } from "../klf_core/types";
import { sendOverHTTP } from "./transport";
import { storeEnvelope, getEnvelope } from "./storage";

export class KLFClient {
  from: string;
  to: string;

  constructor(agentId: string, targetId: string) {
    this.from = agentId;
    this.to = targetId;
  }

  async send(intent: KLFIntent, payload: any, meta?: Partial<KLFEnvelope["meta"]>) {
    const envelope = createEnvelope(intent, payload, this.from, this.to, meta);
    await storeEnvelope(envelope);
    return sendOverHTTP(envelope);
  }

  async retrieve(id: string): Promise<KLFEnvelope | null> {
    return await getEnvelope(id);
  }
} 