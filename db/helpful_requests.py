from db.engine import SessionFactory
from db.models import User, UserRate


class DBUtilities:
    @classmethod
    def get_all_user_ids(cls) -> list[int]:
        with SessionFactory() as session:
            query_result = session.query(User.id).all()
            return [user.id for user in query_result]

    @classmethod
    def get_rates_for_user(cls, user_id: int, only_non_nullable: bool = True) -> list[UserRate]:
        with SessionFactory() as session:
            query = session.query(UserRate).filter(UserRate.user_id == user_id)
            if only_non_nullable:
                query = query.filter(UserRate.rate.isnot(None))
            query_result = query.all()
            return [UserRate(rate.user_id, rate.title_id, rate.rate) for rate in query_result]

    @classmethod
    def add_entities(cls, entities):
        with SessionFactory() as session:
            for entity in entities:
                session.add(entity)
            session.commit()
