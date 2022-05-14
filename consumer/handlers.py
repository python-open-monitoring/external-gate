from consumer import helpers
from consumer import methods
from consumer import schema


@helpers.validate_request_schema(schema.MonitorStat)
async def monitor_stat(validated_data):
    await methods.monitor_stat(validated_data)
