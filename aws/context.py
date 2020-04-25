import uuid
from datetime import date
import os
import humanize


class Context:
    def __init__(self, function_name, function_version):
        self.function_name = function_name
        self.function_version = function_version
        self.invoked_function_arn = "arn:aws:lambda:eu-north-1:000000000000:function:{}".format(self.function_name)
        self.aws_request_id = uuid.uuid1()
        self.log_group_name = "/aws/lambda/{}".format(self.function_name)
        today = date.today()
        self.log_stream_name = "{}/[{}]4459c970fa6d4c77aca62c95850fce54".format(today.strftime("%Y/%m/%d"), self.function_version)
        self.memory_limit_in_mb = Context.memory(self)
        pass

    def memory(self):
        mem = int(os.popen("cat /sys/fs/cgroup/memory/memory.limit_in_bytes").read())
        self.memory_limit_in_mb = humanize.naturalsize(mem, gnu=True)
        return (self.memory_limit_in_mb)
        pass
