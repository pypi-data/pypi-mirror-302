from subprocess import call

from maker.fuzzy_maker import FuzzyMaker


def main():
    maker = FuzzyMaker()
    cmd = maker.run()
    if cmd:
        print(cmd)
        call(cmd.split())


if __name__ == "__main__": main()
