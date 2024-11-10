from achareh_project.settings import redis_client

class RateLimiter:
    def __init__(self, ip_address: str, action_type: str):
        self.ip_address = ip_address
        self.action_type = action_type
        self.prefix = f"rate_limit:{self.action_type}:{self.ip_address}"

    def _get_request_count(self) -> int:
        return int(redis_client.get(self.prefix) or 0)

    def _increment_request_count(self) -> None:
        redis_client.incr(self.prefix)
        redis_client.expire(self.prefix, 60 * 60)

    def is_blocked(self) -> bool:
        return self._get_request_count() >= 3

    def reset_count(self) -> None:
        redis_client.delete(self.prefix)

    def handle_failed_attempt(self) -> None:
        self._increment_request_count()

    def block_for_1_hour(self) -> bool:
        if self.is_blocked():
            return True
        return False
