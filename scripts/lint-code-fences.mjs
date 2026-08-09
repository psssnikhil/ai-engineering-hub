// Lint: every opening code fence in docs/ must declare a language.
// Allowed languages are listed below; ASCII diagrams and program output use `text`.
// Usage: node scripts/lint-code-fences.mjs   (exit 1 on violations)
import { readFileSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";

const ALLOWED = new Set([
  "python", "bash", "text", "json", "yaml", "mermaid",
  "markdown", "dockerfile", "javascript", "typescript", "sql", "toml", "diff", "console",
]);

function* mdFiles(dir) {
  for (const name of readdirSync(dir)) {
    const p = join(dir, name);
    if (statSync(p).isDirectory()) yield* mdFiles(p);
    else if (name.endsWith(".md")) yield p;
  }
}

let errors = 0;
for (const file of mdFiles("docs")) {
  const lines = readFileSync(file, "utf8").split("\n");
  let inFence = false;
  lines.forEach((line, i) => {
    const m = line.match(/^\s*```(\S*)\s*$/);
    if (!m) return;
    if (!inFence) {
      inFence = true;
      const lang = m[1];
      if (!lang) {
        console.error(`${file}:${i + 1}: unlabeled code fence — use \`\`\`text for diagrams/output`);
        errors++;
      } else if (!ALLOWED.has(lang)) {
        console.error(`${file}:${i + 1}: unknown fence language "${lang}" — add to ALLOWED in scripts/lint-code-fences.mjs if intentional`);
        errors++;
      }
    } else {
      inFence = false;
    }
  });
  if (inFence) {
    console.error(`${file}: unclosed code fence`);
    errors++;
  }
}

if (errors) {
  console.error(`\n${errors} fence problem(s).`);
  process.exit(1);
}
console.log("All code fences labeled and closed.");
