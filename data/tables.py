import sqlalchemy
from .db_session import SqlAlchemyBase


class Table(SqlAlchemyBase):
    __tablename__ = 'tables'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    type = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    deck = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    legs = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    cost = sqlalchemy.Column(sqlalchemy.Integer)
    description = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    in_catalog = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)

    def __repr__(self):
        return f'<Table> {self.type} {self.deck} {self.legs}'
