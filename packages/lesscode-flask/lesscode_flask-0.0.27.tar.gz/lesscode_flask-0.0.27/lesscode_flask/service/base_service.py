import logging

from flask_login import current_user
from lesscode_flask.db import db
from lesscode_flask.model.base_model import BaseModel
from lesscode_flask.utils.helpers import serialize_result_to_dict, parameter_validation

logger = logging.getLogger(__name__)


class BaseService:

    def __init__(self, model):
        self.model = model

    @staticmethod
    def add_item(item: BaseModel):
        """
        添加数据
        :param item: 待添加数据对象
        :return:
        """

        # try:
        #
        # except AttributeError:
        #     current_user = None
        try:
            if hasattr(item, "create_user_id"):
                item.create_user_id = current_user.id
            if hasattr(item, "create_user_name"):
                item.create_user_name = current_user.display_name
        except Exception as e:
            if hasattr(item, "create_user_id"):
                item.create_user_id = "AnonymousUserId"
            if hasattr(item, "create_user_name"):
                item.create_user_name = "匿名用户"
        db.session.add(item)
        db.session.commit()
        return item.id

    def add_items(self, items: list):
        """
        添加数据
        :param items: 待添加数据对象集合
        :return:
        """
        for item in items:
            try:
                if hasattr(item, "create_user_id"):
                    item.create_user_id = current_user.id
                if hasattr(item, "create_user_name"):
                    item.create_user_name = current_user.display_name
            except Exception as e:
                if hasattr(item, "create_user_id"):
                    item.create_user_id = "AnonymousUserId"
                if hasattr(item, "create_user_name"):
                    item.create_user_name = "匿名用户"
        db.session.execute(
            self.model.__table__.insert(),
            items
        )
        db.session.commit()
        return items

    def update_item(self, id: str, item: dict):

        try:
            if hasattr(self.model, "modify_user_id"):
                item["modify_user_id"] = current_user.id
            if hasattr(self.model, "modify_user_name"):
                item["modify_user_name"] = current_user.display_name
        except Exception as e:
            if hasattr(item, "modify_user_id"):
                item.create_user_id = "AnonymousUserId"
            if hasattr(item, "modify_user_name"):
                item.create_user_name = "匿名用户"
        self.model.query.filter_by(id=id).update(parameter_validation(item))
        db.session.commit()
        return id

    def get_item(self, id: str):
        """
        获取单条信息
        :param id:
        :return:
        """
        item = self.model.query.get(id)
        return item

    def get_one(self, filters: list):
        """
        获取单条信息
        :param filters:
        :return:
        """
        query = self.model.query
        if filters:
            query = query.filter(*filters)
        item = query.one()
        return item

    def get_items(self, filters: list = None):
        """
        获取列表信息
        :param filters:
        :return:
        """
        query = self.model.query
        if filters:
            query = query.filter(*filters)
        items = query.all()
        return items

    def delete_item(self, id: str):
        self.model.query.filter_by(id=id).delete()
        return id

    def delete_items(self, filters: list):
        if filters and len(filters) > 0:
            self.model.query.filter(*filters).delete()
        return id

    def page(self, columns: [], filters: list = None, page_num: int = 1, page_size: int = 10):
        query = self.model.query
        if filters:
            query = query.filter(*filters)
        pagination = query.paginate(page=page_num, per_page=page_size)
        # 获取当前页的数据
        items = pagination.items
        # 获取分页信息
        total = pagination.total
        has_prev = pagination.has_prev
        has_next = pagination.has_next
        result = {"columns": columns, "dataSource": serialize_result_to_dict(items), "total": total,
                  "has_prev": has_prev,
                  "has_next": has_next}
        return result
