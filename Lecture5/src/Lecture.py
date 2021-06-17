# # COMPUTATIONAL MORPHOLOGY WITH HFST TOOLS - LECTURE 5
#
# <ul>
#  <li><a href="#1.-Big-picture">1. Big picture</a></li>
#  <li><a href="#2.-Guessers-and-stemmers">2. Guessers and stemmers</a></li>
#  <li><a href="#3.-Pronunciation-lexicon-for-a-Language-with-(almost)-regular-Orthography:-Brazilian-Portuguese">3. Pronunciation lexicon for a Language with (almost) regular Orthography: Brazilian Portuguese</a></li>
#  <li><a href="#4.-Regular-expressions-in-xfst">4. Regular expressions in xfst</a></li>
#  <li><a href="#5.-Pronunciation-lexicon-for-a-Language-with-Irregular-Orthography:-English">5. Pronunciation lexicon for a Language with Irregular Orthography: English</a></li>
#  <li><a href="#6.-Sound-Change-in-Indo-European-languages">6. Sound Change in Indo-European languages</a></li>
#  <li><a href="#7.-Assignments">7. Assignments</a></li>
# </ul>
#
# ## 1. Big picture
#
# ### 1.1. lexc
#
# "Lexicon without any replace rules"
#
# <img src="img/big_picture_lexc.png">
#
# ### 1.2. xfst and twolc
#
# "Lexicon combined with replace rules"
#
# <img src="img/big_picture_xfst_and_twolc.png">
#
# ### 1.3. xfst / regular expressions
#
# "Rules without much of a lexicon" 
#
# <img src="img/big_picture_xfst_and_regexps.png">
#
# ## 2. Guessers and stemmers
#
# ### 2.1. Increased coverage with guessers 
#
# <ul>
# <li>Section 9.5.4 in the Beesley & Karttunen book</li>
# <li>A finite-state morphological analyzer only recognizes the words that are included in its lexc lexicon.</li>
# <li>It may take several person-months (or even years) of work to build up a lexicon with the tens of thousands of stems necessary for broad coverage of real text.</li>
# <li>As an alternative, or a complement, one can use</li>
# <ul>
#   <li>guessers</li>
#   <li>stemmers</li>
#   <li>unsupervised morphology</li>
# </ul>
# </ul>
#
# ### 2.2. Definition of a guesser
#
# <ul>
# <li>A guesser is designed to analyze words that are based on any phonologically possible stem.</li>
# <li>The set of phonologically possible stems is definable, more or less precisely, using regular expressions and scripts.</li>
# <li>Useful</li>
# <ul>
#   <li>as a general backup when normal morphological analysis fails</li>
#   <li>for suggesting new stems that need to be added to the lexicon</li>
# </ul>
# </ul>
#
# ### 2.3. Case study: Esperanto verb guesser lexicon
#
# <img src="img/esperanto_lexc.png">
#
# ### 2.4. Case study: Esperanto verb guesser xfst script
#

from hfst_dev import XfstCompiler
comp = XfstCompiler()
script ="""
clear stack

! We limit ourselves here to lower case letters and ignore some Esperanto letters not found in the
! ASCII character set
define Vowel     a | e | i | o | u ;
define ConsClust b | c | d | f | g | h | j | k | l | m | n | p | r | s | t | v | z |
                 k r | p r | t r | g r | b r | d r | s k | s p | s t ;

                 ! Each verb root must be of the format Cc V Cc V Cc V Cc ..., where the first consonant cluster Cc is
                 ! optional and it must be followed by at least one pair of V Cc ( = vowel + consonant cluster):
                 define PossibleVerbRoot  ( ConsClust ) [ [ Vowel ] [ ConsClust ] ]+ "+Guess":0 ;

                 ! The lexc description is compiled and pushed on the stack
                 read lexc esperanto.lexc

                 ! Using the 'substitute defined' command, the placeholder symbol is replaced by the value of PossVerbRoot
                 substitute defined PossibleVerbRoot for ^GUESSVERBROOT

                 ! Make verb vocabulary ready to use
                 define AllPossibleVerbs ;
                 regex AllPossibleVerbs ;
"""
comp.parse_line(script)

