import { KLFEnvelope } from "./types";
import { getHandler } from "./intent-registry";
import { InvalidEnvelopeError, RoutingError } from "./errors";
import { isValidEnvelope } from "./envelope";

export async function routeMessage(envelope: KLFEnvelope): Promise<any> {
  if (!isValidEnvelope(envelope)) {
    throw new InvalidEnvelopeError();
  }

  const handler = getHandler(envelope.intent);
  if (!handler) {
    throw new RoutingError(`No handler registered for intent "${envelope.intent}"`);
  }

  return await handler(envelope.payload, envelope.meta);
} 