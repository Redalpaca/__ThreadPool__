from BiliClass import BiliVideo
from threadpool import ThreadPool, Task
from commandHandler import CommandProcesser

def videoProcesser(bvid, *args, **kwargs):
    video = BiliVideo(bvid)
    video.MergeOutput(pbar= False, *args, **kwargs)
    pass

def command_addVideoTask(bvid):
    task = Task(videoProcesser, bvid, \
                Quality = '360p', path = 'E:/CodeField_1/Code_Python_E/Project/Crawler/ThreadPool/thread_pool/save/')
    global pool
    if pool.addTask(task) == True:
        print(f'\nAdd video {bvid} into Tasks.')
    pass

def craw_biliVideo(bvidList):
    global pool
    pool = ThreadPool(maxThreadNum= 3)
    pool.run(daemon = True)
    
    commands = {
        'stop'  : pool.terminate,
        'q'     : exit,
        'add'   : command_addVideoTask,
    }
    processer = CommandProcesser(pr = print, **commands)
    processer.run()
    
    for bvid in bvidList:
        task = Task(videoProcesser, bvid, Quality = '360p', path = 'E:/CodeField_1/Code_Python_E/Project/Crawler/ThreadPool/thread_pool/save/')
        # print('Add a task.')
        pool.addTask(task)
    pass

def main():
    bvidList = ['BV1ce4y1q778', 'BV1Ns4y1672c', 'BV1n14y1o7Rc', 'BV1kN411S7PJ',\
                'BV1Tg4y1P7bd', 'BV1fX4y1v78g']
    craw_biliVideo([])
    pass

if __name__ == '__main__':
    main()
    pass