import { useEffect, useRef, useState } from "react";
import { Sparkles, Send, Maximize2, Minimize2, Loader2 } from "lucide-react";

interface Message {
  role: "user" | "assistant";
  content: string;
}

const SESSION_ID = crypto.randomUUID();
const API_BASE = "http://localhost:8000";
const SUGGESTIONS = ["Highest gap region?", "Show trend analysis", "Give me a summary"];

// ---------------------------------------------------------------------------
// Inline markdown: **bold**, *italic*, `code`, [text](url), bare https URLs
// ---------------------------------------------------------------------------
const INLINE_RE =
  /(\[[^\]]+\]\(https?:\/\/[^)]+\)|https?:\/\/[^\s,)>\]]+|\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)/g;

function renderInline(text: string): React.ReactNode[] {
  return text.split(INLINE_RE).map((part, i) => {
    const mdLink = part.match(/^\[([^\]]+)\]\((https?:\/\/[^)]+)\)$/);
    if (mdLink)
      return (
        <a
          key={i}
          href={mdLink[2]}
          target="_blank"
          rel="noopener noreferrer"
          className="text-indigo-600 underline underline-offset-2 hover:text-indigo-800 break-all"
        >
          {mdLink[1]}
        </a>
      );
    if (/^https?:\/\//.test(part))
      return (
        <a
          key={i}
          href={part}
          target="_blank"
          rel="noopener noreferrer"
          className="text-indigo-600 underline underline-offset-2 hover:text-indigo-800 break-all"
        >
          {part}
        </a>
      );
    if (/^\*\*(.+)\*\*$/.test(part))
      return (
        <strong key={i} className="font-semibold text-gray-900">
          {part.slice(2, -2)}
        </strong>
      );
    if (/^\*(.+)\*$/.test(part))
      return (
        <em key={i} className="italic">
          {part.slice(1, -1)}
        </em>
      );
    if (/^`(.+)`$/.test(part))
      return (
        <code
          key={i}
          className="bg-indigo-50 text-indigo-700 px-1 py-0.5 rounded text-xs font-mono"
        >
          {part.slice(1, -1)}
        </code>
      );
    return <span key={i}>{part}</span>;
  });
}

// ---------------------------------------------------------------------------
// Block-level markdown renderer (headers, lists, paragraphs)
// ---------------------------------------------------------------------------
function AssistantMessage({ content }: { content: string }) {
  const lines = content.split("\n");
  const blocks: React.ReactNode[] = [];
  let i = 0;
  let key = 0;

  while (i < lines.length) {
    const line = lines[i];
    if (!line.trim()) {
      i++;
      continue;
    }
    const hMatch = line.match(/^(#{1,3})\s+(.+)/);
    if (hMatch) {
      const level = hMatch[1].length;
      const cls =
        level === 1
          ? "font-bold text-gray-900 text-base mt-3 mb-1"
          : level === 2
            ? "font-bold text-gray-900 text-sm mt-2 mb-1"
            : "font-semibold text-gray-800 text-sm mt-2 mb-0.5";
      blocks.push(
        <p key={key++} className={cls}>
          {renderInline(hMatch[2])}
        </p>
      );
      i++;
      continue;
    }
    if (/^---+$/.test(line.trim())) {
      blocks.push(<hr key={key++} className="border-gray-200 my-2" />);
      i++;
      continue;
    }
    if (/^[-*]\s/.test(line)) {
      const items: string[] = [];
      while (i < lines.length && /^[-*]\s/.test(lines[i])) {
        items.push(lines[i].replace(/^[-*]\s/, ""));
        i++;
      }
      blocks.push(
        <ul key={key++} className="list-disc list-outside pl-4 space-y-0.5 my-1">
          {items.map((item, j) => (
            <li key={j} className="text-sm text-gray-700">
              {renderInline(item)}
            </li>
          ))}
        </ul>
      );
      continue;
    }
    if (/^\d+[.)]\s/.test(line)) {
      const items: string[] = [];
      while (i < lines.length && /^\d+[.)]\s/.test(lines[i])) {
        items.push(lines[i].replace(/^\d+[.)]\s/, ""));
        i++;
      }
      blocks.push(
        <ol key={key++} className="list-decimal list-outside pl-4 space-y-0.5 my-1">
          {items.map((item, j) => (
            <li key={j} className="text-sm text-gray-700">
              {renderInline(item)}
            </li>
          ))}
        </ol>
      );
      continue;
    }
    blocks.push(
      <p key={key++} className="text-sm text-gray-700 leading-relaxed">
        {renderInline(line)}
      </p>
    );
    i++;
  }
  return <div className="space-y-1">{blocks}</div>;
}

