import { openDB } from "idb";
import { KLFEnvelope } from "../klf_core/types";

const DB_NAME = "klf-client-db";
const STORE_NAME = "envelopes";

export async function getDB() {
  return await openDB(DB_NAME, 1, {
    upgrade(db) {
      if (!db.objectStoreNames.contains(STORE_NAME)) {
        db.createObjectStore(STORE_NAME, { keyPath: "id" });
      }
    },
  });
}

export async function storeEnvelope(env: KLFEnvelope) {
  const db = await getDB();
  await db.put(STORE_NAME, env);
}

export async function getEnvelope(id: string): Promise<KLFEnvelope | null> {
  const db = await getDB();
  return (await db.get(STORE_NAME, id)) || null;
} 