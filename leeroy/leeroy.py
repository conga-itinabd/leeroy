from pathlib import Path

from .Logger import Logger

from .leeroy_stepsbook.actions import build, rebuild, get_data
from .leeroy_stepsbook.data_classes import make_config
from .leeroy_stepsbook.common_for_actions import Requester
from .leeroy_stepsbook.put_values_to_stepsbook import put_values
from .leeroy_init.leeroy_init import leeroy_init


def leeroy(main_arg, values):

    if main_arg == 'version':
        print('leeroy version: 0.0.1')

    elif main_arg.endswith('.yaml') or main_arg.endswith('.yml'):

        def if_home_path(file_path):
            if file_path.startswith("~"):
                return Path(file_path).expanduser()
            else:
                return Path(file_path)
        config = if_home_path(main_arg)
        values = if_home_path(values)

        pulled_values_steps = put_values(values, config)
        stepsbook = make_config(pulled_values_steps)

        logger = Logger(stepsbook)
        requester = Requester(stepsbook, logger)
        all_statuses = {}
        logger.debug(stepsbook.steps, 'stepsbook.steps')

        for step_name, step in stepsbook.steps.items():
            logger.debug(step_name, 'step_name')
            logger.debug(step, 'step')
            number_of_iteration = 0
            iterations = 1
            step = step[0]
            if step.iterations:
                iterations = int(step.iterations)
            while number_of_iteration != iterations:
                backup_step = step_name
                if iterations > 1:
                    step_name = step_name + '_' + str(number_of_iteration + 1)

                step_name = backup_step
                if step.action == 'build':
                    step_status = build(
                        step, all_statuses, requester, logger
                    )
                elif step.action == 'rebuild':
                    step_status = rebuild(
                        step, all_statuses, requester, logger
                    )
                elif step.action == 'get_data':
                    step_status = get_data(
                        step, all_statuses, requester, logger
                    )
                else:
                    logger.log(
                        'in step ' + step_name + ' no valid action'
                        'starting next step'
                    )
                status = {step_name: step_status}
                all_statuses.update(status)
                number_of_iteration += 1
                logger.debug(all_statuses)
        logger.json_mode(all_statuses)

    elif 'init' in main_arg and (
        not main_arg.endswith('.yaml') and not main_arg.endswith('.yml')
    ):
        leeroy_init(main_arg)

    else:
        print(
            'There is no valid main argument. If you are trying to start '
            'a stepsbook, make sure it ends with .yaml or .yml.'
        )
