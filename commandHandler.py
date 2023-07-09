import threading
import msvcrt

class CommandProcesser(object):
    def __init__(self, *args, **kwargs):
        """
        kwargs will be considered as a mapping of command - function. 
        eg.
            Initialize:
                cper = CommandProcesser( stop = exit, pr = print )
                ↓ 
                cper.pr = print
                cper.stop = exit
            Stdin Input:
                pr 1, 2, 3
                stop
            Call as:
                print('1','2','3')
                exit()
        """
        self.processThread = threading.Thread(target = self.getLine)
        self.args = args
        # Dynamically create instance member variable
        names = self.__dict__
        for key, value in kwargs.items():
            names[key] = value
    
    def run(self):
        self.processThread.start()
      
    # No blocked input.  
    def getLine(self):
        buf = []
        while True:
            if msvcrt.kbhit():
                key_byte = msvcrt.getch()
                key = key_byte.decode('ascii')
                # ESC
                if ord(key) == 27:
                    break
                # backspace
                if key == '\b':
                    buf.pop()
                else:
                    buf.append(key)
                print(key, end='' if key != '\b' else ' \b')
                # Enter
                if key == '\r':
                    command = ''.join(buf)
                    self.handler(command[:-1])
                    buf = []
                    continue

    def handler(self, command: str):
        commandList = command.split(' ')
        command = commandList[0]
        args = ()
        if len(commandList) > 1:
            args = commandList[1:]
        try:
            self.__dict__[command](*args)
        except Exception as e:
            print(f'Invalid command or args input:', command, end=' | ')
            print(e)
        return