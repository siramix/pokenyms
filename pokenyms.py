#!/usr/bin/python
# pokenyms.py
# Play pokenyms via command line

import random
import sys
import string
import time

NUM_BUTTONS = 10     # [Variable] Number of buttons to generate for each challenge

TRAIN_STR = "TRAIN"      # Parameter to train
PLAY_STR = "PLAY"        # Parameter to play the game
ALT_PLAY_STR = "PLAY2"   # Parameter to play the game with no extra letters
SKIP_STR = "SKIP"        # Command to skip an anagram during play

CLUE_WAIT = 5            # Seconds to wait before showing a clue
SKIP_TIME = 30           # Seconds to wait before player can skip
GAME_LIMIT = 10          # Number of anagrams to play during a battle (not training)


def usage():
    print "Usage: "
    print "pokenyms.py %s|%s|%s" % (TRAIN_STR, PLAY_STR, ALT_PLAY_STR)
    print "\t%s:\tSolve just a couple for practice." % TRAIN_STR
    print "\t%s:\tPlay a standard game WITH decoys and a generated dictionary." % PLAY_STR
    print "\t%s:\tPlay a modified game with no decoys and a buzzwords dictionary." % ALT_PLAY_STR
    exit()


def prompt_user(play_type):
    """
    Print out either the training prompt or the play prompt. Wait
    for the player to press enter after.
    """
    if (play_type == TRAIN_STR):
        print color.ORANGE + "Ahhhh a fellow pokenym trainer. \nI see you are green " \
            + "around the ears.\nHow about you play one just to get our feet wet." \
            + "  Once you have trained, come see me again and let's " \
            + color.BOLD + color.GREEN + "PLAY." + color.ENDC
    if (play_type == PLAY_STR):
        print color.RED + "You dare battle my pokenyms?!\n" \
            + "You are foolish to challenge me, but I accept." + color.ENDC

    print color.ORANGE + "\nRules:" + color.ENDC
    print "1. Solve the pokenym presented to you by typing it in and pressing enter."
    print "2. Make as many guesses as you want."
    print "3. Hitting enter will also update the clues."
    print "4. Up to five new clues will be presented to you, one every %d seconds" % CLUE_WAIT
    print "5. After %d seconds you will be given the option to SKIP at no penalty." % SKIP_TIME
    print "\nWhen you are ready to begin battle, press Enter:"
    inputchar = 'x'
    while inputchar != '\n':
        inputchar = sys.stdin.read(1)


def play_anagram(num_anagrams):
    """
    Play a given number of anagrams and print out the total time taken to
    finish.
    """
    total_time = 0.0
    for i in range(num_anagrams):
        anagram = game.get_next_anagram()
        total_time += battle_anagram(anagram)
    final_msg = color.GREEN + "\nFinished battle in %f seconds." + color.ENDC
    print (final_msg % total_time)


def print_challenge(anagram, buttons):
    """
    Print out the blanks corresponding to the anagram key. Then
    print out all of the buttons that a player could choose from.
    """
    print color.RED + "Pokenym GO!" + color.ENDC
    key = anagram.get_anagram_key()
    anagram_len = len(key)

    blanks = ''
    for i in range(anagram_len):
        blanks += "_"
    print blanks
    print "(%i letters long)" % anagram_len

    # Print out correct number of buttons for each play mode
    if PLAY_MODE == ALT_PLAY_STR:
        num_buttons = anagram_len
    elif PLAY_MODE == PLAY_STR or PLAY_MODE == TRAIN_STR:
        num_buttons = NUM_BUTTONS

    for i in range(num_buttons):
        print color.BLUE + buttons[i] + color.ENDC,
    if PLAY_MODE != ALT_PLAY_STR:
        print "\n(some may be decoys!)"


