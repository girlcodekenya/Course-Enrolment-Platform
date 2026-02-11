from sqlalchemy.orm import Query
from app.schemas.common import PaginatedResponse
from typing import TypeVar, Generic, List
from math import ceil

T = TypeVar('T')


def paginate(query: Query, page: int, page_size: int, model_class: type) -> PaginatedResponse:
    total = query.count()
    total_pages = ceil(total / page_size) if page_size > 0 else 0
    
    offset = (page - 1) * page_size
    items = query.offset(offset).limit(page_size).all()
    
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )