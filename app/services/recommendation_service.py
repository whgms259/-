from sqlalchemy.orm import Session
from typing import List
from . import grade_service
from ..models.pydantic.recommendation import Recommendation

# Simple rule-based "AI" for recommendations
RECOMMENDATION_THRESHOLD = 80
RECOMMENDATION_REASON = f"Score is below {RECOMMENDATION_THRESHOLD}."

def get_recommendations_for_user(db: Session, *, user_id: int) -> List[Recommendation]:
        """
        Generates learning recommendations for a user based on their grades.
        """
        user_grades = grade_service.get_grades_by_user(db=db, user_id=user_id)
        
        recommendations = []
        for grade in user_grades:
            if grade.score < RECOMMENDATION_THRESHOLD:
                recommendations.append(
                    Recommendation(
                        subject=grade.subject,
                        reason=RECOMMENDATION_REASON
                    )
                )
        
        return recommendations
