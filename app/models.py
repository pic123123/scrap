from typing import List, Optional, Union, Dict, Any
from pydantic import BaseModel, HttpUrl, Field

class ProductRequest(BaseModel):
    url: HttpUrl = Field(..., description="The Amazon product URL to crawl")

class ProductResponse(BaseModel):
    title: str = Field(..., description="Product title")
    asin: Optional[str] = Field(None, description="Amazon Standard Identification Number")
    price: Optional[str] = Field(None, description="Current price")
    currency: Optional[str] = Field(None, description="Currency symbol/code")
    rating: Optional[str] = Field(None, description="Average customer rating")
    review_count: Optional[Union[str, int]] = Field(None, description="Number of ratings")
    availability: Optional[str] = Field(None, description="Stock status")
    
    brand: Optional[str] = Field(None, description="Brand name")
    model_name: Optional[str] = Field(None, description="Model name")
    breadcrumbs: List[str] = Field(default_factory=list, description="Category path")
    
    features: List[str] = Field(default_factory=list, description="Key features / Bullet points")
    specifications: Dict[str, Any] = Field(default_factory=dict, description="Technical specifications table")
    product_details: Dict[str, Any] = Field(default_factory=dict, description="Product details (Manufacturer, etc.)")
    
    description_summary: Optional[str] = Field(None, description="Summary of product description")
    full_description: Optional[str] = Field(None, description="Full product description")
    
    best_sellers_rank: List[str] = Field(default_factory=list, description="Best Sellers Rank info")
    warranty_info: Optional[str] = Field(None, description="Warranty information")
    
    image_url: Optional[str] = Field(None, description="Main product image URL")
    images: List[str] = Field(default_factory=list, description="List of product image URLs (Main & Gallery, from #altImages)")
    
    # New fields for separated content
    brand_story_images: List[str] = Field(default_factory=list, description="Images from 'From the brand' section")
    manufacturer_images: List[str] = Field(default_factory=list, description="Images from 'From the manufacturer' (aplus-v2) section")
    
    description_images: List[str] = Field(default_factory=list, description="Legacy field for other description images")
    videos: List[str] = Field(default_factory=list, description="List of video URLs found")
    
    usage: Dict[str, int] = Field(default_factory=dict, description="Token usage statistics (input, output, total)")
