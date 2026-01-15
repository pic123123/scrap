from fastapi import FastAPI, HTTPException
from app.models import ProductRequest, ProductResponse
from app.graph import app_workflow
import uvicorn

app = FastAPI(title="Amazon Product Crawler API", description="API to crawl Amazon products using LangGraph and Bedrock")

@app.post("/api/v1/product/info", response_model=ProductResponse)
async def get_product_info(request: ProductRequest):
    """
    Crawls an Amazon product page and returns structured data.
    """
    initial_state = {
        "url": str(request.url),
        "html_content": None,
        "clean_text": None,
        "product_data": None,
        "error": None
    }
    
    # Run the workflow
    final_state = await app_workflow.ainvoke(initial_state)
    
    if final_state.get("error"):
        raise HTTPException(status_code=500, detail=final_state["error"])
        
    if not final_state.get("product_data"):
         raise HTTPException(status_code=404, detail="Could not extract product data")
         
    return final_state["product_data"]

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
