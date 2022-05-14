from pydantic import BaseModel


class MonitorStat(BaseModel):
    monitor_id: int
    user_id: int
    monitor_name: str
    monitor_host: str
    monitor_port: int
    monitor_connection_establish: int
    monitor_request_time: str
    monitor_response_time: int
