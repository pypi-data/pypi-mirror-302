import json
from typing import Optional

from sqlalchemy.sql.type_api import _T

from lesscode_flask.db import db


class BaseModel(db.Model):
    __abstract__ = True
    __bind_key__ = 'default'


    # def to_dict(self):
    #     return {c.name: getattr(self, c.name) for c in self.__table__.columns}


from sqlalchemy import TypeDecorator, VARCHAR, Dialect


class JSONEncodedDict(TypeDecorator):
    """数据字段存储为json格式字符串 ，进行互转"""

    def process_literal_param(self, value: Optional[_T], dialect: Dialect) -> str:
        pass

    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value

