"""
Search router with AI-powered search capabilities.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from shared.database import get_db
from shared.database.services.product_service import product_service

router = APIRouter()

@router.get("/")
async def search_products(
    q: str = Query(..., min_length=1, max_length=200, description="Search query"),
    store_id: Optional[int] = Query(None, description="Filter by store ID"),
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    use_ai: bool = Query(True, description="Enable AI-powered semantic search"),
    limit: int = Query(20, ge=1, le=100, description="Number of results to return"),
    db: Session = Depends(get_db)
):
    """
    Search products using text and/or AI semantic search.
    
    This endpoint combines traditional text search with AI-powered semantic search
    for more relevant and intelligent results.
    """
    try:
        results = product_service.search_products(
            db, q.strip(),
            store_id=store_id,
            category_id=category_id,
            use_ai=use_ai,
            limit=limit
        )
        
        return {
            **results,
            'metadata': {
                'query_length': len(q),
                'filters_applied': {
                    'store_id': store_id,
                    'category_id': category_id
                }
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(e)}"
        )

@router.get("/suggestions")
async def get_search_suggestions(
    q: str = Query(..., min_length=1, max_length=100, description="Partial query for suggestions"),
    store_id: Optional[int] = Query(None, description="Filter by store ID"),
    limit: int = Query(10, ge=1, le=20, description="Number of suggestions"),
    db: Session = Depends(get_db)
):
    """
    Get search suggestions based on partial query.
    Uses product names and categories to provide autocomplete suggestions.
    """
    from shared.database.repositories.product import product_repository
    from sqlalchemy import func, or_
    from shared.database.models.product import Product
    
    # Search in product names and search_text
    suggestions_query = db.query(Product.name).filter(
        or_(
            Product.name.ilike(f"%{q}%"),
            Product.search_text.ilike(f"%{q}%")
        )
    )
    
    if store_id:
        suggestions_query = suggestions_query.filter(Product.store_id == store_id)
    
    suggestions = suggestions_query.distinct().limit(limit).all()
    
    return {
        'query': q,
        'suggestions': [suggestion[0] for suggestion in suggestions],
        'count': len(suggestions)
    }

@router.get("/text-only")
async def search_products_text_only(
    q: str = Query(..., min_length=1, max_length=200, description="Search query"),
    store_id: Optional[int] = Query(None, description="Filter by store ID"),
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    limit: int = Query(20, ge=1, le=100, description="Number of results to return"),
    db: Session = Depends(get_db)
):
    """
    Text-only search without AI semantic search.
    Faster but less intelligent than the main search endpoint.
    """
    from shared.database.repositories.product import product_repository
    
    products = product_repository.search_by_text(
        db, q.strip(),
        store_id=store_id,
        category_id=category_id,
        limit=limit
    )
    
    return {
        'query': q,
        'search_type': 'text_only',
        'total_results': len(products),
        'products': [product.to_dict() for product in products],
        'ai_available': False
    }
