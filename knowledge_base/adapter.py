"""Knowledge-base adapter for read-only access to existing ORM queries.

Phase 1 transition layer: delegate to current SQLAlchemy model queries without
changing behavior.
"""

from __future__ import annotations

from dataclasses import dataclass

from models import Attribute, Hobby


@dataclass
class KnowledgeBaseAdapter:
    """Thin pass-through adapter over existing hobby/attribute queries."""

    def list_hobbies(self, search_text: str = "") -> list[Hobby]:
        """Return hobbies with optional case-insensitive name filtering."""
        query = Hobby.query
        if search_text:
            query = query.filter(Hobby.name.ilike(f"%{search_text}%"))
        return query.all()

    def list_attributes(self) -> list[Attribute]:
        """Return attributes ordered by name."""
        return Attribute.query.order_by(Attribute.name).all()