# ### 2.5. Case study: Esperanto verb guesser example output
#
# Try the following commands:
#
# ```
# up donadas     random-upper     random-lower
# ```

comp.parse_line('up donadas')

# You should get something like this as a result for up donadas:
#
# ```
# don+Guess+Verb+Cont+Pres
# don+Verb+Cont+Pres
# donad+Guess+Verb+Pres
# ```

comp.parse_line('random-upper')

# for random-upper:
#
# ```
# dip+Guess+Verb+Fut
# egrust+Guess+Verb+Subj
# fust+Guess+Verb+Fut
# obr+Guess+Verb+Cont+Fut
# opop+Guess+Verb+Cond
# ```

comp.parse_line('random-lower')

# for random-lower:
#
# ```
# etros
# hemodas
# jumadis
# soski
# tozezus
# ugrucas
# vabis
# ```

# ### 2.6. Stemming
#
# <ul>
#  <li>A term used particularly in information retrieval to describe the process of reducing inflected (or sometimes derived) words to their word stem, base or root form — generally a written word form.</li>
#  <ul>
#   <li>The stem is “fish” for “fishing”, “fished”, and “fisher”.</li>
#   <li>The stem is “argu” for “argue”, “argued”, “argues”, “arguing”, and “argus”...(!)</li>
#  </ul>
#  <li>The stem does not need to be identical to the morphological root of the word.</li>
#  <ul>
#   <li>It is sufficient that related words map to the same stem, even if this stem is not in itself a valid root, such as the stem “argu” above, or the stem “citi” for “city” and “cities”.</li>
#  </ul>
#  <li>Algorithms for stemming have been studied in computer science since the 1960s.</li>
#  <li>Many search engines treat words with the same stem as synonyms, as a kind of query expansion, a process called conflation.</li>
# </ul>
#
# #### Porter’s stemmer (1979-1980)
#
# <ul>
#  <li>Idea:</li>
#  <ul>
#   <li>Remove what looks like suffixes of English words</li>
#   <li>Tidy up a bit</li>
#  </ul>
#  <li>Feasible for English with such “simple morphology”</li>
#  <li>The full algorithm is described <a href="http://tartarus.org/martin/PorterStemmer/def.txt">here</a>.</li>
#  <li>There are other English stemmers:</li>
#  <ul>
#   <li>Snowball</li>
#   <li>Lancaster</li>
#   <li>They are more “aggressive” than the Porter stemmer; they remove more “suffixes”.</li>
#  </ul>
# </ul>
#
# <img src="img/porters_stemmer.png">

# ## 3. Pronunciation lexicon for a Language with (almost) regular Orthography: Brazilian Portuguese
#
# ### 3.1. Transducing between orthographic and pronounced forms of words
#
# <ul>
#  <li>Section 3.5.4 in the Beesley & Karttunen book</li>
#  <li>Exercise on Portuguese Brazilian</li>
#  <li>The task is to create a cascade of rules that maps from orthographical strings in Portuguese (this will be the lexical side) down to strings that represent their pronunciation (this will be the surface side).</li>
#  <ul>
#   <li>There will not be a lexicon.</li>
#   <li>A sample mapping of written “caso” to spoken “kazu” looks like this:
# <pre>
# Lexical: caso
# Surface: kazu
# </pre></li>
#  </ul>
# </ul>
#
#
# ### 3.2. Phonetic symbols for Portuguese
#
# <img src="img/phonetic_symbols_for_portuguese.png">
#
# <i>Table from Beesley & Karttunen: Finite State Morphology, CSLI Publications, 2003.</i>
#
# ### 3.3. Some example words
#
# What applications that you can think of need a mapping between orthographic and pronounced forms?
#
# <img src="img/test_data_for_portuguese.png">
#
# <i>Table from Beesley & Karttunen: Finite State Morphology, CSLI Publications, 2003.</i>
#
# ### 3.4. Conversion from orthography to pronunciation for Brazilian Portuguese
#

