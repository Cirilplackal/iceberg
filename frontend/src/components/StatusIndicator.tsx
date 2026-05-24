type Props = {
  label?: string;
  variant?: "online" | "busy" | "idle";
};

export function StatusIndicator({
  label = "Online",
  variant = "online",
}: Props) {
  const dotColor =
    variant === "busy"
      ? "bg-amber-400/90"
      : variant === "idle"
        ? "bg-zinc-500"
        : "bg-emerald-400/90";

  return (
    <span className="inline-flex items-center gap-2 rounded-full border border-white/[0.08] bg-white/[0.03] px-2.5 py-1">
      <span className="relative flex size-1.5">
        {variant === "online" && (
          <span className="absolute inline-flex size-full animate-ping rounded-full bg-emerald-400/40" />
        )}
        <span className={`relative inline-flex size-1.5 rounded-full ${dotColor}`} />
      </span>
      <span className="text-[11px] font-medium text-zinc-400">{label}</span>
    </span>
  );
}
