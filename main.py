from leeroy.leeroy import leeroy
from leeroy.args import args


if __name__ == '__main__':
    config, values = args()
    leeroy(config, values)
