import { UploadPanel } from "@/components/UploadPanel";
import { ChatPanel } from "@/components/ChatPanel";
import { StatusIndicator } from "@/components/StatusIndicator";

const STACK = ["Gemini 2.5", "Qdrant", "MiniLM", "RAG"];

export default function HomePage() {
  return (
    <div className="ai-ambient relative flex h-dvh flex-col overflow-hidden bg-[#09090b]">
      <div className="ai-grid pointer-events-none absolute inset-0 opacity-40" aria-hidden />

      <header className="relative z-10 shrink-0 border-b border-white/[0.06] px-4 py-2.5 lg:px-6">
        <div className="flex items-center justify-between gap-4">
          <div className="flex min-w-0 items-center gap-3">
            <div className="ai-orb flex size-8 shrink-0 items-center justify-center rounded-lg border border-white/[0.08] bg-white/[0.04]">
              <div className="size-1.5 rounded-full bg-zinc-400" />
            </div>
            <div className="min-w-0">
              <div className="flex items-center gap-2">
                <h1 className="truncate text-sm font-semibold text-zinc-100">
                  Iceberg AI
                </h1>
                <span className="shrink-0 font-mono text-[10px] text-zinc-600">
                  v0.1
                </span>
              </div>
              <p className="hidden truncate text-[11px] text-zinc-600 sm:block">
                Grounded RAG · top-k 3 · threshold 0.7
              </p>
            </div>
          </div>

          <div className="flex shrink-0 items-center gap-2">
            <div className="hidden items-center gap-1 md:flex">
              {STACK.map((item) => (
                <span
                  key={item}
                  className="rounded border border-white/[0.06] bg-white/[0.02] px-1.5 py-0.5 text-[10px] text-zinc-600"
                >
                  {item}
                </span>
              ))}
            </div>
            <StatusIndicator label="Online" variant="online" />
          </div>
        </div>
      </header>

      <main className="relative z-10 grid min-h-0 flex-1 grid-cols-1 gap-3 p-3 lg:grid-cols-[minmax(240px,22%)_minmax(0,1fr)] lg:gap-4 lg:p-4 xl:grid-cols-[minmax(260px,20%)_minmax(0,1fr)]">
        <aside className="flex min-h-0 flex-col lg:max-h-full">
          <UploadPanel />
        </aside>

        <section className="flex min-h-0 min-w-0 flex-col">
          <ChatPanel />
        </section>
      </main>
    </div>
  );
}
