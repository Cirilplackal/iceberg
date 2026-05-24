"use client";

import { useRef, useEffect, useState } from "react";
import {
  BookOpen,
  Brain,
  Loader2,
  Send,
  ShieldCheck,
  Sparkles,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { SourceCard } from "@/components/SourceCard";
import { PanelHeader } from "@/components/PanelHeader";
import { PipelineSteps } from "@/components/PipelineSteps";
import { StatusIndicator } from "@/components/StatusIndicator";
import { askIceberg } from "@/services/rag";
import type { Source } from "@/types/rag";

type Message = {
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
};

const SUGGESTED_PROMPTS = [
  {
    label: "Summarize findings",
    prompt: "Summarize the key findings across my documents",
  },
  {
    label: "Risk analysis",
    prompt: "What are the main risks and concerns mentioned?",
  },
  {
    label: "Cross-document themes",
    prompt: "Compare themes and patterns across uploaded sources",
  },
];

export function ChatPanel() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [pipelineStep, setPipelineStep] = useState(0);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading, pipelineStep]);

  useEffect(() => {
    if (!loading) {
      setPipelineStep(0);
      return;
    }

    setPipelineStep(0);
    const t1 = setTimeout(() => setPipelineStep(1), 600);
    const t2 = setTimeout(() => setPipelineStep(2), 1400);

    return () => {
      clearTimeout(t1);
      clearTimeout(t2);
    };
  }, [loading]);

  async function handleSendMessage(text?: string) {
    const query = (text ?? input).trim();
    if (!query || loading) return;

    setMessages((prev) => [...prev, { role: "user", content: query }]);
    setInput("");
    setLoading(true);

    try {
      const { answer, sources } = await askIceberg(query);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: answer, sources },
      ]);
    } catch (error) {
      console.error(error);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Something went wrong. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="ai-surface ai-glow flex h-full flex-col overflow-hidden rounded-xl">
      <PanelHeader
        compact
        title="Research"
        badge={
          <StatusIndicator
            label={loading ? "Busy" : "Ready"}
            variant={loading ? "busy" : "idle"}
          />
        }
      />

      <div className="min-h-0 flex-1 overflow-y-auto overscroll-contain">
        <div className="space-y-4 px-4 py-3 pb-6">
          {messages.length === 0 && !loading && (
            <div className="flex min-h-[min(100%,280px)] flex-col justify-center py-4 lg:min-h-0">
              <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:gap-8">
                <div className="flex items-start gap-3 lg:max-w-xs lg:shrink-0">
                  <div className="ai-orb flex size-10 shrink-0 items-center justify-center rounded-xl border border-white/[0.08] bg-white/[0.04]">
                    <Sparkles className="size-5 text-zinc-500" />
                  </div>
                  <div>
                    <h3 className="text-sm font-medium text-zinc-300">
                      Ask your knowledge base
                    </h3>
                    <p className="mt-1 text-xs leading-relaxed text-zinc-500">
                      Grounded answers with ranked citations and similarity
                      scores.
                    </p>
                  </div>
                </div>
                <div className="grid flex-1 gap-1.5 sm:grid-cols-3">
                  {SUGGESTED_PROMPTS.map((item) => (
                    <button
                      key={item.label}
                      type="button"
                      onClick={() => handleSendMessage(item.prompt)}
                      className="rounded-lg border border-white/[0.06] bg-white/[0.02] px-3 py-2.5 text-left text-sm text-zinc-400 transition-colors hover:border-white/10 hover:bg-white/[0.04] hover:text-zinc-200"
                    >
                      {item.label}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {messages.map((message, index) => (
            <div key={index}>
              {message.role === "user" ? (
                <div className="flex justify-end">
                  <div className="max-w-[min(88%,42rem)] rounded-2xl rounded-br-sm border border-white/[0.08] bg-zinc-900/80 px-3.5 py-2.5 text-sm leading-relaxed text-zinc-200">
                    {message.content}
                  </div>
                </div>
              ) : (
                <div className="space-y-2.5">
                  <div className="flex items-center gap-2">
                    <div className="flex size-5 items-center justify-center rounded border border-white/[0.08] bg-white/[0.03]">
                      <Brain className="size-3 text-zinc-500" />
                    </div>
                    <span className="text-[11px] font-medium text-zinc-500">
                      Iceberg
                    </span>
                    <span className="inline-flex items-center gap-0.5 rounded border border-emerald-500/15 bg-emerald-500/5 px-1.5 py-px text-[10px] text-emerald-400/80">
                      <ShieldCheck className="size-2.5" />
                      Grounded
                    </span>
                  </div>

                  <div className="max-w-4xl rounded-2xl rounded-tl-sm border border-white/[0.06] bg-white/[0.02] px-3.5 py-3">
                    <p className="whitespace-pre-wrap text-sm leading-relaxed text-zinc-300">
                      {message.content}
                    </p>
                  </div>

                  {message.sources && message.sources.length > 0 && (
                    <div className="space-y-2">
                      <div className="flex items-center justify-between gap-2">
                        <div className="flex items-center gap-1.5 text-zinc-600">
                          <BookOpen className="size-3" />
                          <span className="text-[10px] font-medium uppercase tracking-wider">
                            Sources · {message.sources.length}
                          </span>
                        </div>
                        <span className="font-mono text-[10px] text-zinc-600">
                          avg{" "}
                          {(
                            message.sources.reduce((a, s) => a + s.score, 0) /
                            message.sources.length
                          ).toFixed(3)}
                        </span>
                      </div>
                      <div className="grid gap-2 lg:grid-cols-2 xl:grid-cols-3">
                        {message.sources.map((source, sourceIndex) => (
                          <SourceCard
                            key={`${source.filename}-${source.chunk_index}-${sourceIndex}`}
                            source={source}
                            rank={sourceIndex + 1}
                          />
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}

          {loading && (
            <div className="max-w-2xl space-y-3 rounded-lg border border-white/[0.06] bg-white/[0.02] p-3">
              <div className="flex items-center gap-2">
                <Loader2 className="size-3.5 animate-spin text-zinc-400" />
                <span className="text-shimmer text-sm">Running RAG pipeline</span>
              </div>
              <PipelineSteps activeStep={pipelineStep} />
            </div>
          )}

          <div ref={bottomRef} className="h-px shrink-0" aria-hidden />
        </div>
      </div>

      <div className="shrink-0 border-t border-white/[0.06] bg-zinc-950/90 px-3 py-2.5 backdrop-blur-sm">
        <div className="flex gap-2 rounded-lg border border-white/[0.06] bg-white/[0.02] p-1 pl-2.5 focus-within:border-white/10 focus-within:ai-glow-soft">
          <Textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSendMessage();
              }
            }}
            placeholder="Ask about your knowledge base…"
            rows={1}
            disabled={loading}
            className="min-h-[36px] flex-1 resize-none border-0 bg-transparent py-2 text-sm text-zinc-200 shadow-none placeholder:text-zinc-600 focus-visible:ring-0 disabled:opacity-50"
          />
          <Button
            onClick={() => handleSendMessage()}
            disabled={loading || !input.trim()}
            size="icon"
            variant="secondary"
            className="size-8 shrink-0 rounded-md bg-zinc-100 text-zinc-950 hover:bg-white disabled:opacity-30"
          >
            {loading ? (
              <Loader2 className="size-3.5 animate-spin" />
            ) : (
              <Send className="size-3.5" />
            )}
          </Button>
        </div>
      </div>
    </div>
  );
}