def generate_buttons(anagram):
    """
    Generate a set number of buttons based on the anagram
    passed in, avoiding duplicates and stupid letters.
    """
    key = anagram.get_anagram_key()
    anagram_len = len(key)

    # Number of buttons depends on play mode
    # For standard play, there will be decoys which
    # means NUM_BUTTONS must always exceed max key length
    if PLAY_MODE == ALT_PLAY_STR:
        num_buttons = anagram_len
    elif PLAY_MODE == PLAY_STR or PLAY_MODE == TRAIN_STR:
        assert(anagram_len <= NUM_BUTTONS)
        num_buttons = NUM_BUTTONS

    buttons = ['' for x in xrange(num_buttons)]
    # First fill in the correct buttons
    for i in range(anagram_len):
        buttons[i] = key[i].upper()
    # Now fill in decoy buttons (no dupes)
    if PLAY_MODE == PLAY_STR:
        for i in range(NUM_BUTTONS - anagram_len):
            new_btn = random.choice(string.letters).upper()
            while new_btn in buttons or new_btn == 'X':
                new_btn = random.choice(string.letters).upper()
            buttons[i+anagram_len] = new_btn

    random.shuffle(buttons)
    return buttons


def battle_anagram(anagram):
    """
    Prints the anagram and after a set interval will display additional
    clues to the player.  Once the player gets it right or a time limit has
    been reached, print out and return the time taken.

    @return time_taken Time taken to skip or defeat the anagram
    """
    start = time.time()
    time_taken = 0
    buttons = generate_buttons(anagram)
    related_len = len(anagram.get_relateds())
    entry = ''
    skipped = False

    # Print the challenge and wait for a correct or skip. 'Wipe' console after
    # each guess.
    while entry != anagram.get_anagram_key():
        # Hack to clear screen
        for i in xrange(0, 100):
            print ''
        print_challenge(anagram, buttons)
        time_taken = time.time() - start
        # Print out progressively more clues as time goes by
        print '\nClues:'
        for i in (range(min(int(time_taken / CLUE_WAIT)+1, related_len))):
            print(color.ORANGE + anagram.get_relateds()[i] + color.ENDC)
        print("\n\n%f seconds taken so far. Make a guess: " % time_taken)

        if (time_taken >= SKIP_TIME):
            print ((color.ORANGE + "(More than %d seconds have gone by. "
                    + "Type SKIP to skip, if you're lame.)" + color.ENDC) % SKIP_TIME)

        # Get another guess or 'SKIP'
        entry = sys.stdin.readline().upper().strip()

        # Allow user to skip after a configurable amount of time
        if (entry == SKIP_STR and time_taken >= SKIP_TIME):
            skipped = True
            break

    # Recalculate time taken from start
    time_taken = time.time() - start

    # Print out results of battle and return the time taken to win or skip
    if not skipped:
        print color.GREEN + "Pokenym defeated in %f seconds!" % (time_taken) + color.ENDC
    else:
        print color.RED + "Defeated by %s!" % (anagram.get_anagram_key()) + color.ENDC
    print "Press Enter to fight your next pokenym."
    inputchar = 'x'
    while inputchar != '\n':
        inputchar = sys.stdin.read(1)
    return time_taken


class Anagram(object):
    """
    A tuple of a string and then five related strings.
    For sanity's sake all entries are uppered.
    """
    def get_anagram_key(self):
        return self.ANAGRAM_KEY

    def get_relateds(self):
        return self.RELATEDS

    def __init__(self, anagram, relateds):
        super(Anagram, self).__init__()
        self.ANAGRAM_KEY = anagram.upper()
        self.RELATEDS = ['' for x in xrange(len(relateds))]
        for i in range(len(relateds)):
            self.RELATEDS[i] = relateds[i].upper()


class TrainingAnagrams:
    """
    Stores just training Anagrams.
    """
    INDEX = -1
    ANAGRAMS = [Anagram('', '') for x in xrange(11)]

    def get_next_anagram(self):
        self.INDEX += 1
        return self.ANAGRAMS[self.INDEX]

    def __init__(self):
        self.ANAGRAMS[0] = Anagram('future', ['by-and-by', 'hereafter', 'destiny', 'tomorrow', 'eventuality'])


