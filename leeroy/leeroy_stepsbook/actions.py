import json
import sys

from dataclasses import asdict

from .log_and_catch import get_step_logs, step_changer, get_step_catches
from .common_for_actions import (
    wait_end, get_data, wait_build_number,
    add_slash, get_item_info, def_step_status
)

from .data_classes import StepData


def build(step, all_statuses, requester, logger):
    step_status = def_step_status(step)
    step_data_dict = asdict(step)
    step_data_dict = step_changer(step_data_dict, all_statuses)
    step = StepData(**step_data_dict)
    logger.debug(step, 'step_changer')
    url = add_slash(step.url)
    url = url + 'buildWithParameters'
    responce = requester.post(url, data=step.parameters)

    def main_build(
        item_link, step, all_statuses, step_status, requester, logger
    ):
        item_info = get_item_info(item_link, requester, logger)
        build_url = wait_build_number(item_info, item_link, requester, logger)
        step_status['build_url'] = build_url
        if step.wait_end:
            build_status = wait_end(build_url, requester, logger)
            step_status['status'] = build_status
            build_console_output = get_data(build_url, requester, logger)
            if step.log:
                step_status['log'] = get_step_logs(
                    build_console_output, step.log
                )
            if step.catch:
                step_status['catch'] = get_step_catches(
                    build_console_output, step.catch
                )
        return step_status

    if responce.status_code == 201:
        logger.log(f'\n\n -- step "{step.step}" started -- \n')
        logger.debug(responce.status_code)
        item_link = responce.headers["location"]
        item_link = add_slash(item_link) + 'api/json'

        step_status = main_build(
            item_link, step, all_statuses, step_status, requester, logger
        )
        return step_status

    elif responce.status_code == 404:
        logger.log('build in queue')
        logger.debug(responce.status_code)
        prep_link1 = step.url[:step.url.find('/jenkins')]
        prep_link2 = json.loads(responce.text)['url'] + 'api/json'
        item_link = prep_link1 + prep_link2

        step_status = main_build(
            item_link, step, all_statuses, step_status, requester, logger
        )
        return step_status

    elif responce.status_code == 401:
        print('problems with authorization: ')
        print(responce.status_code)
        sys.exit()


def build_active_choice(step):
    step_status = def_step_status(step)
    return step_status


def rebuild(step, all_statuses, requester, logger):
    step_status = def_step_status(step)
    return step_status


def get_build_data(step):
    step_status = def_step_status(step)
    return step_status
