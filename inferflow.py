# inferflow.py
from celery import Celery
from pydantic import BaseModel
from flow import understand_flows  # Ensure this is correctly imported
import asyncio
import logging
from knowledge_graph import KnowledgeGraph
import os
from dotenv import load_dotenv

load_dotenv(verbose=True, override=True)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

BROKER_URL = os.getenv("BROKER_URL")
celery = Celery('KnowledgeGraph', broker=BROKER_URL)

class FlowInferenceRequest(BaseModel):
    project_id: int
    directory: str
    user_id: str

@celery.task(name="knowledgegraph.task.infer_flows", queue="infer_flow_requests")
def infer_flows(project_id: int, directory: str, user_id: str):
    logger.debug(f"Task received with project_id: {project_id}, directory: {directory}, user_id: {user_id}")
    try:
        request = FlowInferenceRequest(project_id=project_id, directory=directory, user_id=user_id)
        logger.debug(f'infer_flows task started with request: {request}')
        
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                logger.debug("Event loop is already running. Creating a new event loop.")
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            else:
                logger.debug("Using the existing event loop.")
        except RuntimeError:
            logger.debug("No event loop, creating a new one.")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        loop.run_until_complete(understand_flows(request.project_id, request.directory, request.user_id))
        
        return True
    except Exception as e:
        logger.error(f"Error in infer_flows task: {e}")
        return False
