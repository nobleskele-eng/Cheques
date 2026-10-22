// PostToolUse (Write|Edit) hook: warns Claude when MASTER.md goes over its size cap.
// Exit 2 sends the message back to Claude so it trims the file in the same turn.
import { statSync } from 'node:fs';

const CAP = 8000;
let input = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', (c) => { input += c; });
process.stdin.on('end', () => {
  let file = '';
  try { file = JSON.parse(input).tool_input?.file_path || ''; } catch { return; }
  if (!/(^|[\\/])MASTER\.md$/i.test(file)) return;
  let size = 0;
  try { size = statSync(file).size; } catch { return; }
  if (size <= CAP) return;
  process.stderr.write(`MASTER.md is ${size} bytes, over the ${CAP}-byte cap. Cut stale or low-value lines (move detail to reports/, research/ or docs/; git history keeps the old text) until it fits.\n`);
  process.exit(2);
});
