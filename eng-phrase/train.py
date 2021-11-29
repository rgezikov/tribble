#!/usr/bin/env python3

import argparse
import random

pronouns = {
    's': ['I', 'you', 'he', 'she', 'it'],
    'p': ['we', 'you', 'they'],
}

verbs = {
    "to have": {
        "ps": {
            's': ['have', 'have', 'has', 'has', 'has'],
            'p': ['have', 'have', 'have'],
        }
    },
    "to be": {
        "ps": {
            's': ['am', 'are', 'is', 'is', 'is'],
            'p': ['are', 'are', 'are'],
        }
    }
}
verbs_inf = [*verbs]

questions = {
    "ps": {
        's': ['do', 'do', 'does', 'does', 'does'],
        'p': ['do', 'do', 'do']
    }
}

adj = ['small', 'big', 'tall', 'short', 'happy', 'sad', 'good', 'bad', 'cold', 'hot', 'strong', 'weak', 'fast', 'slow',
       'young', 'old']

subj = ['sharpener', 'notebook', 'book', 'ruler', 'rubber', 'pencil case', 'pen', 'pencil', 'felt-tip pen', 'crayons',
        'phone', 'scissors', 'lion', 'giraffe', 'tiger', 'elephant', 'gorilla', 'hippo', 'zebra', 'monkey', 'alligator',
        'rhino', 'parrot', 'cheetah']

forms = ['P', 'N', 'Q']
g_number = ['s', 'p']
tense = ['ps']

parser = argparse.ArgumentParser(description='Учим глаголы to have, to be')
parser.add_argument('-n', dest='num_tasks', required=False, type=int, default=10, help='Количество примеров')
args = parser.parse_args()

for i in range(args.num_tasks):
    miss_verb = random.randint(0, 100) > 30
    example = []
    f = forms[random.randint(0, len(forms) - 1)]
    gn = g_number[random.randint(0, len(g_number) - 1)]
    t = tense[random.randint(0, len(tense) - 1)]
    p_idx = random.randint(0, len(pronouns[gn]) - 1)
    pronoun = pronouns[gn][p_idx]
    example.append(pronoun)
    v_idx = random.randint(0, len(verbs_inf) - 1)
    v_inf = verbs_inf[v_idx]
    verb = verbs[v_inf][t][gn][p_idx]
    example.append(verb)
    if f == 'Q':
        if v_inf == 'to be':
            example = [example[1] if not miss_verb else f'_________({v_inf})', example[0]]
        else:
            example.insert(0, questions[t][gn][p_idx] if not miss_verb else f'_________')
            example[-1] = verbs[v_inf]['ps']['s'][0]
    elif f == 'N':
        if v_inf == 'to be':
            if miss_verb:
                example[-1] = f'_________({v_inf})'
            else:
                example.append('not')
        else:
            example = [example[0]]
            if not miss_verb:
                example.extend([questions[t][gn][p_idx], 'not', verbs[v_inf]['ps']['s'][0]])
            else:
                example.extend([f'_________({v_inf})'])
                # example = [example[0], questions[t][gn][p_idx] if not miss_verb else f'_________({v_inf})', 'not', verbs[v_inf]['ps']['s'][0]]
    else:
        example = [example[0], example[1] if not miss_verb else f'_________({v_inf})']

    adj_idx = random.randint(0, len(adj) - 1)
    subj_idx = random.randint(0, len(subj) - 1)
    example.extend(['a', adj[adj_idx], subj[subj_idx]])

    example[-1] += '?' if f == 'Q' else '.'

    example[0] = example[0][0].upper() + example[0][1:]
    print(f"{f} {' '.join(example)}")