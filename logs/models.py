from infi.clickhouse_orm import Database, Model, StringField, DateTimeField
import os


class LogData(Model):
    id = StringField()
    level = StringField()
    message = StringField()
    extra_info = StringField()
    source = StringField()
    created_at = DateTimeField()
    
    class Meta:
        table_name = 'log_data'

    
db = Database('cnext_logs', host='clickhouse-staging', port=9000, username='cnextuser', password='cnextuser4321')
