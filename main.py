from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from knowledge_graph import KnowledgeGraph
from dotenv import load_dotenv
import sentry_sdk
import os

load_dotenv(verbose=True, override=True)


if os.getenv("ENV") == "production" and os.getenv("isDevelopmentMode") == "disabled":
    sentry_sdk.init(
        dsn= os.getenv("SENTRY_KG_DSN"),
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
    )


app = FastAPI()
class QueryRequest(BaseModel):
    project_id: int
    query: str

@app.post("/query")
async def query_knowledge_graph(request: QueryRequest):
    try:
        knowledge_graph = KnowledgeGraph(request.project_id)
        result = knowledge_graph.query(request.query, request.project_id)
        print("returning result",result)
        return {"result": result}
    except Exception as e:
        print("error in query_knowledge_graph",e)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)
