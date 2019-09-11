# -*- coding: utf-8 -*-
# @Author  : ydf
# @Time    : 2019/8/8 0008 13:32
import json
import time

from function_scheduling_distributed_framework.consumers.base_consumer import AbstractConsumer
from function_scheduling_distributed_framework.consumers.confirm_mixin import ConsumerConfirmMixinWithTheHelpOfRedis
from function_scheduling_distributed_framework.utils import RedisMixin


class RedisConsumerAckAble(ConsumerConfirmMixinWithTheHelpOfRedis, AbstractConsumer, ):
    """
    redis作为中间件实现的。将取出来的消息同时放入一个set中，代表unack消费状态。以支持对机器和python进程的随意关闭和断电。
    """
    BROKER_KIND = 9

    def _shedual_task(self):
        while True:
            t_start = time.time()
            result = self.redis_db_frame.blpop(self._queue_name, timeout=60)
            # task_bytes = self.redis_db_frame.lpop(self._queue_name)
            if result:
                task_str = result[1].decode()
                self._add_task_str_to_unack_zset(task_str, )
                self.logger.debug(f'取出的任务时间是 {round(time.time() - t_start, 4)}    消息是：  {task_str}  ')
                task_dict = json.loads(task_str)
                kw = {'body': task_dict, 'task_str': task_str}
                self._submit_task(kw)

    def _requeue(self, kw):
        self.redis_db_frame.rpush(self._queue_name, json.dumps(kw['body']))
