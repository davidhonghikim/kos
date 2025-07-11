import { writeFileSync } from "fs";

export function generateIntentSchemas(intents: Record<string, any>) {
  Object.entries(intents).forEach(([intent, schema]) => {
    const jsonSchema = {
      $schema: "http://json-schema.org/draft-07/schema#",
      title: intent,
      type: "object",
      ...schema,
    };
    writeFileSync(`./schemas/${intent}.schema.json`, JSON.stringify(jsonSchema, null, 2));
  });
} 