// ---------------------------------------------------------------------------
// Typing / status indicator shown while the agent is working
// ---------------------------------------------------------------------------
function TypingIndicator({ status }: { status: string | null }) {
  return (
    <div className="flex justify-start">
      <div className="h-6 w-6 bg-indigo-100 rounded-full flex items-center justify-center shrink-0 mr-2 mt-0.5">
        <Sparkles className="h-3 w-3 text-indigo-600" />
      </div>
      <div className="bg-gray-50 border border-gray-100 rounded-xl px-3 py-2 flex items-center gap-2">
        {status ? (
          <>
            <Loader2 className="h-3 w-3 text-indigo-400 animate-spin shrink-0" />
            <span className="text-xs text-gray-500">{status}</span>
          </>
        ) : (
          <span className="text-sm text-gray-400 flex items-center gap-1">
            <span className="animate-bounce">●</span>
            <span className="animate-bounce [animation-delay:0.15s]">●</span>
            <span className="animate-bounce [animation-delay:0.3s]">●</span>
          </span>
        )}
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Main component
// ---------------------------------------------------------------------------
export function AskIntelligence() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [streaming, setStreaming] = useState(false);
  const [status, setStatus] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [expanded, setExpanded] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading, status]);

  const send = async (text: string) => {
    const message = text.trim();
    if (!message || loading || streaming) return;

    setMessages((prev) => [...prev, { role: "user", content: message }]);
    setInput("");
    setLoading(true);
    setError(null);
    setStatus(null);

    let bubbleAdded = false;

    try {
      const response = await fetch(`${API_BASE}/chat/stream`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message, session_id: SESSION_ID }),
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);

      const reader = response.body!.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() ?? "";

        for (const line of lines) {
          if (!line.startsWith("data: ")) continue;
          const raw = line.slice(6).trim();
          if (raw === "[DONE]") break;

          try {
            const parsed = JSON.parse(raw);

            if (parsed.error) throw new Error(parsed.error);

            // Tool-progress status — update the typing indicator label
            if (parsed.status) {
              setStatus(parsed.status);
            }

            // Real text chunk — add bubble on first chunk, then append
            if (parsed.t) {
              if (!bubbleAdded) {
                setMessages((prev) => [...prev, { role: "assistant", content: "" }]);
                bubbleAdded = true;
                setLoading(false);
                setStreaming(true);
                setStatus(null);
              }
              setMessages((prev) => {
                const msgs = [...prev];
                const last = msgs[msgs.length - 1];
                msgs[msgs.length - 1] = { ...last, content: last.content + parsed.t };
                return msgs;
              });
            }
          } catch (parseErr) {
            if (parseErr instanceof SyntaxError) continue; // incomplete JSON line
            throw parseErr;
          }
        }
      }
    } catch {
      // Clean up empty bubble if streaming never started
      if (!bubbleAdded) {
        setError("Failed to reach the AI. Make sure the API server is running.");
      }
    } finally {
      setLoading(false);
      setStreaming(false);
      setStatus(null);
    }
  };

  const busy = loading || streaming;

  const panel = (
    <div
      className={`bg-white border rounded-xl flex flex-col ${
        expanded ? "w-full max-w-2xl h-[80vh] shadow-2xl p-6" : "p-6"
      }`}
    >
      {/* Header */}
      <div className="flex items-start gap-3 mb-4">
        <div className="h-10 w-10 bg-indigo-600 rounded-full flex items-center justify-center shrink-0">
          <Sparkles className="h-5 w-5 text-white" />
        </div>
        <div className="flex-1">
          <h3 className="font-bold text-gray-900 mb-1">Ask Intelligence</h3>
          <p className="text-sm text-gray-500">Powered by EquiStat AI</p>
          <div className="mt-1 flex items-center gap-1 text-xs">
            <div className="h-2 w-2 bg-green-500 rounded-full" />
            <span className="text-green-600 font-medium">Online</span>
          </div>
        </div>
        <button
          onClick={() => setExpanded((v) => !v)}
          className="p-1.5 rounded-lg text-gray-400 hover:text-gray-600 hover:bg-gray-100 transition-colors"
          title={expanded ? "Collapse" : "Expand"}
        >
          {expanded ? <Minimize2 className="h-4 w-4" /> : <Maximize2 className="h-4 w-4" />}
        </button>
      </div>

      {/* Message thread */}
      <div className={`flex-1 overflow-y-auto space-y-3 mb-4 pr-1 ${expanded ? "" : "max-h-72"}`}>
        {messages.length === 0 && !loading && (
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-sm text-gray-700 leading-relaxed">
              Hello! I&apos;m your ParityMetrics AI assistant. I can help you analyze
              Rwanda&apos;s gender statistics, identify trends, and uncover regional disparities.
              What would you like to explore today?
            </p>
          </div>
        )}

        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
            {msg.role === "assistant" && (
              <div className="h-6 w-6 bg-indigo-100 rounded-full flex items-center justify-center shrink-0 mr-2 mt-0.5">
                <Sparkles className="h-3 w-3 text-indigo-600" />
              </div>
            )}
            <div
              className={`rounded-xl px-3 py-2 text-sm leading-relaxed ${
                msg.role === "user"
                  ? "max-w-[80%] bg-indigo-600 text-white"
                  : "flex-1 bg-gray-50 border border-gray-100"
              }`}
            >
              {msg.role === "user" ? msg.content : <AssistantMessage content={msg.content} />}
            </div>
          </div>
        ))}

        {/* Typing / status indicator — visible during tool calls AND while waiting for first chunk */}
        {loading && <TypingIndicator status={status} />}

        {error && <p className="text-xs text-red-500 text-center">{error}</p>}
        <div ref={bottomRef} />
      </div>

      {/* Suggestions */}
      {messages.length === 0 && !busy && (
        <div className="flex flex-wrap gap-2 mb-4">
          {SUGGESTIONS.map((s) => (
            <button
              key={s}
              onClick={() => send(s)}
              className="px-3 py-1.5 bg-white border border-gray-200 hover:border-indigo-300 hover:bg-indigo-50 rounded-lg text-xs text-gray-600 hover:text-indigo-600"
            >
              {s}
            </button>
          ))}
        </div>
      )}

      {/* Input */}
      <div className="relative">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && send(input)}
          placeholder="Ask about trends, gaps, forecasts..."
          disabled={busy}
          className="w-full px-4 py-3 pr-12 bg-white border border-gray-200 rounded-lg text-sm text-black focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent disabled:opacity-50"
        />
        <button
          onClick={() => send(input)}
          disabled={busy || !input.trim()}
          className="absolute right-2 top-1/2 -translate-y-1/2 h-8 w-8 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-40 rounded-lg flex items-center justify-center"
        >
          <Send className="h-4 w-4 text-white" />
        </button>
      </div>
    </div>
  );

  if (expanded) {
    return (
      <div
        className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
        onClick={(e) => e.target === e.currentTarget && setExpanded(false)}
      >
        {panel}
      </div>
    );
  }

  return panel;
}
