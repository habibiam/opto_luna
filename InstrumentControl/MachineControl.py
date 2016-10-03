# MachineContol.py
#Date Created 2 Oct 2016.

from multiprocessing import Process, Pipe
from Gui import luna, cur_temp
from HardWareManager import dp
#This starts the GUI process
def startGui(pipe):
    luna.setReaderPipe(pipe)
    luna.mainloop()

#This invokes the publisher
def startHardwareManager(pipe):
    dp.Publish(pipe)

if __name__ == '__main__':
    # Creat Pipe
    writer, reader = Pipe()
    hw = Process(target=startHardwareManager, args=(writer,))
    gui = Process(target=startGui, args=(reader,))
    # Process Management
    gui.start()
    hw.start()

    gui.join()
    hw.join()

    writer.close()
    reader.close()

