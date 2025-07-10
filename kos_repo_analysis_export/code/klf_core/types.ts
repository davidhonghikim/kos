export type KLFIntent =
  | "agent.speak"
  | "agent.listen"
  | "agent.describe"
  | "agent.run"
  | "agent.reply"
  | "task.create"
  | "task.cancel"
  | "task.status"
  | "plugin.load"
  | "plugin.unload"
  | "admin.update"
  | "auth.login"
  | "auth.refresh"
  | "vault.read"
  | "vault.write"
  | string;

export interface KLFEnvelope {
  id: string;
  intent: KLFIntent;
  from: string;
  to: string;
  issued_at: number;
  payload: any;
  meta?: {
    auth?: {
      jwt?: string;
      signature?: string;
      publicKey?: string;
    };
    trace?: string[];
    version?: string;
    priority?: "low" | "normal" | "high";
  };
} 