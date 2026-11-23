import fs from "node:fs/promises";
import path from "node:path";
import Link from "next/link";
import { notFound } from "next/navigation";
const sources = { model: { file: "lib/pilot.ts", title: "Checkpoint 1 Shared pilot model and rules" }, controller: { file: "app/api/pilots/route.ts", title: "Checkpoint 2 Server validation and success branch" }, view: { file: "components/PilotForm.tsx", title: "Checkpoint 3 React form and error messages" } };
export default async function Checkpoint({ params }: { params: Promise<{ checkpoint: string }> }) {
  const { checkpoint } = await params;
  if (!(checkpoint in sources)) notFound();
  const item = sources[checkpoint as keyof typeof sources];
  const source = await fs.readFile(path.join(process.cwd(), item.file), "utf8");
  return <main className="lab"><Link href="/lab">← Lab overview</Link><h1>{item.title}</h1><p>Actual project source: <code>{item.file}</code>. Line numbers match the file.</p><nav>{Object.keys(sources).map(key => <Link key={key} href={`/lab/${key}`}>{key}</Link>)}</nav><div className="code-panel"><pre>{source.split("\n").map((line, i) => <span className="code-line" key={i}><span className="line-no">{i + 1}</span>{line || " "}</span>)}</pre></div></main>;
}
