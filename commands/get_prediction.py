import datetime
import logging
import random
import time

import sqlalchemy as sa
from sqlalchemy.exc import PendingRollbackError

from commands import Command
from db.engine import SessionFactory
from db.models import User, UserRate
from utils.client import ShikimoriClient
from utils.predictors.predictor import Predictor
from utils.settings import settings


class GetPredictionCommand(Command):
    def __init__(self, user_marks: list[UserRate]):
        self.user_marks = user_marks

    def execute(self):
        predictor = Predictor()

