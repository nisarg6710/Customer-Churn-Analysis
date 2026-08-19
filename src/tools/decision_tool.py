from src.decision_engine.next_best_action import (
    RetentionDecisionEngine
)


engine = RetentionDecisionEngine()


def get_next_best_action(customer):

    return engine.recommend(customer)