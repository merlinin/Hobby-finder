"""Knowledge-base adapter for read-only access to existing ORM queries."""

from __future__ import annotations

from dataclasses import dataclass

from models import Attribute, Hobby


@dataclass
class KnowledgeBaseAdapter:
    """Thin adapter over existing hobby/attribute queries."""

    def list_hobbies(self, search_text: str = "") -> list[Hobby]:
        """Return hobbies with optional case-insensitive name filtering."""
        query = Hobby.query
        if search_text:
            query = query.filter(Hobby.name.ilike(f"%{search_text}%"))
        return query.all()

    def list_attributes(self) -> list[Attribute]:
        """Return attributes ordered by name."""
        return Attribute.query.order_by(Attribute.name).all()

    def get_hobby_by_name(self, activity_name: str) -> Hobby | None:
        """Return hobby by exact canonical name."""
        return Hobby.query.filter_by(name=activity_name).first()

    def get_activity_attributes(self, hobby: Hobby | None) -> dict[str, int]:
        """Return a normalized attribute-name/value mapping for a hobby."""
        if hobby is None:
            return {}
        return {ha.attribute.name.lower(): ha.value for ha in hobby.attributes}
