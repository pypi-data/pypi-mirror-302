# -*- coding: utf-8 -*-
"""
:Author: HuangJianYi
:Date: 2024-01-18 18:19:58
@LastEditTime: 2024-10-16 11:51:53
@LastEditors: HuangJianYi
:Description: 框架DB操作类
"""
from seven_framework.base_model import *
from seven_framework import *
from seven_cloudapp_frame.libs.common import *
from seven_cloudapp_frame.libs.customize.seven_helper import *

class FrameDbModel(BaseModel):

    def __init__(self, model_class, sub_table):
        """
        :Description: 框架DB操作类
        :param model_class: 实体对象类
        :param sub_table: 分表标识
        :last_editors: HuangJianYi
        """
        super(FrameDbModel,self).__init__(model_class, sub_table)

    def add_list_batch(self, data_list, batch_num=100):
        """
        :description: 分批添加数据
        :param data_list：数据列表
        :param batch_num：分批数量
        :return 成功添加的数量
        :last_editors: HuangJianYi
        """
        page_index = 0
        total = 0
        while True:
            add_list = data_list[page_index * batch_num:(page_index + 1) * batch_num]
            if not add_list:
                return total
            result = self.add_list(add_list)
            if result == True:
                total += len(add_list)
            page_index += 1

    def set_sub_table(self, object_id=''):
        """
        :description: 设置分表
        :param object_id:object_id
        :return:
        :last_editors: HuangJianYi
        """
        table_name = str(self.model_obj).lower()
        sub_table_config = share_config.get_value("sub_table_config",{})
        table_config = sub_table_config.get(table_name, None)
        if table_config and object_id:
            sub_table = SevenHelper.get_sub_table(object_id, table_config.get("sub_count", 10))
            if sub_table:
                # 数据库表名
                self.table_name = table_name.replace("_tb", f"_{sub_table}_tb")
        return self
    
    def set_view(self, view_name=''):
        """
        :description: 设置视图
        :param view_name:视图名
        :return:
        :last_editors: HuangJianYi
        """
        table_name = str(self.model_obj).lower()
        if not view_name:
            self.table_name = table_name.replace("_tb", "_view")
        else:
            self.table_name = view_name
        return self
    
    def relation_and_merge_dict_list(self, primary_dict_list, relation_db_model, relation_key_field, field="*", primary_key_field="id", is_cache=True, dependency_key="", cache_expire=1800):
        """
        :description: 根据给定的主键表关联ID数组从关联表获取字典列表合并。
        :param primary_dict_list: 主表字典列表
        :param relation_db_model: 关联表关联model
        :param relation_key_field:  关联表关联字段
        :param field: 关联表查询字段
        :param primary_key_field: 主表关联字段
        :param is_cache: 是否开启缓存（1-是 0-否）
        :param dependency_key: 缓存依赖键
        :param cache_expire: 缓存过期时间（秒）
        :return:
        :last_editors: HuangJianYi
        """
        if len(primary_dict_list) <= 0:
            return primary_dict_list
        # 检查relation_key_field是否已经在field中
        if field != "*" and relation_key_field not in field.split(","):
            field = f"{relation_key_field},{field}"
        ext_table_ids = [i[primary_key_field] for i in primary_dict_list]
        where = SevenHelper.get_condition_by_int_list(relation_key_field, ext_table_ids)
        if is_cache == True:
            relation_dict_list = relation_db_model.get_cache_dict_list(where, field=field, dependency_key=dependency_key, cache_expire=cache_expire)
        else:
            relation_dict_list = relation_db_model.get_dict_list(where, field=field)
        dict_list = SevenHelper.merge_dict_list(primary_dict_list, primary_key_field, relation_dict_list, relation_key_field, exclude_merge_columns_names="id")
        return dict_list
    
    def relation_and_merge_dict(self, primary_dict, relation_db_model, field="*", primary_key_field="id", is_cache=True, dependency_key="", cache_expire=1800):
        """
        :description: 根据给定的主键表字典合并关联表字典。
        :param primary_dict: 主表字典
        :param relation_db_model: 关联表关联model
        :param field: 关联表查询字段
        :param primary_key_field: 主表关联字段
        :param is_cache: 是否开启缓存（1-是 0-否）
        :param dependency_key: 缓存依赖键
        :param cache_expire: 缓存过期时间（秒）
        :return:
        :last_editors: HuangJianYi
        """
        if not primary_dict:
            return primary_dict
        if is_cache == True:
            relation_dict = relation_db_model.get_cache_dict_by_id(primary_dict[primary_key_field], field=field, dependency_key=dependency_key, cache_expire=cache_expire)
        else:
            relation_dict = relation_db_model.get_dict_by_id(primary_dict[primary_key_field], field=field)
        if relation_dict and "id" in relation_dict:
            del relation_dict["id"]
        if relation_dict:
            primary_dict.update(relation_dict)
        return primary_dict
    
    
    def add_update_entity_list(self, models, update_sql, params_list=None):
        """
        :Description: 批量数据入库,遇到主键冲突则更新指定字段
        :param models: 模型实体列表
        :param update_sql: 如果主键冲突则执行的更新sql语句
        :param params_list: 参数化查询参数列表
        :return: 返回受影响的行数
        :last_editors: HuangJianYi
        """
        if not models:
            return 0

        field_list = self.model_obj.get_field_list()
        if len(field_list) == 0:
            return 0

        insert_field_str = ""
        insert_values_str = ""
        all_params = []

        for model in models:
            single_value_str = ""
            single_params = []
            for field_str in field_list:
                param_value = str(getattr(model, field_str))
                if str(field_str).lower() == self.primary_key_field.lower() and param_value == "0":
                    continue
                if not insert_field_str:
                    insert_field_str += f"`{field_str}`,"
                single_value_str += "%s,"
                single_params.append(param_value)
            
            insert_values_str += f"({single_value_str.rstrip(',')}),"
            all_params.extend(single_params)

        if params_list:
            for params in params_list:
                all_params.extend(params)

        insert_field_str = insert_field_str.rstrip(',')
        insert_values_str = insert_values_str.rstrip(',')
        
        sql = f"INSERT INTO {self.table_name}({insert_field_str}) VALUES {insert_values_str} ON DUPLICATE KEY UPDATE {update_sql};"
        
        if not self.is_transaction():
            return self.db.insert(sql, tuple(all_params), False)

        transaction_item = {"sql": sql, "params": tuple(all_params)}
        self.db_transaction.transaction_list.append(transaction_item)
        return True
