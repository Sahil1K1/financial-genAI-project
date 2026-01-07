from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
import json
import uvicorn
from src.utils.logger import get_logger

logger = get_logger('api endpoints')

app = FastAPI(
    title="Financial Summary app",
    description="It will provide financial data summary",
    version="1.0.0"
)

OUTPUTS = Path('data/outputs')

@app.get('/')
async def root():
    return {
        "message": "Financial summary api",
        "version": "1.0.0",
        "endpoints":""
    }

@app.get('/health')
async def health_check():
    return {"STATUS":"healthy",
            "output":str(OUTPUTS.exists())
            }


@app.get('/summary')
async def summary_endpoint():
    """if llm_output.json file has something inside of it then this function will return the same if not then it will run pipeline2 first and return the output from that file"""
    llm_file_output = OUTPUTS / "llm_output.json"
    if llm_file_output.exists():
        try:
            with open(llm_file_output, 'r') as file:
                data = json.load(file)
                return JSONResponse(content=data)
        except Exception as e:
            logger.info('Error is : {e}')
            # raise FileNotFoundError()
            raise HTTPException(status_code=500, detail=f"Error is {e}")
    else:
        raise HTTPException(status_code=404, detail=f'No summaries found')
    

if __name__ == "__main__":
    uvicorn.run(
        "src.app:app",
        host='0.0.0.0',
        port=8000,
        reload=True,
        log_level='info'
    )