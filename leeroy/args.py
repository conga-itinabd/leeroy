import argparse


def args():
    pars_args = argparse.ArgumentParser(
        description='job manager leeroy for Jenkins'
    )
    pars_args.add_argument('config_file', help='steps config path')
    pars_args.add_argument('-v', '--values', help='values path')
    args = pars_args.parse_args()

    config = args.config_file
    values = args.values

    return config, values
