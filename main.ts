import { copyFile, mkdir } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const destinationRoot = process.env.MAKEFUN_OUTPUT_DIR?.trim() || "/output";
const source = resolve(dirname(fileURLToPath(import.meta.url)), "entry.png");
const destination = join(destinationRoot, "entry.png");

async function publish() {
  try {
    await mkdir(dirname(destination), { recursive: true });
    await copyFile(source, destination);
    console.log(`Wrote ${destination}`);
  } catch (error) {
    const detail = error instanceof Error ? error.message : String(error);
    console.error(`Could not copy the bundled poster to ${destination}: ${detail}`);
    process.exitCode = 1;
  }
}

void publish();