from hfst_dev import compile_xfst_script
compile_xfst_script(
"""
define Vowel [ a | e | i | o | u
             | á | é | í | ó | ú
             | â | ê |     ô
             | ã |         õ
             | à
             |                 ü
] ;

define Rule1 [ s -> z || Vowel _ Vowel ];

define Rule2 [ ç -> s ];

define Rule3 [ c h -> %$ ];

define Rule4 [ c -> s || _ [ e | i | é | í | ê ] ];

define Rule5 [ c -> k ];

define Rule6 [ s s -> s ];

define Rule7 [ n h -> N ];

define Rule8 [ l h -> L ];

define Rule9 [ h -> 0 ];

define Rule10 [ r r -> R ];

define Rule11 [ r -> R || .#. _ ];

define Rule12 [ e -> i || _ (s) .#. , .#. p _ r ];

define Rule13 [ o -> u || _ (s) .#. ];

define Rule14 [ d -> J || _ [ i | í ] ];

define Rule15 [ t -> C || _ [ i | í ] ];

define Rule16 [ z -> s || _ .#. ];

read regex Rule1 .o. Rule2 .o. Rule3 .o. Rule4 .o. Rule5 .o. Rule6 .o. Rule7 .o. Rule8 .o.
Rule9 .o. Rule10 .o. Rule11 .o. Rule12 .o. Rule13 .o. Rule14 .o. Rule15 .o. Rule16 ;

invert net
minimize net
apply up
disse
simpático
chato
braços
""")

#
# ### 3.5. Alternative: Don't define individual rules, but rather one large regular expression
#
# <img src="img/alternative_for_portuguese.png">

# ## 4. Regular expressions in xfst
#
# <i>Figures and tables taken from Beesley & Karttunen: Finite State Morphology, CSLI Publications, 2003.</i>
#
# ### 4.1. Kleene (1956): Formal language theory
#
# <img src="img/kleene_formal_language_theory.png">
#
# #### Examples (1)
#
# <img src="img/kleene_example_1.png">
#
# #### Examples (2)
#
# <img src="img/kleene_example_2.png">
#
# #### Examples (3)
#
# <img src="img/kleene_example_3.png">

# ### 4.2. Writing regular expressions in xfst
#
# #### Writing regular expressions in xfst (1)
#
# ```
# read regex d o g | c a t | h o r s e ;
# print words
# ```
#
# Test by copying the above and giving it as input for interactive xfst program:

from hfst_dev import start_xfst
start_xfst()

# Also test the examples given below. <b>NOTE: Do not start xfst shell if you already
# have an xfst shell running.</b> If you wish to start another shell, first exit
# the current shell with command `exit`.

# #### Writing regular expressions in xfst (2)
#
# ```
# read regex [ d o g | c a t | r a t | e l e p h a n t ] - [ d o g | r a t ];
# print words
# ```
#
# #### Writing regular expressions in xfst (3)
# ```
# read regex (r e)[[m a k e] | [c o m p i l e]]
# print words
# ```
#
# It is a bit like writing a lexicon in xfst without using lexc.
#
# #### Writing regular expressions in xfst (4)
#
# ```
# read regex a b c* d (e) f+ ;
# random-words
# ```
#
# #### Writing regular expressions in xfst (5)
#
# ```
# read regex [ g o:e o:e s e | m o:i u:0 s:c e | b o o k 0:s ] ;
# upper-words
# lower-words
# down mouse
# ```

