"""The queue of planned calls, kept in Redis.

Each planned call is a job "<order_id>:<attempt_no>" in a sorted set, scored by the time
it is due. A job can be planned only once, so repeats can't create a second call.
"""
from datetime import datetime, timedelta, timezone

import redis

from app.config import settings

IST = timezone(timedelta(hours=5, minutes=30))


class CallQueue:
    def __init__(self, client: redis.Redis, prefix: str = "haanji"):
        self.r = client
        self.prefix = prefix
        self.due_key = f"{prefix}:calls:due"

    def _order_key(self, order_id: str) -> str:
        return f"{self.prefix}:calls:order:{order_id}"

    def plan(self, order_id: str, attempt_no: int, at: datetime) -> bool:
        """Plan a call. False if this order + attempt was already planned."""
        job = f"{order_id}:{attempt_no}"
        pipe = self.r.pipeline()
        pipe.zadd(self.due_key, {job: at.timestamp()}, nx=True)
        pipe.sadd(self._order_key(order_id), job)
        added, _ = pipe.execute()
        return bool(added)

    def planned(self, order_id: str) -> list[tuple[int, datetime]]:
        """(attempt_no, due time in IST) for every call still planned for an order."""
        out = []
        for job in self.r.smembers(self._order_key(order_id)):
            score = self.r.zscore(self.due_key, job)
            if score is not None:
                out.append((int(job.rsplit(":", 1)[1]), datetime.fromtimestamp(score, IST)))
        return sorted(out)

    def cancel(self, order_id: str) -> int:
        """Drop every planned call for an order. Returns how many were dropped."""
        jobs = list(self.r.smembers(self._order_key(order_id)))
        removed = self.r.zrem(self.due_key, *jobs) if jobs else 0
        self.r.delete(self._order_key(order_id))
        return removed

    def claim_due(self, now: datetime, limit: int = 100) -> list[tuple[str, int, datetime]]:
        """Take calls that are due. Each job is handed out once, even with several workers."""
        claimed = []
        for job, score in self.r.zrangebyscore(self.due_key, "-inf", now.timestamp(), start=0, num=limit, withscores=True):
            if self.r.zrem(self.due_key, job):
                order_id, attempt = job.rsplit(":", 1)
                self.r.srem(self._order_key(order_id), job)
                claimed.append((order_id, int(attempt), datetime.fromtimestamp(score, IST)))
        return claimed

    def size(self) -> int:
        return self.r.zcard(self.due_key)


def get_queue() -> CallQueue:
    return CallQueue(redis.Redis.from_url(settings.redis_url, decode_responses=True))