class BattleAnagrams:
    """
    Stores the primary set of Anagrams to play with.
    """
    INDEX = -1
    ANAGRAMS = [Anagram('', '') for x in xrange(11)]

    def get_next_anagram(self):
        self.INDEX += 1
        return self.ANAGRAMS[self.INDEX]

    def __init__(self):
        self.ANAGRAMS[0] = Anagram('bazaar', ['emporium', 'store', 'market', 'outlet', 'boutique'])
        self.ANAGRAMS[1] = Anagram('greenhorn', ['abecedarian', 'apprentice', 'amateur', 'freshman', 'rookie'])
        self.ANAGRAMS[2] = Anagram('clobber', ['batter', 'bludgeon', 'lambaste', 'pummel', 'annihilate'])
        self.ANAGRAMS[3] = Anagram('traffic', ['business', 'marketplace', 'trade', 'commerce', 'dealings'])
        self.ANAGRAMS[4] = Anagram('special', ['distinguished', 'defined', 'best', 'extraordinary', 'distinctive'])
        self.ANAGRAMS[5] = Anagram('garment', ['apparel', 'array', 'attire', 'costume', 'covering'])
        self.ANAGRAMS[6] = Anagram('danger', ['distress', 'harm\'s way', 'imperilment', 'jeopardy', 'risk'])
        self.ANAGRAMS[7] = Anagram('bride', ['mate', 'newlywed', 'spouse', 'wife', 'better half'])
        self.ANAGRAMS[8] = Anagram('tribute', ['accolade', 'acknowledgement', 'applause', 'appreciation', 'commendation'])
        self.ANAGRAMS[9] = Anagram('lasso', ['bola', 'halter', 'rope', 'snare', 'capture'])


class BuzzwordsAnagrams:
    """
    Stores anagrams from Buzzwords. Should be a less predicable and more fun experience than
    the BattleAnagrams.
    """
    INDEX = -1
    ANAGRAMS = [Anagram('', '') for x in xrange(11)]

    def get_next_anagram(self):
        self.INDEX += 1
        return self.ANAGRAMS[self.INDEX]

    def __init__(self):
        self.ANAGRAMS[0] = Anagram('Spreadsheet', ['EXCEL', 'NUMBERS', 'MATH', 'EQUATIONS', 'TABLE'])
        self.ANAGRAMS[1] = Anagram('Spiritual', ['BELIEF', 'RELIGION', 'FAITH', 'GOD', 'HOLY'])
        self.ANAGRAMS[2] = Anagram('Blister', ['POP', 'SKIN', 'HEEL', 'HANDLE', 'FOOT'])
        self.ANAGRAMS[3] = Anagram('Motherboard', ['COMPUTER', 'PROCESSOR', 'BOOT', 'CIRCUIT', 'CHIP'])
        self.ANAGRAMS[4] = Anagram('Bar Stool', ['DRINK', 'SIT', 'CHAIR', 'FIGHT', 'KITCHEN'])
        self.ANAGRAMS[5] = Anagram('Therapist', ['ANALYZE', 'DOCTOR', 'COUCH', 'SHRINK', 'PSYCHIATRIST'])
        self.ANAGRAMS[6] = Anagram('Whirlpool', ['WATER', 'SPIN', 'RIVER', 'SWIRL', 'APPLIANCE'])
        self.ANAGRAMS[7] = Anagram('Calculus', ['MATH', 'FUNCTION', 'DERIVATIVE', 'INTEGRAL', 'LIMIT'])
        self.ANAGRAMS[8] = Anagram('Illiterate', ['READ', 'WRITE', 'WORD', 'SCHOOL', 'EDUCATE'])
        self.ANAGRAMS[9] = Anagram('Beatbox', ['RHYTHM', 'DRUM', 'MOUTH', 'SOUND', 'MUSIC'])


class color:
    """
    Helper class for printing color strings to the console.
    """
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    ORANGE = '\033[93m'
    RED = '\033[91m'
    BOLD = "\033[1m"
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.BLUE = ''
        self.GREEN = ''
        self.ORANGE = ''
        self.RED = ''
        self.BOLD = ''
        self.ENDC = ''

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
    # Either train (one game) or play pokenyms
    global PLAY_MODE
    PLAY_MODE = sys.argv[1]
    if PLAY_MODE == TRAIN_STR:
        game = TrainingAnagrams()
        prompt_user(TRAIN_STR)
        play_anagram(1)
    elif PLAY_MODE == PLAY_STR:
        # 10 word game of standard pokenyms (decoy letters, dictionary words)
        game = BattleAnagrams()
        prompt_user(PLAY_STR)
        play_anagram(GAME_LIMIT)
    elif PLAY_MODE == ALT_PLAY_STR:
        # 10 word game of buzzwords pokenyms
        game = BuzzwordsAnagrams()
        prompt_user(PLAY_STR)
        play_anagram(GAME_LIMIT)
    else:
        usage()
