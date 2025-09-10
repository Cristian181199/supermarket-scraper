"""
Products router with standard CRUD operations.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from shared.database import get_db
from shared.database.services.product_service import product_service

router = APIRouter()

@router.get("/")
async def get_products(
    skip: int = Query(0, ge=0, description="Number of products to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of products to return"),
    store_id: Optional[int] = Query(None, description="Filter by store ID"),
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    in_stock_only: bool = Query(False, description="Only show products in stock"),
    db: Session = Depends(get_db)
):
    """
    Get products with pagination and optional filters.
    """
    if store_id:
        return product_service.get_products_by_store(
            db, store_id,
            category_id=category_id,
            skip=skip, 
            limit=limit,
            in_stock_only=in_stock_only
        )
    else:
        # Get all products with filters
        filters = {}
        if category_id:
            filters['category_id'] = category_id
        if in_stock_only:
            filters['in_stock'] = 'in_stock'
        
        from shared.database.repositories.product import product_repository
        products = product_repository.get_multi(
            db, skip=skip, limit=limit, filters=filters
        )
        
        return {
            'products': [product.to_dict() for product in products],
            'total': product_repository.count(db, filters),
            'skip': skip,
            'limit': limit
        }

@router.get("/{product_id}")
async def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific product by ID.
    """
    from shared.database.repositories.product import product_repository
    product = product_repository.get(db, product_id)
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return product.to_dict()

@router.get("/{product_id}/similar")
async def get_similar_products(
    product_id: int,
    limit: int = Query(10, ge=1, le=50, description="Number of similar products"),
    db: Session = Depends(get_db)
):
    """
    Get products similar to the specified product using AI embeddings.
    """
    similar_products = product_service.get_similar_products(db, product_id, limit)
    
    if not similar_products:
        raise HTTPException(
            status_code=404, 
            detail="Product not found or no similar products available"
        )
    
    return {
        'product_id': product_id,
        'similar_products': similar_products,
        'count': len(similar_products)
    }

@router.get("/by-price-range/")
async def get_products_by_price_range(
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
    store_id: Optional[int] = Query(None, description="Filter by store ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get products within a specific price range.
    """
    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(
            status_code=400,
            detail="Minimum price cannot be greater than maximum price"
        )
    
    products = product_service.get_products_by_price_range(
        db, min_price, max_price,
        store_id=store_id, skip=skip, limit=limit
    )
    
    return {
        'products': products,
        'filters': {
            'min_price': min_price,
            'max_price': max_price,
            'store_id': store_id
        },
        'count': len(products)
    }
