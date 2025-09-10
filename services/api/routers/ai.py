"""
AI router for embeddings, recommendations, and advanced AI features.
"""
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Optional

from shared.database import get_db
from shared.database.services.product_service import product_service
from shared.ai.embeddings.generator import embedding_generator

router = APIRouter()

@router.get("/status")
async def ai_status():
    """
    Get AI system status and capabilities.
    """
    return {
        'embedding_generator': {
            'available': embedding_generator.is_available(),
            'model': embedding_generator.model,
            'dimension': embedding_generator.dimension
        },
        'features': {
            'semantic_search': embedding_generator.is_available(),
            'product_recommendations': embedding_generator.is_available(),
            'text_analysis': True,
            'batch_processing': True
        }
    }

@router.post("/generate-embeddings")
async def generate_embeddings(
    background_tasks: BackgroundTasks,
    batch_size: int = Query(50, ge=1, le=200, description="Number of products to process"),
    db: Session = Depends(get_db)
):
    """
    Generate embeddings for products that don't have them.
    This is processed in the background to avoid timeout.
    """
    if not embedding_generator.is_available():
        raise HTTPException(
            status_code=503,
            detail="AI embedding service is not available. Please check OpenAI API configuration."
        )
    
    # Process synchronously for small batches, background for large ones
    if batch_size <= 10:
        result = product_service.generate_missing_embeddings(db, batch_size)
        return {
            'status': 'completed',
            'result': result
        }
    else:
        background_tasks.add_task(
            _generate_embeddings_background, 
            batch_size
        )
        return {
            'status': 'processing',
            'message': f'Generating embeddings for up to {batch_size} products in background',
            'batch_size': batch_size
        }

async def _generate_embeddings_background(batch_size: int):
    """Background task for generating embeddings."""
    from shared.database.config import db_manager
    
    with db_manager.get_session() as db:
        result = product_service.generate_missing_embeddings(db, batch_size)
        print(f"Background embedding generation completed: {result}")

@router.post("/update-search-texts")
async def update_search_texts(
    db: Session = Depends(get_db)
):
    """
    Update search_text field for products that don't have it.
    This improves text search performance.
    """
    try:
        updated_count = product_service.update_search_texts(db)
        return {
            'status': 'completed',
            'updated_products': updated_count,
            'message': f'Updated search text for {updated_count} products'
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update search texts: {str(e)}"
        )

@router.post("/create-vector-indexes")
async def create_vector_indexes(
    db: Session = Depends(get_db)
):
    """
    Create vector indexes for better search performance.
    Requires at least 1000 products with embeddings.
    """
    try:
        success = product_service.create_vector_indexes(db)
        if success:
            return {
                'status': 'completed',
                'message': 'Vector indexes created successfully'
            }
        else:
            return {
                'status': 'skipped',
                'message': 'Not enough products with embeddings (need at least 1000)'
            }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create vector indexes: {str(e)}"
        )

@router.get("/recommendations/{product_id}")
async def get_ai_recommendations(
    product_id: int,
    limit: int = Query(10, ge=1, le=50, description="Number of recommendations"),
    db: Session = Depends(get_db)
):
    """
    Get AI-powered product recommendations based on embeddings similarity.
    """
    if not embedding_generator.is_available():
        raise HTTPException(
            status_code=503,
            detail="AI recommendation service is not available"
        )
    
    try:
        recommendations = product_service.get_similar_products(db, product_id, limit)
        
        if not recommendations:
            raise HTTPException(
                status_code=404,
                detail="Product not found or no embeddings available"
            )
        
        return {
            'product_id': product_id,
            'recommendations': recommendations,
            'algorithm': 'vector_similarity',
            'model_used': embedding_generator.model,
            'count': len(recommendations)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate recommendations: {str(e)}"
        )

@router.get("/analytics")
async def get_ai_analytics(
    db: Session = Depends(get_db)
):
    """
    Get analytics about AI features usage and data coverage.
    """
    from shared.database.repositories.product import product_repository
    from sqlalchemy import func
    from shared.database.models.product import Product
    
    # Get statistics
    total_products = product_repository.count(db)
    products_with_embeddings = db.query(func.count(Product.id)).filter(
        Product.embedding.is_not(None)
    ).scalar()
    
    products_with_search_text = db.query(func.count(Product.id)).filter(
        Product.search_text.is_not(None)
    ).scalar()
    
    embedding_coverage = (products_with_embeddings / total_products * 100) if total_products > 0 else 0
    search_text_coverage = (products_with_search_text / total_products * 100) if total_products > 0 else 0
    
    return {
        'total_products': total_products,
        'ai_coverage': {
            'products_with_embeddings': products_with_embeddings,
            'embedding_coverage_percent': round(embedding_coverage, 2),
            'products_with_search_text': products_with_search_text,
            'search_text_coverage_percent': round(search_text_coverage, 2)
        },
        'ai_status': {
            'embedding_service_available': embedding_generator.is_available(),
            'model': embedding_generator.model,
            'ready_for_vector_indexes': products_with_embeddings >= 1000
        }
    }
