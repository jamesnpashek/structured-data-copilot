import React from "react";

interface Props {
  rationale: {
    summary: string;
    schema_types: string[];
    key_decisions: string[];
  } | null;
}

export default function RationaleCard({ rationale }: Props) {
  if (!rationale) return null;
  return (
    <div className="border border-gray-200 rounded-lg p-5">
      <h2 className="text-lg font-semibold mb-2">Rationale</h2>
      <p className="text-sm text-gray-700 mb-3">{rationale.summary}</p>
      {rationale.schema_types?.length > 0 && (
        <p className="text-xs text-gray-500 mb-2">
          <span className="font-medium">Schema types: </span>
          {rationale.schema_types.join(", ")}
        </p>
      )}
      {rationale.key_decisions?.length > 0 && (
        <ul className="list-disc list-inside text-sm text-gray-700 space-y-1">
          {rationale.key_decisions.map((d, i) => (
            <li key={i}>{d}</li>
          ))}
        </ul>
      )}
    </div>
  );
}
