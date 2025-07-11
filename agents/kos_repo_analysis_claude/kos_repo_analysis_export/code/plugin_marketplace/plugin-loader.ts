import fs from 'fs';
import path from 'path';
import axios from 'axios';

export async function downloadAndVerifyPlugin(url: string, id: string): Promise<void> {
  const pluginPath = path.resolve('plugins', id + '.js');
  const res = await axios.get(url);

  if (!res.data || typeof res.data !== 'string') {
    throw new Error('Invalid plugin data');
  }

  fs.writeFileSync(pluginPath, res.data, 'utf-8');
  console.log(`✅ Plugin ${id} installed at ${pluginPath}`);
} 