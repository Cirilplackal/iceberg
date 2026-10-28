export type Source = {
  filename: string;

  chunk_index: number;

  score: number;

  preview: string;
};

export type RAGResponse = {
  answer: string;

  sources: Source[];
};
