from typing import List
import asyncio
from fastapi import FastAPI, HTTPException
from app.models import ProductRequest, ProductResponse
from app.graph import app_workflow
import uvicorn

app = FastAPI(title="Amazon Product Crawler API", description="API to crawl Amazon products using LangGraph and Bedrock")

@app.post("/api/v1/product/info", response_model=List[ProductResponse])
async def get_product_info(request: ProductRequest):
    """
    Crawls an Amazon product page and returns structured data.
    """
    async def process_url(url: str):
        initial_state = {
            "url": str(url),
            "html_content": None,
            "clean_text": None,
            "product_data": None,
            "error": None
        }
        
        # Run the workflow
        final_state = await app_workflow.ainvoke(initial_state)
        
        if final_state.get("error"):
            # Instead of raising http exception immediately, we might want to return the error
            # For now, let's log it or return a partial result? 
            # The prompt implies we want to handle list input. 
            # If one fails, we probably shouldn't fail all.
            # But the user rule says "return structured data".
            # Let's assume we return successfully processed ones or handle errors gracefully?
            # Or raise 500 if one fail? 
            # "Exception handling: network error ... try-except".
            # Let's return None or an error object if possible, but the response model is ProductResponse.
            # If we strictly follow ProductResponse, we might need a dummy object or change response model to allow errors.
            # However, looking at ProductResponse, it has many Optional fields.
            # Let's try to return what we have.
            print(f"Error processing {url}: {final_state['error']}")
            return None 

        return final_state.get("product_data")

    # Process all URLs concurrently
    results = await asyncio.gather(*(process_url(url) for url in request.urls))
    
    # Filter out None results or handle them. 
    # If we want to return helpful errors for specific URLs, we would need a wrapper model.
    # For now, let's return the successful ones.
    successful_results = [r for r in results if r is not None]
    
    if not successful_results and request.urls:
         # If all failed, raise an error
         raise HTTPException(status_code=500, detail="Failed to process all provided URLs")
         
    return successful_results

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
