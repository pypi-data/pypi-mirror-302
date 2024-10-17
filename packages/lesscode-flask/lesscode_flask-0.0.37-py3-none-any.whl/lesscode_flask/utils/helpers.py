class app_config:

    @staticmethod
    def get(key, default=None):
        """
        获取配置
        :param key: 配置key
        :param default: 默认值
        :return:
        """
        from flask import current_app
        return current_app.config.get(key, default)


def serialize_result_to_dict(result):
    """
    结果对象序列化为字典
    :param result:
    :return:
    """
    if isinstance(result, list):
        return [serialize_result_to_dict(r) for r in result]
    if not hasattr(result, "__dict__"):
        return result
    return {k: v for k, v in result.__dict__.items() if not k.startswith('_')}


def alchemy_result_to_dict(result):
    """
    alchemy 指定字段查询后返回的数据解析为字典
    :param result:
    :return:
    """
    data_list = []
    if not result:
        return result
    if isinstance(result, list):
        key_list = list(result[0]._fields)
        for d in result:
            dict_data = dict(zip(key_list, d))
            data_list.append(dict_data)
        return data_list
    else:
        if result:
            key_list = list(result._fields)
            return dict(zip(key_list, result))
        else:
            return {}


def generate_uuid():
    """
    生成UUID
    :return:
    """
    import uuid
    return uuid.uuid4().hex.replace("-", "")


def get_start_port():
    """
    获取启动端口
    :return:
    """
    import sys
    arg_list = sys.argv
    for a in arg_list:
        if "--port" in a:
            return a.split("=")[1]
    return "5000"


def parameter_validation(obj: dict):
    """
    验证参数对象中非None的键值
    :return:
    """
    return {k: v for k, v in obj.items() if v}


def parse_boolean(s):
    """
    将字符串转换为布尔值。
    :param s: 待转换的字符串
    :return:
    """
    s = str(s)
    s = s.strip().lower()
    if s in ("yes", "true", "on", "1"):
        return True
    # elif s in ("no", "false", "off", "0", "none"):
    #     return False
    else:
        # 其余不在判断全返False
        return False


def inject_args(req, func, view_args={}):
    import inspect

    """
    实现参数自动注入
    :param req: 请求对象
    :param func: 请求处理函数
    :param view_args: 路径上获取的参数
    :return:
    """
    jsons = {}
    args = req.args
    form = req.form
    files = req.files
    if req.mimetype == 'application/json' and req.json is not None:
        jsons = req.json
    # 合并args、form和json参数字典
    arguments = dict(**args, **form, **jsons, **files, **view_args)
    # 获取处理方法的 参数签名
    parameters = inspect.signature(func).parameters.items()
    # 获取所有参数名称
    parameter_names = [parameter_name for parameter_name, parameter in parameters]
    kwargs = {}
    # 检查传入的参数中 哪些不在参数列表中，单独存储
    for key in arguments.keys():
        if key not in parameter_names:
            kwargs[key] = arguments[key]
    params_dict = {}
    # parameterName 参数名称, parameter 参数对象
    for parameter_name, parameter in parameters:
        print("parameter_name",parameter_name, parameter)
        # 依据参数名称，获取请求参数值
        argument_value = arguments.get(parameter_name)
        # 兼容**kwargs 参数
        if parameter.kind == inspect.Parameter.VAR_KEYWORD:
            argument_value = kwargs
        if argument_value is not None:
            # 获取形参类型
            parameter_type = parameter.annotation
            # 形参类型为空，尝试获取形参默认值类型
            if parameter_type is inspect.Parameter.empty:
                parameter_type = type(parameter.default)
            if parameter_type == int:
                params_dict[parameter_name] = int(argument_value)
            elif parameter_type == float:
                params_dict[parameter_name] = float(argument_value)
            elif parameter_type == bool:
                params_dict[parameter_name] = parse_boolean(argument_value)
            else:
                # 其余都按str处理
                params_dict[parameter_name] = argument_value
    return params_dict


def mustache_render(template, **kwargs):
    """
    模板参数渲染
    :param template: 模板
    :param kwargs:参数
    :return:
    """
    from jinja2 import Template
    # 创建模板对象
    template = Template(template)
    # 渲染模板
    return template.render(**kwargs)
