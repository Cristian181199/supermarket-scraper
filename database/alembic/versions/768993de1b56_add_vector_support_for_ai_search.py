"""Add vector support for AI search

Revision ID: 768993de1b56
Revises: 38b2e008c07a
Create Date: 2025-09-10 18:46:27.357139

"""
from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


# revision identifiers, used by Alembic.
revision = '768993de1b56'
down_revision = '38b2e008c07a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add new columns for AI and enhanced search capabilities
    
    # Enhanced product information
    op.add_column('products', sa.Column('description', sa.Text(), nullable=True))
    op.add_column('products', sa.Column('nutritional_info', sa.JSON(), nullable=True))
    
    # Availability and stock information
    op.add_column('products', sa.Column('in_stock', sa.String(20), nullable=False, server_default='unknown'))
    op.add_column('products', sa.Column('availability_text', sa.String(), nullable=True))
    
    # AI and Vector Search fields
    op.add_column('products', sa.Column('embedding', Vector(1536), nullable=True))
    op.add_column('products', sa.Column('embedding_model', sa.String(50), nullable=True))
    op.add_column('products', sa.Column('embedding_updated_at', sa.DateTime(), nullable=True))
    
    # Search optimization
    op.add_column('products', sa.Column('search_text', sa.Text(), nullable=True))
    op.add_column('products', sa.Column('search_vector', Vector(1536), nullable=True))
    
    # Enhanced metadata
    op.add_column('products', sa.Column('last_price_update', sa.DateTime(), nullable=True))
    op.add_column('products', sa.Column('scrape_count', sa.Numeric(10, 0), nullable=False, server_default='1'))
    
    # Add indexes for performance
    op.create_index('ix_products_search_text', 'products', ['search_text'])
    op.create_index('ix_products_in_stock', 'products', ['in_stock', 'store_id'])
    op.create_index('ix_products_store_category', 'products', ['store_id', 'category_id'])
    op.create_index('ix_products_price_range', 'products', ['price_amount', 'store_id'])
    
    # Vector similarity search indexes (will be created after data is populated)
    # These require the ivfflat extension which needs data to build the index
    # op.execute('CREATE INDEX ix_products_embedding_vector ON products USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100)')
    # op.execute('CREATE INDEX ix_products_search_vector ON products USING ivfflat (search_vector vector_cosine_ops) WITH (lists = 100)')
    
    # Full-text search index using GIN
    op.execute('CREATE INDEX ix_products_search_text_gin ON products USING gin(to_tsvector(\'english\', search_text))')


def downgrade() -> None:
    # Remove indexes
    op.drop_index('ix_products_search_text_gin', 'products')
    # op.drop_index('ix_products_search_vector', 'products')
    # op.drop_index('ix_products_embedding_vector', 'products')
    op.drop_index('ix_products_price_range', 'products')
    op.drop_index('ix_products_store_category', 'products')
    op.drop_index('ix_products_in_stock', 'products')
    op.drop_index('ix_products_search_text', 'products')
    
    # Remove columns
    op.drop_column('products', 'scrape_count')
    op.drop_column('products', 'last_price_update')
    op.drop_column('products', 'search_vector')
    op.drop_column('products', 'search_text')
    op.drop_column('products', 'embedding_updated_at')
    op.drop_column('products', 'embedding_model')
    op.drop_column('products', 'embedding')
    op.drop_column('products', 'availability_text')
    op.drop_column('products', 'in_stock')
    op.drop_column('products', 'nutritional_info')
    op.drop_column('products', 'description')
