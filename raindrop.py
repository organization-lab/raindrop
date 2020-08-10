import rumps
import time
import os


rumps.debug_mode(True)


SEC_TO_MIN = 60


# global parameters for MVP version
current_user_input = ''  # temp version


log = 'test.log'
writer = open(log, 'a')


def timez():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


writer.write('open at {}\n'.format(timez()))
writer.close()


class TimerApp(object):
    def __init__(self, timer_interval=1):
        self.timer = rumps.Timer(self.on_tick, 1)
        self.timer.stop()  # timer running when initialized
        self.timer.count = 0
        self.app = rumps.App("Raindrop", "💧")
        self.start_pause_button = rumps.MenuItem(title='Start Timer',
                                                 callback=lambda _: self.start_timer(_, self.interval))
        self.stop_button = rumps.MenuItem(title='Stop Timer',
                                          callback=None)
        self.buttons = {}
        self.buttons_callback = {}
        for i in [5, 10, 15, 20, 25, 1]:
            title = str(i) + ' Minutes'
            callback = lambda _, j=i: self.set_mins(_, j)
            self.buttons["btn_" + str(i)] = rumps.MenuItem(title=title, callback=callback)
            self.buttons_callback[title] = callback
        self.interval = 5 * SEC_TO_MIN  # current 5 min by default
        self.buttons['btn_5'].state = True
        self.app.menu = [
            self.start_pause_button,
            None,
            # self.button_things,
            # None,
            *self.buttons.values(),
            None,
            self.stop_button]

    def run(self):
        self.app.run()

    def set_things_mins(self, sender):
        # pass_interval = get_things_min()
        print("pass_interval is now", pass_interval)
        # self.button_things.title = "Default (" + str(round(pass_interval)) + "min)"
        # self.set_mins(sender, pass_interval)

    def set_mins(self, sender, interval):
        for btn in [*self.buttons.values()]:
            if sender.title == btn.title:
                self.interval = interval*SEC_TO_MIN
                btn.state = True
            elif sender.title != btn.title:
                btn.state = False

    def start_timer(self, sender, interval):
        for btn in [*self.buttons.values()]:
            btn.set_callback(None)

        # add a window for user input
        t = rumps.Window(message='What will this raindrop for?',
                         title='Raindrop',
                         default_text='Unspecific',
                         dimensions=(160,40))
        global current_user_input  # a temp solution to work
        current_user_input = t.run().text
        print('{}, {}, {}'.format(timez(), current_user_input, interval))
        global log  # TODO(mofhu): make this more elegant
        writer = open(log, 'a')
        writer.write('{}, {}, {}\n'.format(timez(), current_user_input, interval))
        writer.close()


        if sender.title.lower().startswith(("start", "continue")):
            if sender.title == 'Start Timer':
                # reset timer & set stop time
                self.timer.count = 0
                self.timer.end = interval
            # change title of MenuItem from 'Start timer' to 'Pause timer'
            sender.title = 'Pause Timer'
            # lift off! start the timer
            self.timer.start()
        else:  # 'Pause Timer'
            sender.title = 'Continue Timer'
            self.timer.stop()

    def on_tick(self, sender):
        time_left = sender.end - sender.count
        mins = time_left // 60 if time_left >= 0 else time_left // 60 + 1
        secs = time_left % 60 if time_left >= 0 else (-1 * time_left) % 60
        if mins == 0 and time_left < 0:  # TODO(mofhu): check the `pause` issue when click the menubar
            # global current_user_input  # a temp solution to work
            response = rumps.Window(
                message='This raindrop is for {}\nHow many % time you concentrated on your main objective? How do you feel now? How do you feel about this raindrop? (1-5 stars)'.format(current_user_input),
                title='Congratulation! You finished a raindrop today!',
                default_text='80',
                ok = '⭐️⭐️⭐️⭐️⭐️'
            )
            response.add_buttons(['⭐️⭐️⭐️⭐️', '⭐️⭐️⭐️', '⭐️⭐️', '⭐️'])
            feedback = response.run()
            global log  # TODO(mofhu): make this more elegant
            print('{}, {}'.format(6-feedback.clicked, feedback.text))  # 5 stars == button 1 ... 1 star == button 5
            writer = open(log, 'a')
            writer.write('{}, {}\n'.format(6-feedback.clicked, feedback.text))  # 5 stars == button 1 ... 1 star == button 5
            writer.close()
            """
            rumps.notification(title='Raindrop',
                               subtitle='Time is up for this raindrop - {}! Take a break :)'.format(current_user_input),
                               message='')
            """
            self.stop_timer(sender)
            self.stop_button.set_callback(None)
        else:
            self.stop_button.set_callback(self.stop_timer)
            self.app.title = '{:2d}:{:02d}'.format(mins, secs)
        sender.count += 1

    def stop_timer(self, sender=None):
        self.timer.stop()
        self.timer.count = 0
        self.app.title = "💧"
        self.stop_button.set_callback(None)

        for key, btn in self.buttons.items():
            btn.set_callback(self.buttons_callback[btn.title])

        self.start_pause_button.title = 'Start Timer'


if __name__ == '__main__':
    # write project log to text file (temp)
    # from sys import argv
    # script, log_file = argv
    # log = open(log_file, 'a')

    app = TimerApp(timer_interval=1)
    app.run()
