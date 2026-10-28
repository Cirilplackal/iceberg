import { Check, Loader2 } from "lucide-react";

const STEPS = [
  { id: "retrieve", label: "Vector retrieval" },
  { id: "context", label: "Context assembly" },
  { id: "generate", label: "LLM synthesis" },
] as const;

type Props = {
  activeStep: number;
};

export function PipelineSteps({ activeStep }: Props) {
  return (
    <div className="flex flex-wrap gap-2">
      {STEPS.map((step, index) => {
        const done = index < activeStep;
        const active = index === activeStep;

        return (
          <div
            key={step.id}
            className={`inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-[11px] transition-colors ${
              done
                ? "border-white/10 bg-white/[0.04] text-zinc-400"
                : active
                  ? "border-white/15 bg-white/[0.06] text-zinc-200 ai-glow-soft"
                  : "border-white/[0.05] bg-transparent text-zinc-600"
            }`}
          >
            {done ? (
              <Check className="size-3 text-zinc-500" />
            ) : active ? (
              <Loader2 className="size-3 animate-spin text-zinc-400" />
            ) : (
              <span className="size-3 rounded-full border border-zinc-700" />
            )}
            {step.label}
          </div>
        );
      })}
    </div>
  );
}
