# coding:utf-8

from threadpool import ThreadPool, makeRequests
from functools import wraps
import threading
import time

def asynch(wait=True):
    def package(fun):
        @wraps(fun)
        def realf(*args, **kws):
            process = {True:__asynch_wait, False:__asynch_no_wait}
            process[wait](fun, *args, **kws)
            return handler

        def __unbox(arg):
            fun = arg[0]
            arg_list = arg[1]
            kw_list = arg[2]
            res = fun(*arg_list, **kw_list)
            handler.finish(res)

        def __asynch_no_wait(fun, *args, **kws):
            argbag = ([fun, args, kws],)
            workers = ThreadPool(1)
            reqs = makeRequests(__unbox, argbag)
            [workers.putRequest(req) for req in reqs]
            #workers.wait()加上这句就会等待所有子线程结束

        def __asynch_wait(fun, *args, **kws):
            name = "worker_"+str(int(time.time()))
            argbag = ([fun, args, kws],)
            worker = threading.Thread(target=__unbox, name=name, args=argbag)
            worker.start()

        class Handler(object):

            def __init__(self):
                self.__ENUM = "#$%^&*#$%^&*#$%^&*_%&$&%$@#$%^&*"
                self.asynch_res = self.__ENUM

            def get_result(self):
                while self.asynch_res is self.__ENUM:
                    pass
                return self.asynch_res

            def is_finish(self):
                if self.asynch_res is self.__ENUM:
                    return False
                return True

            def finish(self, res):
                self.asynch_res = res
                
        handler = Handler()
        return realf
    
    if callable(wait):
        fun = wait
        wait = True
        return package(fun)

    if not isinstance(wait, bool):
        raise("parameter must be bool")

    return package