# ### 4.3. Summary: Regular expression syntax in xfst for repetition
#
# <img src="img/xfst_repetition.png">
#
# #### Syntax for complement (= something other than)
#
# <img src="img/xfst_complement.png">
#
# #### Writing regular expressions in xfst (6)
#
# ```
# read regex [ b o b | j o b | r o b | k n o b ] .o. [ o -> u || \[b | j | n] _ ];
# upper-words
# lower-words
# ```
#
# #### Syntax for contain/ignore (= is part of)
#
# <img src="img/xfst_contain_ignore.png">
#
# #### Writing regular expressions in xfst (7)
#
# ```
# read regex [[t a l o | k y l ä | k o r i] s s A] .o. [ A -> a || $[a|o|u] ~$[ä|ö|y] _ ] .o. [ A -> ä ] ;
# upper-words
# lower-words
# ```
#
# #### Writing regular expressions in xfst (8)
#
# ```
# read regex [[{talo} | {kylä} | {kori}] {ssA}] .o. [ A -> a || $[a|o|u] ~$[ä|ö|y] _ ] .o. [ A -> ä ] ;
# upper-words
# lower-words
# ```
#
# You can write a sequence of symbols, such as t a l o, together, if you enclose it in curly brackets: {talo}.

start_xfst()

# ## 5. Pronunciation lexicon for a Language with Irregular Orthography: English
#
# <i>Figures taken from Jurafsky & Martin: Speech and Language Processing, Prentice Hall, 1999.</i>
#
# ### 5.1. Symbol set for English pronunciation
#
# <img src="img/english_phonemes.png">
#
# ### 5.2. "Two levels times two"
#
# <ul>
#  <li>We do not transduce between the orthographic form and the pronounced form.</li>
#  <li>We transduce between the morphological lexical form and surface form (as earlier on this lecture).</li>
#  <li>Every input and output symbol consists of two parts:</li>
#  <ul>
#   <li>orthographic form</li>
#   <li>pronounced form</li>
#   <li>For instance: o|aa</li>
#  </ul>
# </ul>
#
# <img src="img/two_levels_times_two.png">
#
# ### 5.3. Example entries from the noun stem lexicon
#
# <img src="img/example_entries.png">
#
# ### 5.4. Transducer for singular and plural inflection
#
# <img src="img/singular_and_plural_inflection.png">
#
# ### 5.5. Noun stems and inflections composed
#
# <img src="img/noun_stems_and_inflections_composed.png">

# ## 6. Sound Change in Indo-European languages
#
# ### 6.1. Research initiative
#
# <ul>
#  <li>Creation of an interactive lexicon available on the Internet</li>
#  <li>Using finite-state alternation rules to model sound change from Proto-Indo-European (PIE) to descendant languages</li>
#  <li>HFST Foma engine (similar to HFST xfst)</li>
#  <li>People</li>
#  <ul>
#   <li>Jouna Pyysalo</li>
#   <li>Måns Huldén</li>
#  </ul>
# <li><a href="http://pielexicon.hum.helsinki.fi/">Project homepage</a></li>
# </ul>
#
# <img src="img/pie_lexicon.png">
#
# #### Example 1: Autumn, End
#
# <img src="img/autumn_end.png">
#
# #### Example 2: Spring, Warmth
#
# <img src="img/spring_warmth.png">

# ## More information
#
# <ul>
#  <li>Selected parts of Chapter 2 and 3 of the Beesley & Karttunen book: “A Systematic Introduction” and “The xfst Interface”</li>
# </ul>
#
# ## 7. Assignments
#
# ### Assignment 5.1: Analysis of vocabularies
#
# The HFST project has produced open-source morphological analyzers for some languages.
# You can download them from <a href="https://korp.csc.fi/download/hfst-morphologies/">Kielipankki (The Language Bank of Finland) pages</a>.
#
# <b>a.</b> Decide what language you want to work on.
# You can choose one of the following analyzers:
# <a href="https://korp.csc.fi/download/hfst-morphologies/en/wn-bnc/">English</a>,
# <a href="https://korp.csc.fi/download/hfst-morphologies/fi/omorfi/">Finnish</a>,
# <a href="https://korp.csc.fi/download/hfst-morphologies/test/fr/morphalou/">French</a>,
# <a href="https://korp.csc.fi/download/hfst-morphologies/test/de/morphisto-smor/">German</a>,
# <a href="https://korp.csc.fi/download/hfst-morphologies/sv/dsso/">Swedish</a>,
# or <a href="https://korp.csc.fi/download/hfst-morphologies/test/tr/trmorph/">Turkish</a>.
#
# Download the zip package, extract it, and search for file with extension `.hfst`. This is the analyzer file.
#
# <b>b.</b> Read the transducer from file and test it with HfstTransducer.read_from_file and HfstTransducer.lookup.
# Type in a few word forms and check what analyses you get for these word forms (the format of the tags is slightly different in the different languages).

