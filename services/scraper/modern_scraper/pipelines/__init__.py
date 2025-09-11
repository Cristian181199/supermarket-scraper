"""
Pipelines Package

Contiene los pipelines modernos para procesamiento de datos scrapeados.
Incluye validación, enriquecimiento, y integración con base de datos.
"""

from .validation import ValidationPipeline, DuplicateDetectionPipeline
from .enrichment import EnrichmentPipeline, CategoryHierarchyPipeline
from .database import DatabasePipeline, AIIntegrationPipeline

__all__ = [
    'ValidationPipeline',
    'DuplicateDetectionPipeline', 
    'EnrichmentPipeline',
    'CategoryHierarchyPipeline',
    'DatabasePipeline',
    'AIIntegrationPipeline'
]
