import requests
import json
from argparse import ArgumentParser
from termcolor import colored

class DomainSearcher():
    def __init__(self, args:dict) -> None:
        self.__dict__.update(args)

    def _handleData(self, data):
        entities = "\n".join(list(set([x['common_name'] for x in data])))
        if self.output != None:
            if not self._writeToFile(entities):
                print("Could not write to an output file.")
        if self.verbose:
            print(f"Found {len(entities.splitlines())} domains.")
            print(entities)
        print(colored("Done!", "green"))

    def _writeToFile(self, data:str)->bool:
        try:
            with open(self.output, "w") as f:
                f.write(data+"\n")
                f.close()
        except:
            return False
        return True

    def __call__(self):
        """
        The main of Domain Searcher.
        """
        response = requests.get(f'https://crt.sh/?q={self.target}&output=json')
        if response.ok:
            return self._handleData(json.loads(response.text))
        else:
            raise ValueError("not a valid organization name.")

def getArgs():
    parser = ArgumentParser("cdf", description="find all the domains registered under a company")
    parser.add_argument("target", type=str, help="Specify the target organazition")
    parser.add_argument("-v", "--verbose", default=False, action="store_true", help="Specify if you need verbose output")
    parser.add_argument("-o", "--output", default=None, help="Specify output file name if one is needed")
    return parser.parse_args().__dict__

def bunner(args:dict):
    print('-'*50)
    print("target >> "+colored(args['target'], "cyan"))
    print("verbose >> "+colored(args['verbose'], "cyan"))
    print("output >> "+colored(args['output'], "cyan"))
    if args["verbose"] == False and args["output"] == None:
        print('*'*40)
        print(colored("the program won't output anything.".upper(), "red"))
        print('*'*40)
    print('-'*50)

def main()->int:
    args = getArgs()
    try:
        bunner(args)
        ds = DomainSearcher(args)
        ds()
        return 0
    except:
        return 1

if __name__ == '__main__':
    exit(main())
