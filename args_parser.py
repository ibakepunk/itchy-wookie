from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument('action', choices=['open', 'close', 'clear'])
parser.add_argument('--ports', nargs='+', type=int)
