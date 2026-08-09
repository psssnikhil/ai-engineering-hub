#!/usr/bin/env node
/**
 * Scan docs/ for arXiv, YouTube, and common doc links → resources/*.md
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DOCS = path.join(__dirname, '../docs');
const RESOURCES = path.join(__dirname, '../resources');

const ARXIV = /https?:\/\/arxiv\.org\/[^\s)\]"']+/gi;
const YOUTUBE = /https?:\/\/(?:www\.)?(?:youtube\.com\/watch\?v=[\w-]+|youtu\.be\/[\w-]+)[^\s)\]"']*/gi;
const HTTP = /https?:\/\/[^\s)\]"']+/gi;

function walk(dir, files = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(p, files);
    else if (entry.name.endsWith('.md')) files.push(p);
  }
  return files;
}

function uniqueSorted(items) {
  return [...new Set(items)].sort();
}

function categorize(url) {
  if (/arxiv\.org/i.test(url)) return 'papers';
  if (/youtube\.com|youtu\.be/i.test(url)) return 'videos';
  if (/github\.com/i.test(url)) return 'tools';
  if (/langchain|pinecone|openai|anthropic|huggingface|docs\./i.test(url)) return 'tools';
  return 'other';
}

function main() {
  const allUrls = [];
  for (const file of walk(DOCS)) {
    const text = fs.readFileSync(file, 'utf-8');
    const matches = text.match(HTTP) || [];
    for (let url of matches) {
      url = url.replace(/[.,;:]+$/, '');
      if (!url.includes('github.io/ai-engineering-hub')) allUrls.push(url);
    }
  }

  const buckets = { papers: [], videos: [], tools: [], other: [] };
  for (const url of uniqueSorted(allUrls)) {
    buckets[categorize(url)].push(url);
  }

  fs.mkdirSync(RESOURCES, { recursive: true });

  writeList(path.join(RESOURCES, 'raw-extracted-links.md'), 'Raw Extracted Reference Links', [...buckets.papers, ...buckets.videos, ...buckets.tools, ...buckets.other.slice(0, 100)], 'Auto-extracted raw URLs from lesson files.');

  console.log(`Extracted: ${buckets.papers.length} papers, ${buckets.videos.length} videos, ${buckets.tools.length} tools to raw-extracted-links.md.`);
}

function writeList(filePath, title, urls, intro) {
  const lines = [
    `# ${title}`,
    '',
    intro,
    '',
    `_Auto-generated from lesson content. Edit freely and re-run \`npm run extract-resources\`._`,
    '',
  ];
  for (const url of urls) {
    lines.push(`- ${url}`);
  }
  lines.push('');
  fs.writeFileSync(filePath, lines.join('\n'));
}

main();
