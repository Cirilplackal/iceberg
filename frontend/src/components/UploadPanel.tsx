"use client";

import { useRef, useState } from "react";
import { Check, FileUp, Loader2, Upload } from "lucide-react";
import { Button } from "@/components/ui/button";
import { PanelHeader } from "@/components/PanelHeader";

type UploadResponse = {
  filename: string;
  characters: number;
  total_chunks: number;
  embedding_dimension: number;
  status: string;
};

export function UploadPanel() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<UploadResponse | null>(null);
  const [dragOver, setDragOver] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  async function handleUpload() {
    if (!file) return;

    setLoading(true);
    setResponse(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) throw new Error("Upload failed");

      setResponse(await res.json());
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }

  function handleFileSelect(selected: File | undefined) {
    if (selected?.type === "application/pdf") {
      setFile(selected);
      setResponse(null);
    }
  }

  function formatBytes(bytes: number) {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  }

  return (
    <div className="ai-surface flex h-full min-h-0 flex-col overflow-hidden rounded-xl lg:sticky lg:top-0">
      <PanelHeader compact title="Documents" />

      <div className="flex min-h-0 flex-1 flex-col gap-3 overflow-y-auto p-3">
        <div
          role="button"
          tabIndex={0}
          onClick={() => inputRef.current?.click()}
          onKeyDown={(e) => e.key === "Enter" && inputRef.current?.click()}
          onDragOver={(e) => {
            e.preventDefault();
            setDragOver(true);
          }}
          onDragLeave={() => setDragOver(false)}
          onDrop={(e) => {
            e.preventDefault();
            setDragOver(false);
            handleFileSelect(e.dataTransfer.files[0]);
          }}
          className={`flex cursor-pointer flex-col items-center rounded-lg border border-dashed px-3 py-5 transition-colors ${
            dragOver
              ? "border-white/20 bg-white/[0.04]"
              : "border-white/[0.1] bg-white/[0.02] hover:border-white/15"
          }`}
        >
          <input
            ref={inputRef}
            type="file"
            accept=".pdf"
            className="hidden"
            onChange={(e) => handleFileSelect(e.target.files?.[0])}
          />
          <FileUp className="mb-2 size-4 text-zinc-500" />
          <p className="line-clamp-2 text-center text-xs text-zinc-400">
            {file ? file.name : "Drop PDF or browse"}
          </p>
          {file && (
            <p className="mt-1 font-mono text-[10px] text-zinc-600">
              {formatBytes(file.size)}
            </p>
          )}
        </div>

        <Button
          onClick={handleUpload}
          disabled={loading || !file}
          variant="secondary"
          className="h-8 w-full gap-1.5 rounded-lg bg-zinc-100 text-xs text-zinc-950 hover:bg-white disabled:opacity-30"
        >
          {loading ? (
            <>
              <Loader2 className="size-3.5 animate-spin" />
              Ingesting…
            </>
          ) : (
            <>
              <Upload className="size-3.5" />
              Ingest
            </>
          )}
        </Button>

        {response && (
          <div className="space-y-2 rounded-lg border border-white/[0.08] bg-white/[0.02] p-2.5">
            <div className="flex items-center gap-1.5 text-emerald-400/90">
              <Check className="size-3.5" />
              <span className="text-xs font-medium">Indexed</span>
            </div>
            <div className="grid grid-cols-2 gap-1.5 text-[10px]">
              <Metric label="Chunks" value={String(response.total_chunks)} />
              <Metric
                label="Chars"
                value={response.characters.toLocaleString()}
              />
              <Metric
                label="Dims"
                value={String(response.embedding_dimension)}
              />
              <Metric label="Store" value="Qdrant" />
            </div>
            <p className="truncate font-mono text-[10px] text-zinc-600">
              {response.filename}
            </p>
          </div>
        )}

        <p className="mt-auto text-[10px] leading-snug text-zinc-600">
          Extract → chunk (1k/200) → embed → index
        </p>
      </div>
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded border border-white/[0.05] bg-black/20 px-2 py-1.5">
      <p className="font-mono text-zinc-400">{value}</p>
      <p className="text-zinc-600">{label}</p>
    </div>
  );
}
