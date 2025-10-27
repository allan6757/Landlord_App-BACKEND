# Pagination Utility
# Provides consistent pagination across all list endpoints

from flask import request

def paginate_query(query, schema):
    """
    Paginate a SQLAlchemy query and return formatted results
    
    Args:
        query: SQLAlchemy query object
        schema: Marshmallow schema for serialization
        
    Returns:
        Dictionary with paginated data and metadata
    """
    # Get pagination parameters from request (default: page 1, 10 items per page)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Limit per_page to prevent excessive data requests
    per_page = min(per_page, 100)  # Maximum 100 items per page
    
    # Execute pagination query
    paginated = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False  # Don't raise error if page is out of range
    )
    
    # Serialize the items using the provided schema
    items = schema.dump(paginated.items, many=True)
    
    # Return paginated response with metadata
    return {
        'items': items,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total_items': paginated.total,
            'total_pages': paginated.pages,
            'has_next': paginated.has_next,
            'has_prev': paginated.has_prev,
            'next_page': page + 1 if paginated.has_next else None,
            'prev_page': page - 1 if paginated.has_prev else None
        }
    }

def get_pagination_params():
    """
    Extract and validate pagination parameters from request
    
    Returns:
        Tuple of (page, per_page)
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Ensure valid values
    page = max(1, page)  # Page must be at least 1
    per_page = min(max(1, per_page), 100)  # Between 1 and 100
    
    return page, per_page
