# from sqlalchemy import BigInteger, Boolean, Column, DateTime, Integer, Text
# from sqlalchemy import create_engine
# from sqlalchemy.orm import declarative_base

# Base = declarative_base()

# _type_lookup = {
#     'bigint': BigInteger,
#     'boolean': Boolean,
#     'default': '',
#     'index': True,
#     'int': Integer,
#     'required': False,
#     'text': Text,
#     'timestamptz': DateTime(timezone=True),
#     'unique': True,
#     'values': Text
# }


# def convert_table_classname(name):
#     return ''.join(x.capitalize() or '_' for x in name.split('_'))


# def mapping_for_json(schema):
#     for table_key, table_values in schema.items():

#         for table_name, col_data in table_values.items():

#             json_cls_schema = {'tablename': table_name,
#                                'columns': [{'name': 'id', 'type': Integer, 'is_pk': True}]}

#             for col_name, constraints in col_data.items():
#                 new_col = {'name': col_name}

#                 if 'type' in constraints and constraints['type'] in _type_lookup:
#                     new_col.update(
#                         {'name': col_name, 'type': _type_lookup[constraints['type']]})

#                 if 'default' in constraints:
#                     _type_lookup.update({'default': constraints['default']})

#                 for x in constraints:
#                     if x is not 'type' and x in _type_lookup:
#                         new_col.update(
#                             {'name': col_name, 'type': _type_lookup[constraints['type']], x: _type_lookup[x]})

#                 json_cls_schema['columns'].append(new_col)

#             clsdict = {'clsname': convert_table_classname(
#                 table_name), '__tablename__': json_cls_schema['tablename']}

#             clsdict.update(
#                 {record['name']: Column(
#                     record['type'],
#                     primary_key=record.get('is_pk', False),
#                     nullable=record.get('required', False),
#                     unique=record.get('unique', False),
#                     default=record.get('default', False)
#                 )
#                     for record in json_cls_schema['columns']
#                 }
#             )

#             e = create_engine("sqlite://", echo=True)
#             type(clsdict['clsname'], (Base,), clsdict)
#             Base.metadata.create_all(e)

# from sqlalchemy import BigInteger, Boolean, Column, DateTime, Integer, Text
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

# _type_lookup = {
#     'bigint': BigInteger,
#     'boolean': Boolean,
#     'default': '',
#     'index': True,
#     'int': Integer,
#     'required': False,
#     'text': Text,
#     'timestamptz': DateTime(timezone=True),
#     'unique': True,
#     'values': Text
# }

# class TableMapper:
#     def __init__(self, schema):
#         self.schema = schema

#     def convert_table_classname(self, name):
#         return ''.join(x.capitalize() or '_' for x in name.split('_'))

#     def create_class(self, table_name, col_data):
#         cls_name = self.convert_table_classname(table_name)
#         cls_dict = {'__tablename__': table_name, 'id': Column(Integer, primary_key=True)}

#         for col_name, constraints in col_data.items():
#             column_args = {'name': col_name}

#             if 'type' in constraints and constraints['type'] in _type_lookup:
#                 column_args.update({'type': _type_lookup[constraints['type']]})

#             if 'default' in constraints:
#                 _type_lookup.update({'default': constraints['default']})

#             for x in constraints:
#                 if x != 'type' and x in _type_lookup:
#                     column_args.update({'name': col_name, 'type': _type_lookup[constraints['type']], x: _type_lookup[x]})

#             cls_dict[col_name] = Column(**column_args)

#         return type(cls_name, (Base,), cls_dict)

#     def map_tables(self):
#         for table_key, table_values in self.schema.items():
#             for table_name, col_data in table_values.items():
#                 new_class = self.create_class(table_name, col_data)
#                 e = create_engine("sqlite://", echo=True)
#                 Base.metadata.create_all(e)

# # Example usage:
# # schema = {
# #     'table_key': {
# #         'table_name': {
# #             'column1': {'type': 'int'},
# #             'column2': {'type': 'text', 'required': True},
# #             # ... other columns ...
# #         }
# #     }
# # }
# # mapper = TableMapper(schema)
# # mapper.map_tables()
