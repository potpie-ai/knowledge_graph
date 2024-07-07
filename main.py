from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from knowledge_graph import KnowledgeGraph
from dotenv import load_dotenv

load_dotenv(verbose=True, override=True)

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
