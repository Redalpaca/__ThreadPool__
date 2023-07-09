import threading
import queue
from typing import Any
# list.append() / list.pop() is atomic.

crawlerLock = threading.Lock()

class SyncQuene(list):
    MAX_ELE_NUM = 20
    
    def __init_subclass__(self):
        self.quene = []
        return super().__init_subclass__()
    
    def __len__(self):
        return len(self.quene)
    
    def is_full(self):
        return True if self.__len__() >= SyncQuene.MAX_ELE_NUM else False
    
    def is_empty(self):
        return True if self.__len__() <= 0 else False
    
    def push(self, task):
        with crawlerLock:
            if self.is_full():
                return False
            self.quene.append(task)
        return True
    
    def pop(self):
        with crawlerLock:
            if self.is_empty():
                return 
            task = self.quene[0]
            self.quene.pop(0)
        return task
    pass

class ErrorHandler:
    def __init__(self):
        pass
    def __call__(self, *args: Any, **kwds: Any):
        pass
    pass

class Task:
    def __init__(self, func_task, *args, **kwargs):
        self.func_task = func_task
        self.args = args
        self.kwargs = kwargs
        self.error_handler = None
        self.isterminal = False
    def run(self):
        try:
            self.func_task(*self.args, **self.kwargs)
        except Exception as e:
            print(e)
            return e
        return None
    def handler(self, error):
        if not error:
            return False
        retry = False
        if self.error_handler:
            retry = self.error_handler(error, *self.args, **self.kwargs)
        return retry

class ThreadPool(object):
    def __init__(self, maxThreadNum):
        self.maxThreadNum = maxThreadNum
        
        self.TaskQueue = queue.Queue()
        self.ThreadList = []
        
        self.isterminal = False
        self.poolLock = threading.Lock()
        self.printLock = threading.Lock()
        pass
    
    def __create_thread(self, daemon):
        thread = threading.Thread(target= self.func_thread)
        # Whether to use Guardian Thread
        thread.daemon = daemon
        return thread
    def run(self, daemon = True):
        for i in range(self.maxThreadNum):
            cur = self.__create_thread(daemon)
            cur.name = f'thread_{i}'
            self.ThreadList.append(cur)
            cur.start()
        pass
    
    def addTask(self, *Tasks):
        if self.isterminal:
            print('addTask failed: The thread pool is shut down.')
            return False
        for task in Tasks:
            if not isinstance(task, Task):
                continue
            self.TaskQueue.put(task)
        return True
    
    def terminate(self, *args):
        """
        Only called at main thread, so it's lock free.
        """
        self.isterminal = True
        for i in range(self.maxThreadNum):
            task_end = Task(lambda x:x)
            task_end.isterminal = True
            self.TaskQueue.put(task_end)
    
    def func_thread(self):
        current_thread = threading.current_thread()
        while not self.isterminal:
            current_task = self.TaskQueue.get()
            current_task: Task
            if current_task.isterminal:
                break
            self.printLock.acquire()
            print(current_thread.name, 'get a task.')
            self.printLock.release()
            
            error = current_task.run()
            retry = current_task.handler(error)
            if retry:
                self.TaskQueue.put(current_task)
            
            self.printLock.acquire()
            print(current_thread.name, 'finish a task.')
            self.printLock.release()
        print('{name} is terminal.'.format(name = current_thread.name))
        
if __name__ == '__main__':
    pass