import React, { useState } from "react";

interface DiffEntry {
  op: "add" | "remove" | "replace";
  path: string;
  before?: unknown;
  after?: unknown;
}

interface Props {
  diff: DiffEntry[] | null;
}

function opColor(op: DiffEntry["op"]) {
  return op === "add"
    ? "text-green-700 bg-green-50"
    : op === "remove"
    ? "text-red-700 bg-red-50"
    : "text-yellow-700 bg-yellow-50";
}

function opLabel(op: DiffEntry["op"]) {
  return op === "add" ? "ADD" : op === "remove" ? "REMOVE" : "CHANGE";
}

export default function JsonLdDiff({ diff }: Props) {
  const [expanded, setExpanded] = useState(false);

  if (!diff || diff.length === 0) {
    return (
      <div className="border border-gray-200 rounded-lg p-5">
        <h2 className="text-lg font-semibold mb-2">JSON-LD Changes</h2>
        <p className="text-sm text-gray-500">No changes from existing structured data.</p>
      </div>
    );
  }

  const visible = expanded ? diff : diff.slice(0, 5);

  return (
    <div className="border border-gray-200 rounded-lg p-5">
      <h2 className="text-lg font-semibold mb-3">
        JSON-LD Changes{" "}
        <span className="text-sm font-normal text-gray-500">({diff.length} operations)</span>
      </h2>
      <ul className="space-y-2">
        {visible.map((entry, i) => (
          <li key={i} className="text-sm font-mono">
            <span className={`inline-block text-xs font-bold px-1.5 py-0.5 rounded mr-2 ${opColor(entry.op)}`}>
              {opLabel(entry.op)}
            </span>
            <span className="text-gray-600">{entry.path}</span>
            {entry.op === "replace" && (
              <div className="ml-6 mt-1 space-y-0.5">
                <div className="text-red-600 line-through">{JSON.stringify(entry.before)}</div>
                <div className="text-green-700">{JSON.stringify(entry.after)}</div>
              </div>
            )}
            {entry.op === "add" && (
              <div className="ml-6 mt-1 text-green-700">{JSON.stringify(entry.after)}</div>
            )}
          </li>
        ))}
      </ul>
      {diff.length > 5 && (
        <button
          onClick={() => setExpanded(!expanded)}
          className="mt-3 text-xs text-blue-600 hover:underline"
        >
          {expanded ? "Show less" : `Show ${diff.length - 5} more…`}
        </button>
      )}
    </div>
  );
}
