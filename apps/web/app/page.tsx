"use client";

import { useState } from "react";
import UrlForm from "@/components/UrlForm";
import JsonLdDiff from "@/components/JsonLdDiff";
import ValidationReport from "@/components/ValidationReport";
import RationaleCard from "@/components/RationaleCard";

export default function Home() {
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(url: string) {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await fetch("/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      });
      if (!res.ok) throw new Error(await res.text());
      setResult(await res.json());
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="max-w-4xl mx-auto p-8">
      <h1 className="text-2xl font-bold mb-6">Structured Data Copilot</h1>
      <UrlForm onSubmit={handleSubmit} loading={loading} />
      {error && <p className="text-red-600 mt-4">{error}</p>}
      {result && (
        <div className="mt-8 space-y-6">
          <RationaleCard rationale={result.rationale} />
          <ValidationReport report={result.validation} />
          <JsonLdDiff diff={result.diff} />
        </div>
      )}
    </main>
  );
}
