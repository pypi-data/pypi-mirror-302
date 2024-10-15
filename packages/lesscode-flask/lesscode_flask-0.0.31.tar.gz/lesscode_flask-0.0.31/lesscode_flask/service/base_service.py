import logging

from flask_login import current_user

from lesscode_flask.db import db
from lesscode_flask.model.base_model import BaseModel
from lesscode_flask.utils.helpers import serialize_result_to_dict, parameter_validation, alchemy_result_to_dict

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

    def get_items(self, select_columns: list = None, order_columns: list = None, filters: list = None, offset: int = 0,
                  size: int = 10):
        """
        获取列表信息
        :param select_columns:
        :param order_columns:
        :param filters:
        :param offset:
        :param size:
        :return:
        """
        query = self.model.query
        if filters:
            query = query.filter(*filters)
        if order_columns:
            query = query.order_by(*order_columns)
        if offset > 0:
            query = query.offset(offset).limit(size)
        if select_columns:
            query = query.with_entities(*select_columns)
            data = alchemy_result_to_dict(query.all())
        else:
            data = serialize_result_to_dict(query.all())
        return data

    def delete_item(self, id: str):
        return self.model.query.filter_by(id=id).delete()

    def delete_items(self, filters: list):
        if filters and len(filters) > 0:
            return self.model.query.filter(*filters).delete()
        return 0

    def page(self, select_columns: list = None, columns: list = None, order_columns: list = None, filters: list = None,
             page_num: int = 1,
             page_size: int = 10):
        """
        分页查询
        :param select_columns:
        :param columns:
        :param order_columns:
        :param filters:
        :param page_num:
        :param page_size:
        :return:
        """
        query = self.model.query
        if filters:
            query = query.filter(*filters)
        if order_columns:
            query = query.order_by(*order_columns)
        if select_columns:
            query = query.with_entities(*select_columns)

        pagination = query.paginate(page=page_num, per_page=page_size)
        # 获取当前页的数据
        items = pagination.items
        # 获取分页信息
        total = pagination.total
        has_prev = pagination.has_prev
        has_next = pagination.has_next
        if select_columns:
            data = alchemy_result_to_dict(items)
        else:
            data = serialize_result_to_dict(items)
        result = {"columns": columns, "dataSource": data, "total": total,
                  "has_prev": has_prev,
                  "has_next": has_next}
        if columns:
            result["columns"] = columns
        return result
