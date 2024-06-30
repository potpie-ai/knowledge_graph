from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from flow import understand_flows
from knowledge_graph import KnowledgeGraph
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
class QueryRequest(BaseModel):
    project_id: str
    query: str

@app.post("/query")
async def query_knowledge_graph(request: QueryRequest):
    knowledge_graph = KnowledgeGraph(request.project_id)
    result = knowledge_graph.query(request.query, request.project_id)
    return {"result": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)
