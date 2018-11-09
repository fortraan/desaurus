barLen = 50
full = "\u2589" * barLen
empty = " " * barLen
bar = 0
print("Initialising...\n[\033[38;2;0;255;0m" + empty + "\033[0m]", end = "")

from math import floor
from time import sleep


def print_bar(percentage, msg):
    global bar
    msg = msg + empty[len(msg):barLen]
    for i in range(bar, percentage + 1):
        print("\r[\033[48;2;0;255;0m\033[38;2;0;0;0m" + msg[0:floor(i / (100 / barLen))] + "\033[0m" + msg[floor(
            (i / (100 / barLen))):barLen - 1] + "] " + str(i) + "%", end = "", flush = True)
        sleep(0.02)
    bar = percentage


print_bar(0, "import: vocabulary")
from vocabulary.vocabulary import Vocabulary as vb

print_bar(8, "import: json")
import json

print_bar(15, "import: nltk.tokenize.word_tokenize")
from nltk.tokenize import word_tokenize

print_bar(35, "import: nltk.pos_tag")
from nltk import pos_tag

print_bar(68, "import: textstat.textstat.textstat")
from textstat.textstat import textstat

print_bar(80, "import: pattern.text.en.conjugate")
from pattern.text.en import conjugate

print_bar(100, "Done")


class SimpleSynonymFinder:
    words = []
    common = []
    model = []

    def __init__(self, w, com):
        self.words = word_tokenize(w)
        self.common = com
        self.model = pos_tag(self.words)
        print(self.model)

    def simplify(self):
        print(self.words)
        simplified = []
        simplified2 = []
        simplified3 = []
        for word in self.model:
            print("Word: ", word)
            shortest_syn = ""
            # synonyms = list(chain.from_iterable([word.lemma_names() for word in wordnet.synsets(word[0])]))
            synonyms_json = vb.synonym(word[0]) or []
            synonyms = [s["text"] for s in json.loads(synonyms_json)]
            if synonyms == [] or word[0].lower() in ' '.join(self.common):
                print("Either no synonym found or too common:", word)
                simplified.append(word[0])
                simplified2.append(word[0])
                simplified3.append(word[0])
                continue
            print(word[0] + "-->" + word[1])
            print(synonyms)
            best_synonym = sorted(synonyms, key = textstat.gunning_fog)[0]
            print(best_synonym)
            if "V" in word[1]:
                print("Cast: " + self.cast_base_verb(best_synonym, word[1]))
                simplified2.append(self.cast_base_verb(best_synonym, word[1]))
            else:
                print("Not a verb")
                simplified2.append(best_synonym)
            for definition in [e for e in synonyms if e in ' '.join(self.common)]:
                if len(definition) < len(shortest_syn) or shortest_syn == "":
                    shortest_syn = definition
            print("Selected definition: " + str(shortest_syn))
            simplified.append(shortest_syn)
            simplest = ""
            simplest_score = 100000000
            for definition in [e for e in synonyms if e in ' '.join(self.common)]:
                if textstat.gunning_fog(definition) < simplest_score:
                    simplest = definition
                    simplest_score = textstat.gunning_fog(definition)
            print(simplest)
            if "V" in word[1]:
                print("Cast: " + self.cast_base_verb(simplest, word[1]))
                simplified3.append(self.cast_base_verb(simplest, word[1]))
            else:
                print("Not a verb")
                simplified3.append(simplest)
        simp = ""
        for s in simplified:
            simp = simp + s
            # if s in ",.!;:?":
            simp = simp + " "
        simp2 = ""
        for s in simplified2:
            simp2 = simp2 + s
            # if s in ",.!;:?":
            simp2 = simp2 + " "
        simp3 = ""
        for s in simplified3:
            simp3 = simp3 + s
            # if s in ",.!;:?":
            simp3 = simp3 + " "
        return [simp, simp2, simp3]

    @staticmethod
    def cast_base_verb(verb, pos):
        if pos == "VB":
            # Verb, base
            return verb
        elif pos == "VBD":
            # Verb, past tense
            return conjugate(verb, tense = "past")
        elif pos == "VBG":
            # Verb, gerund or present participle
            return conjugate(verb, tense = "present", mood = "indicative", aspect = "progressive")
        elif pos == "VBN":
            # Verb, past participle
            return conjugate(verb, tense = "past", mood = "indicative", aspect = "progressive")
        elif pos == "VBP":
            # Verb, non 3rd-person singular present
            return conjugate(verb, tense = "present", person = 1, number = "singular", mood = "indicative",
                             aspect = "imperfective")
        elif pos == "VBZ":
            # Verb, 3rd-person singular present
            return conjugate(verb, tense = "present", person = 3, number = "singular", mood = "indicative",
                             aspect = "imperfective")
