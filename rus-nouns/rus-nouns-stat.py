import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import multiprocessing
import os
import re

from typing import List, Dict

THIS_SCRIPT_PATH = os.path.dirname(__file__)
RUSSIAN_LETTERS = "абвгдежзийклмнопрстуфхцчшщьыъэюя"


class LetterScheme:
    def __init__(self, known:str=None, not_here:str=""):
        self.known = known
        self.not_here = not_here

    def to_regex(self):
        if self.known:
            return self.known
        if self.not_here:
            return f"[^{self.not_here}]"
        return "."

    def __str__(self):
        return f"'{self.known}';{self.not_here}"

    def __repr__(self):
        return str(self)

class WordScheme:
    def __init__(self, letters: List[LetterScheme], not_present:str):
        self.letters = letters
        self.not_present = not_present

    def to_regex(self):
        return "".join([l.to_regex() for l in self.letters])

    def __str__(self):
        return f"{{'{self.to_regex()}';'{self.not_present}'}}"

    def __repr__(self):
        return str(self)

    def allowed_letters(self):
        allowed = ""
        for ls in self.letters:
            if ls.known and ls.known not in allowed:
                allowed += ls.known
            if ls.not_here:
                for lnh in ls.not_here:
                    if lnh not in allowed:
                        allowed += lnh
        return allowed

    def update(self, candidate, match_result):
        all_known = ""
        for i, l in enumerate(match_result):
            if l == 'M':
                self.letters[i].known = candidate[i]
                all_known += candidate[i]
            elif l == 'P':
                self.letters[i].not_here += candidate[i]

        for i, l in enumerate(match_result):
            if l not in "MP":
                if l not in all_known:
                    self.not_present += l
                else:
                    self.letters[i].not_here += l

    def all_guessed(self):
        return all([x.known is not None for x in self.letters])

class WordsDB:
    NOUNS_FILE_NAME = os.path.abspath(os.path.join(THIS_SCRIPT_PATH, 'Russian-Nouns', 'dist', 'russian_nouns.txt'))
    LETTERS_NUM = 5

    def __init__(self):
        self.letter_counter: Dict[str, int] = None
        self.word_weights: Dict[str, int] = None
        self.words = self.get_nouns(WordsDB.LETTERS_NUM)
        self.calculate_statistics()

    @staticmethod
    def get_nouns(word_len:int):
        with open(WordsDB.NOUNS_FILE_NAME, 'r') as nouns_file:
            nouns = [line.strip() for line in nouns_file]
        nouns = list(filter(lambda x: len(x) == word_len, nouns))
        nouns = [x for x in nouns if '-' not in x]
        nouns = [x.replace('ё', 'е') for x in nouns]
        return nouns

    @staticmethod
    def word_weight(letter_counter:dict, word:str):
        weight = 0
        used_letters = ""
        for letter in word:
            if letter not in used_letters:
                weight += letter_counter[letter]
                used_letters += letter
        return weight


    def calculate_statistics(self):
        self.letter_counter =  {}
        for letter in RUSSIAN_LETTERS:
            self.letter_counter[letter] = 0
        for word in self.words:
            for letter in word:
                self.letter_counter[letter] += 1
        self.word_weights = {}
        for word in self.words:
            self.word_weights[word] = self.word_weight(self.letter_counter, word)

    def get_matching_words(self, present, not_allowed, regex):
        regex_comp = re.compile(regex) if regex else None
        words = []
        for word in self.words:
            wrong_one = False
            if not_allowed:
                for letter in word:
                    if letter in not_allowed:
                        wrong_one = True
                        break
            if wrong_one:
                continue
            if present:
                for letter in present:
                    if letter not in word:
                        wrong_one = True
                        break
            if wrong_one:
                continue
            if regex_comp:
                if not regex_comp.match(word):
                    continue
            words.append(word)
        return words

    def find_word(self, word_scheme:WordScheme):
        present:str = word_scheme.allowed_letters()
        not_allowed:str = word_scheme.not_present
        regex = word_scheme.to_regex()

        matching_words = self.get_matching_words(present, not_allowed, regex)
        sorted_matching_words = sorted(matching_words, key=lambda x: self.word_weights[x], reverse=True)
        return sorted_matching_words

