"use client";

import React, { useState } from "react";

interface Props {
  onSubmit: (url: string) => void;
  loading: boolean;
}

export default function UrlForm({ onSubmit, loading }: Props) {
  const [url, setUrl] = useState("");

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (url.trim()) onSubmit(url.trim());
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <input
        type="url"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="https://example.com/page"
        required
        className="flex-1 border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <button
        type="submit"
        disabled={loading}
        className="bg-blue-600 text-white px-4 py-2 rounded text-sm font-medium hover:bg-blue-700 disabled:opacity-50"
      >
        {loading ? "Analyzing…" : "Analyze"}
      </button>
    </form>
  );
}
