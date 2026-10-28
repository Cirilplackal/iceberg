import type { ReactNode } from "react";

type Props = {
  title: string;
  description?: string;
  badge?: ReactNode;
  meta?: ReactNode;
  compact?: boolean;
};

export function PanelHeader({
  title,
  description,
  badge,
  meta,
  compact = false,
}: Props) {
  return (
    <div
      className={`shrink-0 border-b border-white/[0.06] px-4 ${compact ? "py-2.5" : "py-3"}`}
    >
      <div className="flex items-center justify-between gap-3">
        <div className="min-w-0">
          <h2 className="truncate text-sm font-medium text-zinc-200">{title}</h2>
          {description && !compact && (
            <p className="mt-0.5 truncate text-xs text-zinc-500">{description}</p>
          )}
        </div>
        {badge}
      </div>
      {meta && <div className={compact ? "mt-2" : "mt-2.5"}>{meta}</div>}
    </div>
  );
}
