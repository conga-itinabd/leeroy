import json
import requests

from datetime import datetime


class Logger:
    def __init__(self, stepsbook):
        self.cfg = stepsbook

        if self.cfg.skiptls:
            requests.packages.urllib3.disable_warnings()
        current_datetime = datetime.now()
        date_formatted = current_datetime.strftime("%d/%m/%Y")
        time_formatted = current_datetime.strftime("%H:%M")
        if self.cfg.output != 'json':
            print('\n --- Jenkins job manager "leeroy" started! --- ')
            print(f'data: {date_formatted}, time: {time_formatted}')
            print('steps of stepsbook:')
            for step_name, _ in stepsbook.steps.items():
                print(f' - "{step_name}"')

    def log(self, message):
        if self.cfg.output != 'json':
            print(message)

    def file(self, message):
        if self.cfg.log_file:
            with open(self.cfg.log_file, "a") as file:
                file.write(message)

    def log_print_and_file(self, message):
        self.log(message)
        self.file(message)

    def debug(self, message, tag=''):
        if self.cfg.debug:
            print('\n\n[DEBUG]' + str(tag) + ': ' + str(message))

    def json_mode(self, all_statuses):
        if self.cfg.output == 'json':
            all_statuses_json = json.dumps(all_statuses, indent=4)
            print(all_statuses_json)
