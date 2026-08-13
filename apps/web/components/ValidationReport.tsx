import React from "react";

interface ValidationError {
  field: string;
  message: string;
  severity: "error" | "warning";
}

interface Props {
  report: {
    valid: boolean;
    errors: ValidationError[];
    warnings: ValidationError[];
    iterations: number;
  } | null;
}

export default function ValidationReport({ report }: Props) {
  if (!report) return null;

  const allIssues = [
    ...(report.errors ?? []).map((e) => ({ ...e, severity: "error" as const })),
    ...(report.warnings ?? []).map((w) => ({ ...w, severity: "warning" as const })),
  ];

  return (
    <div className="border border-gray-200 rounded-lg p-5">
      <div className="flex items-center gap-2 mb-3">
        <h2 className="text-lg font-semibold">Validation</h2>
        <span
          className={`text-xs font-medium px-2 py-0.5 rounded-full ${
            report.valid
              ? "bg-green-100 text-green-700"
              : "bg-red-100 text-red-700"
          }`}
        >
          {report.valid ? "Passed" : "Failed"}
        </span>
        {report.iterations > 1 && (
          <span className="text-xs text-gray-400 ml-auto">
            {report.iterations} repair iterations
          </span>
        )}
      </div>
      {allIssues.length === 0 ? (
        <p className="text-sm text-gray-500">No issues found.</p>
      ) : (
        <ul className="space-y-1">
          {allIssues.map((issue, i) => (
            <li key={i} className="text-sm flex gap-2">
              <span
                className={`shrink-0 font-medium ${
                  issue.severity === "error" ? "text-red-600" : "text-yellow-600"
                }`}
              >
                {issue.severity === "error" ? "✗" : "⚠"}
              </span>
              <span className="text-gray-700">
                <span className="font-medium">{issue.field}: </span>
                {issue.message}
              </span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