pass # <write your solution here>

# Perform the same test in an interactive xfst shell (open it with with start_xfst). Use commands `load stack` and `lookup` instead.

pass # <write your solution here>

# <b>c.</b> Pick a text file containing words of the language you chose.
# There should be one word per line in the file.
# If you don’t have any text file available, you can use one of the pre-prepared files english-words.txt, finnish-words.txt, french-words.txt, german-words.txt or swedish-words.txt.
# For reading, you can use Python's `open(path,mode)` and `<file>.read()`, `<file>.readline()`, or `<file>.readlines()`.
#
# <b>d.</b> Run the entire text file through the analyzer, as follows:

# <you must edit the code so that it will work for the language you have chosen>
for line in some_text_file:
    some_analyzer.lookup(line)

# <b>e.</b> Browse through the analyses of the words.
# Find a few words that are out-of-vocabulary, that is, the analyzer does not recognize them and cannot provide any analysis.
# Why aren't these words covered in the vocabulary of the analyzer?

# ### Assignment 5.2: Creating a translating guesser
#
# Your task is to create a guesser that translates words between related languages or dialects.
# For instance, in the attached file there is an example xfst script that translates English words ending in “-ity” to Swedish words ending in “-itet”.
#
# For instance,
#
# * down electricity produces elektricitet,
# * down university produces universitet, and
# * down popularity produces popularitet.
#
# You can solve this tasks in two ways:
# 
# * either using only an xfst script as in English-to-Swedish translation example,
# * or using a lexc file in combination with an xfst script as in the Esperanto guesser (check lecture slides).
#
# If you use a lexc file you can do translation between suffixes of two languages in the continuation lexicons, such that the lexical form of a suffix is “ity” and its surface form is “itet”.
#
# * a. Choose the two languages you want to translate between.
# * b. You must have a regular expression that produces plausible words (or stems) in your source language.
# * c. Implement at least two translation rules (or equivalent translations in lexc).
# * d. You must test your system on at least five word forms and include the output of the test in your answer.

pass # <write your solution here>

# ### Assignment 5.3: Regular expressions
#
# In this assignment, you will practice writing regular expressions in xfst.
# Please note that in this assignment multicharacters are not allowed.
# 
# 1. Write regular expressions that denote languages which would accept:
#
# * a. union of the words: cat, cats, cat's, and cats'.
# * b. anything but the set of words: {sing, sang, sung}.
# * c. subtraction of the sets: {cat, dog, rat, mouse, cow} and {mouse, rat}.
#
# Run each regular expression in xfst shell with `read regex` command. After each regular expression run command `print net`.
#
# Next you will write regular expressions that contain composition with replace rules.
#
# 2. Write an expression where an English verb vocabulary {sing, sit, ring, win} will be changed into past tense {sang, sat, rang, won}.

pass # <write your solution here>

# 3. Write an expression where a set of Finnish words {makkara, hattara, jäkälä, läsnä} will be composed with rules that change a into ä, and ä into a,
# so that we get set {mäkkärä, hättärä, jakala, lasna} as final output. If you want, you can use parallel replace rules
# to solve this although they haven't been thought in the lectures (check the book for that), but also other solutions are possible.

pass # <write your solution here>

# ### Assignment 5.4: Drawing automata and transducers with hfst
#
# 1. Draw union
# 
# * a. Start xfst shell and run following commands:
#
# ```
# read regex [ s i n g | s o n g | s i n g e r ] |  [ f l i n g | f i n g e r ] ;`
# view net
# ```
#
# After you have done that, exit with `exit`.
#
# 2. Following the same instructions, view images for regular expressions:
#
# * a. `{ready} .o. [ a |e | i |o | u ] -> %[ ... %]`
# * b. `(r e) [ [m a k e] | [c o m p i l e] ]`
