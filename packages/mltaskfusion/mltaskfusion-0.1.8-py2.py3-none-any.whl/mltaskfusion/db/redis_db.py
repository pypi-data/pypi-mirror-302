import json
import time
import redis
from typing import Any, Union
from mltaskfusion.utils import config, helper
from .base import _ScikitCompact, Job, QueueJobModel


class PyRedis(redis.Redis):
    """redis client"""

    def __init__(self):
        host = config.config("REDIS_HOST", "127.0.0.1")
        pwd = config.config("REDIS_PASSWORD", None)
        port = config.config("REDIS_PORT", 6379)

        redis.Redis.__init__(self, host=host, port=int(port), password=pwd)


class RedisQueue(PyRedis, _ScikitCompact):
    """队列"""

    def __init__(self, queue_name="ml-default", retry_after=0):
        """

        Attributes
        ------------
        queue_name
            str

        retry_after
            int 多少秒后重新进入队列,为0时不进入重试队列.
        """
        super(RedisQueue, self).__init__()
        self.queue_name = queue_name
        self.tries = 3
        self.retry_after = retry_after

    def call_lua_script(self, lua_script: str, keys: Union[list, None] = None, args: Union[list, None] = None) -> Any:
        """调用lua脚本

        Parameters
        ----------
        lua_script : str
            脚本
        keys : list, optional
            keys参数集合, by default None
        args : list, optional
            args参数集合, by default None

        Returns
        -------
        Any
        """

        script = self.register_script(lua_script)
        return script(keys=keys if keys else [], args=args if args else [])

    def size(self):
        """获取队列任务数量"""
        lua_script = """
            return redis.call('llen', KEYS[1]) + redis.call('zcard', KEYS[2]) + redis.call('zcard', KEYS[3])
        """
        return self.call_lua_script(
            lua_script=lua_script, keys=[self.queue_name, self.queue_name + ":delayed", self.queue_name + ":reserved"]
        )

    def push(self, job: QueueJobModel) -> int:
        """添加任务

        Parameters
        ------------
        job
            dict

        Returns
        ------------
        int
        """

        job = job.data
        if int(job.get("max_tries", self.tries)) <= int(job.get("attempts", 0)):
            return 0

        lua_script = """
            -- Push the job onto the queue...
            redis.call('rpush', KEYS[1], ARGV[1])
            -- Push a notification onto the "notify" queue...
            redis.call('rpush', KEYS[2], 1)
            return 1
        """

        return self.call_lua_script(
            lua_script=lua_script, keys=[self.queue_name, self.queue_name + ":notify"], args=[self._payload(job)]
        )

    def pop(self, islast: bool = False) -> Job:
        """获取队列任务

        Parameters
        -----------
        islast : bool
            是否删除并返回存储在 中的 key 列表的最后一个元素

        Returns
        -----------
        Job|None
        """

        lua_script = """
            -- Pop the first job off of the queue...
            local job = redis.call('%s', KEYS[1])
            local reserved = false

            if(job ~= false) then
                -- Increment the attempt count and place job on the reserved queue...
                reserved = cjson.decode(job)
                if (reserved['max_tries'] > reserved['attempts']) then
                    reserved['attempts'] = reserved['attempts'] + 1
                    reserved = cjson.encode(reserved)
                    redis.call('zadd', KEYS[2], ARGV[1], reserved)
                end
                redis.call('%s', KEYS[3])
            end

            return {job, reserved}
        """
        command = "rpop" if islast else "lpop"
        lua_script = lua_script % (command, command)
        self.migrate()
        result = self.call_lua_script(
            lua_script=lua_script,
            keys=[self.queue_name, self.queue_name + ":reserved", self.queue_name + ":notify"],
            args=[self._availableat(self.retry_after)],
        )

        if result[0] is not None:
            return Job(worker=self, job=result[0], reserved=result[1])

        return None

    def migrate(self):
        """迁移重试任务"""
        self._migrate_expired_jobs(self.queue_name + ":delayed", self.queue_name)

        if self.retry_after > 0:
            self._migrate_expired_jobs(self.queue_name + ":reserved", self.queue_name)

    def _migrate_expired_jobs(self, from_key: str, to_key: str):
        """迁移等待重试任务

        Parameters
        -------------
        from_key
            str

        to_key
            str

        Returns
        -------------
        mixed
        """

        lua_script = """
            -- Get all of the jobs with an expired "score"...
            local val = redis.call('zrangebyscore', KEYS[1], '-inf', ARGV[1])

            -- If we have values in the array, we will remove them from the first queue
            -- and add them onto the destination queue in chunks of 100, which moves
            -- all of the appropriate jobs onto the destination queue very safely.
            if(next(val) ~= nil) then
                redis.call('zremrangebyrank', KEYS[1], 0, #val - 1)

                for i = 1, #val, 100 do
                    redis.call('rpush', KEYS[2], unpack(val, i, math.min(i+99, #val)))
                    -- Push a notification for every job that was migrated...
                    for j = i, math.min(i+99, #val) do
                        redis.call('rpush', KEYS[3], 1)
                    end
                end
            end

            return val
        """

        result = self.call_lua_script(
            lua_script=lua_script, keys=[from_key, to_key, to_key + ":notify"], args=[self._availableat()]
        )
        return result

    def delete_reserved(self, job):
        """释放重试任务

        Parameters
        ----------------
        job
            Job

        Returns
        ----------------
        int
        """

        return self.zrem(self.queue_name + ":reserved", job.get_reserved_job())

    def delete_all_reserved(self):
        """释放所有重试任务

        Returns
        ----------------
        int
        """

        return self.delete(self.queue_name + ":reserved")

    def delete_and_release(self, job, delay=0):
        lua_script = """
            -- Remove the job from the current queue...
            redis.call('zrem', KEYS[2], ARGV[1])

            -- Add the job onto the "delayed" queue...
            redis.call('zadd', KEYS[1], ARGV[2], ARGV[1])

            return true
        """

        return self.call_lua_script(
            lua_script=lua_script,
            keys=[self.queue_name + ":delayed", self.queue_name + ":reserved"],
            args=[job.get_reserved_job(), self._availableat(delay)],
        )

    def _payload(self, job: dict):
        """组装job

        Parameters
        -------------
        job
            dict

        Returns
        -------------
        str
        """

        if job.get("id", None) is None:
            job["id"] = helper.unique_id()

        job["max_tries"] = self.tries
        job["attempts"] = job.get("attempts", 0)

        return json.dumps(job)

    def _availableat(self, delay: int = 0):
        return int(time.time()) + delay

    def get_cache_key(self, task_id: str) -> str:
        """获取任务存储key

        Parameters
        ----------
        task_id : str
            任务ID

        Returns
        -------
        str
        """
        return self.queue_name + ":" + task_id

    def push_and_response(self, job: QueueJobModel, seconds: int = 30) -> Any:
        """推送队列并获取查询结果

        Parameters
        ----------
        task_id : MlNode
            任务ID
        seconds : int, optional
            等待时间, by default 30
        """
        self.push(job=job)
        expired_time = int(time.time()) + seconds
        lua_script = """
            -- get result...
            local result = redis.call('get', KEYS[1])

            if(result ~= nil) then
                redis.call('del', KEYS[1])
            end

            return result
        """
        result = None

        while expired_time > time.time():
            response = self.call_lua_script(lua_script=lua_script, keys=[self.get_cache_key(job.id)])

            if response is not None:
                result = json.loads(response)
                break

            time.sleep(0.1)
            continue

        return result

    def update_result(self, task_id: str, data: dict, expired_seconds: int = 1800) -> bool:
        """更新任务结果

        Parameters
        ----------
        task_id : str
            任务标识
        data : dict
            结果
        expired_seconds : int
            过期时间

        Returns
        -------
        bool
        """

        return self.setex(self.get_cache_key(task_id=task_id), time=expired_seconds, value=json.dumps(data))
