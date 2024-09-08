from collections import defaultdict
from typing import NamedTuple

import scipy

from db.engine import SessionFactory
from db.helpful_requests import DBUtilities
from db.models import UserRate, User, Rate


class FormattedRates(NamedTuple):
    user1_rates: list[float]
    user2_rates: list[float]
    title_matching: dict[int, int]


class Prediction(NamedTuple):
    rate: float
    weight: float

    def __add__(self, other: 'Prediction') -> 'Prediction':
        weight = self.weight + other.weight
        return Prediction(
            rate=(self.rate * self.weight + other.rate * other.weight) / weight,
            weight=weight,
        )


class Predictor:
    def __init__(self, user_id: int, rates: list[Rate]):
        self.user_id: int = user_id
        self.user_rates: list[Rate] = rates
        self.normalized_user_rates = self.get_normalized_rates(
            [rate.rate for rate in rates]
        )
        self.predictions: defaultdict[int, Prediction] = defaultdict(lambda: Prediction(0, 0))

    def fit(self):
        other_users = DBUtilities.get_all_user_ids()
        for other_user in other_users:
            other_user_rates = DBUtilities.get_rates_for_user(other_user.id)
            self.update_predictions(other_user_rates)

    def predict(self) -> list[Rate]:
        predictions: list[Rate] = [Rate(title_id, prediction.rate) for title_id, prediction in self.predictions.items()]
        return sorted(predictions, key=lambda rate: -rate.rate)

    @classmethod
    def get_correlation(cls, list1: list, list2: list) -> float:
        return float(scipy.stats.pearsonr(list1, list2).statistic)

    @classmethod
    def get_normalized_rates(cls, rates: list[float], default_value: float = 1.0) -> list[float]:
        if not rates:
            return []
        min_rate = min(rates)
        max_rate = max(rates)
        if min_rate == max_rate:
            return [default_value] * len(rates)
        normalized_rates = [(rate - min_rate) / (max_rate - min_rate) for rate in rates]
        return normalized_rates

    @classmethod
    def format_rates(cls, user1_rates: list[Rate], user2_rates: list[Rate]) -> FormattedRates:
        user1_matching: dict[int, Rate] = {user_rate.title_id: user_rate for user_rate in user1_rates}
        user2_matching: dict[int, Rate] = {user_rate.title_id: user_rate for user_rate in user2_rates}
        common_titles: set[int] = set(user1_matching.keys() & user2_matching.keys())
        title_matching: dict[int, int] = {number: title_id for number, title_id in enumerate(common_titles)}
        user1_rates: list[float] = [user1_matching[title_id].rate for _, title_id in title_matching.items()]
        user2_rates: list[float] = [user2_matching[title_id].rate for _, title_id in title_matching.items()]
        return FormattedRates(user1_rates, user2_rates, title_matching)

    def update_predictions(self, other_user_rates: list[Rate]) -> None:
        formatted_rates = self.format_rates(self.user_rates, other_user_rates)
        if self.is_degenerate(formatted_rates.user1_rates) or self.is_degenerate(formatted_rates.user2_rates):
            return
        correlation = self.get_correlation(formatted_rates.user1_rates, formatted_rates.user2_rates)
        new_title_ids = (
                {user_rate.title_id for user_rate in other_user_rates}
                - {user_rate.title_id for user_rate in self.user_rates}
        )
        other_user_matching: dict[int, Rate] = {user_rate.title_id: user_rate for user_rate in other_user_rates}
        new_titles_other_user_rates: list[float] = [
            other_user_matching[new_title_id].rate for new_title_id in new_title_ids
        ]
        normalized_other_user_rates: list[float] = self.get_normalized_rates(new_titles_other_user_rates)
        new_title_rates: list[Rate] = [
            Rate(title_id, rate) for title_id, rate in zip(new_title_ids, normalized_other_user_rates)
        ]
        self._update_predictions(new_title_rates, correlation, len(formatted_rates.title_matching))

    def _update_predictions(self, other_user_rates: list[Rate], correlation: float, intersect_count: int) -> None:
        for rate in other_user_rates:
            self.predictions[rate.title_id] = Prediction(
                rate=correlation * rate.rate,
                weight=intersect_count,
            )

    @classmethod
    def is_degenerate(cls, lst: list[float]):
        return len(set(lst)) < 2
