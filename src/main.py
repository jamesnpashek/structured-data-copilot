from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl

from pipeline import run_pipeline

app = FastAPI(title="Structured Data Copilot", version="0.1.0")


class AnalyzeRequest(BaseModel):
    url: HttpUrl


@app.post("/api/analyze")
def analyze(body: AnalyzeRequest):
    try:
        result = run_pipeline(str(body.url))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
