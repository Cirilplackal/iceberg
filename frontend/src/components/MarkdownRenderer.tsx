import ReactMarkdown from "react-markdown";

import remarkGfm from "remark-gfm";

type Props = {
  content: string;
};

export function MarkdownRenderer({ content }: Props) {
  return (
    <div className="prose prose-invert max-w-none">
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
    </div>
  );
}
