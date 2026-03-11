"""Application orchestration layer."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.contracts import QualificationInput
from knowledge_base.adapter import KnowledgeBaseAdapter
from matching.adapter import MatchingAdapter
from personal_status.adapter import PersonalStatusAdapter
from personal_status.port import UserContext
from qualification.adapter import PreliminaryQualificationAdapter
from research.adapter import ResearchAdapter


@dataclass
class AppOrchestrator:
    """Facade used by Flask routes."""

    research_adapter: ResearchAdapter = field(default_factory=ResearchAdapter)
    knowledge_base_adapter: KnowledgeBaseAdapter = field(default_factory=KnowledgeBaseAdapter)
    matching_adapter: MatchingAdapter = field(default_factory=MatchingAdapter)
    qualification_adapter: PreliminaryQualificationAdapter = field(
        default_factory=PreliminaryQualificationAdapter
    )
    personal_status_adapter: PersonalStatusAdapter = field(default_factory=PersonalStatusAdapter)

    def get_index_context(self) -> dict[str, object]:
        return {"top_words": self.research_adapter.get_top_words(top_n=12)}

    def generate_wordcloud_image(self):
        return self.research_adapter.generate_wordcloud_image()

    def list_hobbies(self, search_text: str = ""):
        return self.knowledge_base_adapter.list_hobbies(search_text=search_text)

    def list_attributes(self):
        return self.knowledge_base_adapter.list_attributes()

    def qualify_activity(self, payload: QualificationInput) -> dict[str, object]:
        hobbies = self.knowledge_base_adapter.list_hobbies()
        canonical_names = [hobby.name for hobby in hobbies]
        match = self.matching_adapter.match_activity(payload.activity, canonical_names)

        hobby = self.knowledge_base_adapter.get_hobby_by_name(match.activity_name) if match.matched else None
        attributes = self.knowledge_base_adapter.get_activity_attributes(hobby)
        qualification = self.qualification_adapter.qualify(match.matched, attributes)

        user_context = UserContext(
            currently_active=payload.currently_active,
            previously_active=payload.previously_active,
            frequency=payload.frequency,
            personal_importance=payload.personal_importance,
            intends_to_resume=payload.intends_to_resume,
        )
        personal_status = self.personal_status_adapter.derive(qualification.status, user_context)

        return {
            "input": {
                "activity": payload.activity,
                "currently_active": payload.currently_active,
                "previously_active": payload.previously_active,
                "frequency": payload.frequency,
                "personal_importance": payload.personal_importance,
                "intends_to_resume": payload.intends_to_resume,
            },
            "match": {
                "matched": match.matched,
                "activity_name": match.activity_name,
                "match_type": match.match_type,
                "confidence": match.confidence,
            },
            "attributes": attributes,
            "qualification": {
                "status": qualification.status,
                "label": qualification.status,
                "preliminary": qualification.preliminary,
                "score": qualification.score,
                "support_strength": qualification.support_strength,
                "supporting_attributes": qualification.supporting_attributes,
                "missing_or_weak_attributes": qualification.missing_or_weak_attributes,
            },
            "explanation": qualification.explanation,
            "personal_status": personal_status.status,
            "personal_explanation": personal_status.explanation,
        }
