from wordle import Wordle
import argparse
argparser = argparse.ArgumentParser()
argparser.add_argument('--lang', type=str, default='english', help='language')

def main(lang):
    w = Wordle(lang)
    w.play()

if __name__ == '__main__':
    args = argparser.parse_args()
    main(args.lang)
