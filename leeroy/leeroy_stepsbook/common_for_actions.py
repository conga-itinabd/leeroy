import requests
import json
import time
import sys


def add_slash(url):
    url = url if url.endswith('/') else url + '/'
    return url


def def_step_status(step):
    step_status = {
        'build_url': '',
        'status': ''
    }
    if step.log:
        step_status.update({'log': {}})
    if step.catch:
        step_status.update({'catch': {}})
    return step_status


class Requester:
    def __init__(self, stepsbook, logger):
        self.auth = (stepsbook.user, stepsbook.token)
        self.headers = {"Accept": "application/json"}
        self.logger = logger

        self.verify = True
        if stepsbook.skiptls:
            self.verify = False

    def post(self, url, data):
        self.logger.debug(url, 'requester.post url')
        return requests.post(
            url=url, auth=self.auth, data=data,
            verify=self.verify, headers=self.headers
        )

    def get(self, url):
        return requests.get(
            url=url, auth=self.auth,
            verify=self.verify, headers=self.headers
        )


def get_item_info(item_url, requester, logger):
    responce = requester.get(item_url)
    if not responce.text:
        logger.log("can't get item info. check your job")
        sys.exit()

    return responce.text


def wait_build_number(item_info, item_link, requester, logger):
    logger.log(' - getting build number... - \n')
    logger.debug('item link: ' + item_link)
    data = json.loads(item_info)
    while True:
        if "executable" in data:
            if "url" in data["executable"]:
                build_url = data["executable"]["url"]
                logger.log(
                    '\n - got result!\n'
                    '   build url: ' + build_url
                )
                return build_url
        else:
            time.sleep(12)
            item_info = get_item_info(item_link, requester, logger)
            data = json.loads(item_info)
            time.sleep(2)
            logger.log(
                'trying get build number\n'
                'maybe it is in queue, waiting...'
            )


def wait_end(build_url, requester, logger):
    logger.log('\n - waiting end of build - \n')
    time.sleep(3)
    waited_seсs = 0
    url = add_slash(build_url) + 'api/json'
    responce = requester.get(url)
    build_data = responce.text
    build_data = json.loads(build_data)
    try:
        while build_data["building"]:
            time.sleep(5)
            responce = requester.get(url)
            build_data = responce.text
            build_data = json.loads(build_data)
            waited_seсs += 5
            if waited_seсs < 60:
                if waited_seсs % 10 == 0:
                    logger.log(f'waiting {waited_seсs} seconds...')
            elif waited_seсs < 300:
                if waited_seсs % 20 == 0:
                    quotient, remainder = divmod(waited_seсs, 60)
                    logger.log(
                        f'waiting {quotient} minutes, {remainder} seconds...'
                    )
            elif waited_seсs < 1200:
                if waited_seсs % 60 == 0:
                    logger.log(f'waiting {str(waited_seсs/60)} minutes...')
            elif waited_seсs < 3600:
                if waited_seсs % 300 == 0:
                    logger.log('-logging every 5 minutes...')
                    logger.log(f'waiting {str(waited_seсs/60)} minutes...')
            else:
                quotient, remainder = divmod(waited_seсs, 600)
                if quotient % 600 == 0:
                    logger.log('-logging every 10 minutes...')
                    logger.log(
                        f'waiting {quotient} hours, {remainder} minutes...'
                    )

        if build_data["result"] == "FAILED":
            print('build failed\nleeroy stopped')
            sys.exit()
        else:
            logger.log(' - build finnished with status:'
                '\n   ' + build_data["result"]
            )
        return build_data["result"]
    except Exception as e:
        print(
            'something went wrong\n'
            'check your creds or network\nerror:'
        )
        print(e)
        sys.exit()


def get_data(build_url, requester, logger):
    url = add_slash(build_url) + 'consoleText/api/json'
    try:
        responce = requester.get(url)
    except Exception as e:
        print('something went wrong with job')
        print(e)
        sys.exit()
    return responce.text
