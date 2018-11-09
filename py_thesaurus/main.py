from py_thesaurus.base_class import WordAnalyzer
import argparse

parser = argparse.ArgumentParser(
    description='Analyze word using thesaurus.com/dictionary.com')
parser.add_argument('word', help="Word to get definition/synonym for")
parser.add_argument('-d', dest="method", action='store_const',
                    const='d', help="Option for definition")
parser.add_argument('-s', dest="method", action='store_const',
                    const='s', help="Option for synonym")
parser.add_argument('-a', dest="method", action='store_const',
                    const='a', help="Option for all")
args = parser.parse_args()
# print(args.word)
# print(args.method)


def main():
    new_instance = WordAnalyzer(args.word)
    if args.method == 'a':
        print("Synonyms")
        print(new_instance.get_synonym())
        print("Definitions")
        print(new_instance.get_definition())
    elif args.method == 's':
        print("Synonyms")
        print(new_instance.get_synonym())
    else:
        print("Definitions")
        print(new_instance.get_definition())

