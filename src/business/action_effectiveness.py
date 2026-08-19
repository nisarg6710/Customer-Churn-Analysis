RETENTION_PROBABILITIES = {
    "Personalized SMS campaign": 0.20,
    "Personalized engagement campaign": 0.25,
    "Personalized retention call": 0.45,

    "Discounted data pack": 0.40,
    "Premium discounted data pack": 0.50,

    "Recharge incentive": 0.40,
    "Premium recharge incentive": 0.50,

    "Loyalty offer": 0.45,
    "High-value loyalty offer": 0.50,

    "Minimal intervention": 0.10,
    "No intervention": 0.0,
}


def get_retention_probability(action):
    return RETENTION_PROBABILITIES.get(
        action,
        0.0
    )