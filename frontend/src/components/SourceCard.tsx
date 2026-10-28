import { FileText } from "lucide-react";
import type { Source } from "@/types/rag";

type Props = {
  source: Source;
  rank: number;
};

export function SourceCard({ source, rank }: Props) {
  const relevancePercent = Math.round(source.score * 100);

  return (
    <div className="rounded-lg border border-white/[0.06] bg-white/[0.02] p-2.5 transition-colors hover:border-white/10 hover:bg-white/[0.03]">
      <div className="flex items-start gap-2">
        <span className="flex size-5 shrink-0 items-center justify-center rounded border border-white/[0.08] font-mono text-[9px] text-zinc-600">
          {rank}
        </span>
        <div className="min-w-0 flex-1">
          <div className="flex items-start justify-between gap-2">
            <div className="flex min-w-0 items-center gap-1.5">
              <FileText className="size-3 shrink-0 text-zinc-600" />
              <p className="truncate text-xs text-zinc-300">{source.filename}</p>
            </div>
            <span className="shrink-0 font-mono text-[10px] text-zinc-500">
              {source.score.toFixed(2)}
            </span>
          </div>
          <div className="mt-1.5 h-px rounded-full bg-white/[0.06]">
            <div
              className="h-full rounded-full bg-zinc-500/50"
              style={{ width: `${relevancePercent}%` }}
            />
          </div>
          <p className="mt-1.5 line-clamp-2 text-[11px] leading-relaxed text-zinc-500">
            {source.preview}
          </p>
        </div>
      </div>
    </div>
  );
}
