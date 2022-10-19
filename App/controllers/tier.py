from dataclasses import dataclass

from App.models import Profile


@dataclass
class Tier:
    tier: int
    tier_points: int
    views_left: int


# tuple -> points, views
tiers = {
    1: (0, 2),
    2: (4, 4),
    3: (6, 6),
    4: (8, 8),
    5: (10, 10)
}


def get_tier_views(tier: int) -> int:
    global tiers
    return tiers[tier][1]


def update_tier_information(profile: Profile):
    global tiers
    max_tier = len(tiers)

    profile.add_tier_point()
    current_tier = profile.tier

    if current_tier >= max_tier:
        return

    next_tier = current_tier + 1

    if profile.tier_points == tiers[next_tier][0]:
        profile.set_tier(next_tier)
        profile.set_views_left(tiers[next_tier][1])