def calculate_result(hidden, candidate):
    result = candidate
    hidden_no_present = hidden
    for i, (h, c) in enumerate(zip(hidden, candidate)):
        if h == c:
            result = f"{result[:i]}M{result[i+1:]}"
            hidden_no_present = f"{hidden_no_present[:i]}_{hidden_no_present[i+1:]}"
    for i, (h, c) in enumerate(zip(hidden, candidate)):
        if h != c:
            if c in hidden_no_present:
                result = f"{result[:i]}P{result[i+1:]}"
    return result

def solve(hidden_word):
    current_scheme = WordScheme([LetterScheme() for i in range(WordsDB.LETTERS_NUM)], "")

    for fw in init_words:
        result = calculate_result(hidden_word, fw)
        current_scheme.update(fw, result)

    iteration = len(init_words)

    while True:
        iteration += 1
        found_words = wdb.find_word(current_scheme)
        result = calculate_result(hidden_word, found_words[0])
        # print(iteration, found_words[0])
        # print(iteration, result)
        current_scheme.update(found_words[0], result)
        # print(iteration, current_scheme)
        if current_scheme.all_guessed():
            return iteration, current_scheme


def solve_function(word_list:List[str], results):
    guessed = {}
    for word in word_list:
        i, scheme = solve(word)
        guessed[word] = (i, scheme)
    results.update(guessed)

init_words = []

if __name__ == "__main__":
    wdb = WordsDB()

    # init_words = []
    # current_scheme = WordScheme([LetterScheme() for i in range(WordsDB.LETTERS_NUM)], "")
    #
    # init_words.append(wdb.find_word(current_scheme)[0])
    # current_scheme.update(init_words[-1], init_words[-1])
    # init_words.append(wdb.find_word(current_scheme)[0])
    # current_scheme.update(init_words[-1], init_words[-1])
    # init_words.append(wdb.find_word(current_scheme)[0])
    #
    # print(init_words)

    out_hist = []

    init_words_list = [[], ['кроат', 'селин'], ['стужа', 'бидон']]

    for iw in init_words_list:
        # continue
        init_words = iw
        num_processes = 10
        part_size = len(wdb.words) // num_processes
        pool = multiprocessing.Pool(processes=num_processes)
        manager = multiprocessing.Manager()
        results = manager.dict()
        parts = [wdb.words[i:i + part_size] for i in range(0, len(wdb.words), part_size)]
        pool.starmap(solve_function, [(part, results) for part in parts])
        pool.close()
        pool.join()

        combined_results = dict(results)
        sorted_guessed = sorted(combined_results.items(), key=lambda x: x[1][0])

        total_attempts = 0
        in_6_attempts = 0
        hist = {i:0 for i in range(1, 12)}
        for sg in sorted_guessed:
            # print(sg)
            n_attempts = sg[1][0]
            total_attempts += n_attempts
            hist[n_attempts] += 1
            if n_attempts <= 6:
                in_6_attempts += 1

        print(f"{'-'*50}")
        print(f"init_words: {init_words}")
        print(f"total_attempts: {total_attempts}")
        print(f"in_6_attempts: {in_6_attempts}")
        print(f"hist: {hist}")
        out_hist.append(hist)

    # out_hist = [
    #     {1: 10, 2: 5, 3: 12, 4: 8, 5: 15},
    #     {1: 8, 2: 6, 3: 10, 4: 5, 5: 12},
    #     {1: 6, 2: 7, 3: 9, 4: 11, 5: 14}
    # ]

    alpha = [1.0, 0.5, 0.7]
    labels = list(out_hist[0].keys())
    x = np.arange(len(labels))
    for i, (h, iw, a) in enumerate(zip(out_hist, init_words_list, alpha)):
        values = list(h.values())
        cumulative_probs = np.cumsum(values) / sum(values)
        plt.plot(h.keys(), cumulative_probs, label=f"{iw}", alpha=a)
    plt.xlabel('Num of attempts')
    plt.ylabel('Counts')
    plt.title('Histograms')
    plt.legend()
    plt.show()