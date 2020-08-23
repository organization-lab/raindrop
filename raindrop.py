import rumps
import time


SEC_TO_MIN = 60


def timez():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


class TimerApp(object):
    def __init__(self, log, quote, debug_mode):
        self.timer = rumps.Timer(self.on_tick, 1)
        self.log = log
        self.quote = quote
        self.debug_mode = debug_mode
        with open(self.log, 'a') as log_writer:  # append mode
            log_writer.write('raindrop.open: {}\n'.format(timez()))
        if self.debug_mode:
            rumps.debug_mode(True)  # rumps debug info is useful for dev and usage
        self.timer.stop()  # timer running when initialized
        self.timer.count = 0
        self.app = rumps.App("Raindrop", "💧")
        self.start_pause_button = rumps.MenuItem(title='Start Timer',
                                                 callback=lambda _: self.start_timer(_, self.interval))
        self.stop_button = rumps.MenuItem(title='Stop Timer',
                                          callback=None)
        self.buttons = {}
        self.buttons_callback = {}
        self.timer_list = [5, 10, 15, 20, 25]  # TODO(mofhu): maybe extend it later as an optional user input
        if self.debug_mode:
            self.timer_list.append(1)  # only add 1 min in debug mode

        for i in self.timer_list:
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

    def get_quote(self):
        quote_list = open(self.quote).readlines()
        from random import choice
        return choice(quote_list)

    def run(self):
        self.app.run()

    def set_things_mins(self, sender):
        # pass_interval = get_things_min()
        print("raindrop.interval:", pass_interval)
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
        # sender.title could be "Start Timer"/"Continue Timer"/"Pause Timer"
        if sender.title == 'Start Timer':
            start_quote = self.get_quote()
            # add a window for user input
            t = rumps.Window(message='{}\nWhat will this raindrop for?'.format(start_quote),
                            title='Raindrop',
                            default_text='Unspecific',
                            dimensions=(160,40))
            self.current_user_input = t.run().text
            print('raindrop.start: {}, {}, {}'.format(timez(), self.current_user_input, interval))
            with open(self.log, 'a') as log_writer:  # append mode
                log_writer.write('raindrop.start: {}, {}, {}\n'.format(timez(), self.current_user_input, interval))
            # reset timer & set stop time
            self.timer.count = 0
            self.timer.end = interval
            # change title of MenuItem from 'Start timer' to 'Pause timer'
            sender.title = 'Pause Timer'
            # lift off! start the timer
            self.timer.start()
        elif sender.title == 'Continue Timer':
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
            end_quote = self.get_quote()
            response = rumps.Window(
                message='{}\nThis raindrop is for {}.\nHow many % time you concentrated on your main objective? How do you feel now? How do you feel about this raindrop? (1-5 stars)'.format(end_quote, self.current_user_input),
                title='Congratulation! You finished a raindrop today!',
                default_text='80',
                ok = '⭐️⭐️⭐️⭐️⭐️'
            )
            response.add_buttons(['⭐️⭐️⭐️⭐️', '⭐️⭐️⭐️', '⭐️⭐️', '⭐️'])
            feedback = response.run()
            print('raindrop.end.feedback: {}, {}'.format(6-feedback.clicked, feedback.text))  # 5 stars == button 1 ... 1 star == button 5
            with open(self.log, 'a') as log_writer:  # append mode
                log_writer.write('raindrop.end.feedback: {}, {}\n'.format(6-feedback.clicked, feedback.text))  # 5 stars == button 1 ... 1 star == button 5
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
        # TODO(mofhu): add a output log here, and also for quit app

        for key, btn in self.buttons.items():
            btn.set_callback(self.buttons_callback[btn.title])

        self.start_pause_button.title = 'Start Timer'



if __name__ == '__main__':
    # parse argument
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('log',
                        help='Path of log file')
    parser.add_argument('quote',
                        help='Path of quote file')
    parser.add_argument('-d', '--debug',
                        help='Flag of debug mode. Debug mode enables 1) `rumps` output 2) 1 min timer for test',
                        action='store_true')
    args = parser.parse_args()
    if args.debug:
        print(args.log, args.quote, args.debug)

    # init app
    app = TimerApp(log=args.log,
                   quote=args.quote,
                   debug_mode=args.debug)
    app.run()
