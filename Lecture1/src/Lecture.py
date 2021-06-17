# # COMPUTATIONAL MORPHOLOGY WITH HFST TOOLS - LECTURE 1
#
# <ul>
# <li>1. <a href="#1.-Prerequisites">Prerequisites</a></li>
# <li>2. <a href="#2.-Course-material">Course material</a></li>
# <li>3. <a href="#3.-Course-overview">Course overview</a></li>
# <li>4. <a href="#4.-Hockett's-models-of-morphology">Hockett's models of morphology</a></li>
# <li>5. <a href="#5.-Morphological-generators-and-analyzers">Morphological generators and analyzers</a></li>
# <li>6. <a href="#6.-A-Finite-State-Transducer-that-implements-a-morphological-generator">A Finite-State Transducer that implements a morphological generator</a></li>
# <li>7. <a href="#7.-Lexc-code-that-represents-this-transducer">Lexc code that represents this transducer</a></li>
# <li>8. <a href="#8.-Assignments">Assignments</a></li>
# </ul>
#
# ## HFST - Helsinki Finite-State Technology
#
# The HFST toolkit is intended for processing natural language
# morphologies. The toolkit is demonstrated by wide-coverage
# implementations of a number of languages of varying morphological
# complexity. HFST is written mainly in C++, but there is also a Python interface
# which is demonstrated on these notebooks.
#
# ## 1. Prerequisites
#
# <ul>
# <li>Foundations of general linguistics</li>
# <li>Basic knowledge on how to use a computer</li>
# <li>Some programming experience is desirable</li>
# <li>Knowledge of Natural Language Processing (NLP) is also a plus</li>
# </ul>
#
# ## 2. Course material
#
# If you want a book:
#
# <ul>
# <li>Kenneth R. Beesley and Lauri Karttunen: <a href="http://press.uchicago.edu/ucp/books/book/distributed/F/bo3613750.html">Finite State Morphology</a>, CSLI Publications, 2003</li>
# <li>Daniel Jurafsky and James H. Martin, Speech and Language Processing, Prentice Hall, second edition, 2009</li>
# </ul>
#
# Links:
#
# <ul>
# <li>HFST <a href="https://hfst.github.io">main page</a>.</li>
# <li>For installation of the HFST package for Python, see our <a href="https://pypi.org/project/hfst_dev/">PyPI pages</a>.</li>
# <li>For more information about the interface, see our <a href="https://github.com/hfst/python-hfst-4.0/wiki">Github wiki pages</a>.</li>
# </ul>
#
# First, import the package and list its contents with `help`.

import hfst_dev
help(hfst_dev)

# Then, see for more information on some of the functions, e.g. `compile_lexc_file`.

help(hfst_dev.compile_lexc_file)

# Also print the version number of the package.

print(hfst_dev.__version__)

# ## 3. Course overview
#
# This web course is based largely on the course <a href="https://courses.helsinki.fi/en/LDA-T3101/120259674">”Computational Morphology”</a> held at the University of Helsinki spring 2018.
# The course was taught and planned by Mathias Creutz. Senka Drobac also contributed to the exercises.
# The web course uses the same examples and exercises, but HFST command line tools have been replaced with HFST Python interface.
#
# <table>
# <tr> <th>Lecture</th> <th>Topics</th> </tr>
# <tr> <td>1</td> <td>Theories of morphology, generators and analyzers, lexc</td> </tr>
# <tr> <td>2</td> <td>Finite-state basics, xfst rules</td> </tr>
# <tr> <td>3</td> <td>Disambiguation, probabilities, finite-state networks summarized</td> </tr>
# <tr> <td>(4)</td> <td>(Machine learning)</td> </tr>
# <tr> <td>5</td> <td>Guessers, stemmers, regular expressions in xfst</td> </tr>
# <tr> <td>6</td> <td>Twolc, two-level rules</td> </tr>
# <tr> <td>7</td> <td>Flag diacritics, non-concatenative morphology</td> </tr>
# <tr> <td>8</td> <td>Optimization of finite-state networks</td> </tr>
# </table>

# ## 4. Hockett's models of morphology
#
# ### 4.1. Word and Paradigm (W&P), Example: Finnish nouns
#
# <table>
# <tr> <th>Numbers/Cases</th> <th>Singular</th> <th>Plural</th> </tr>
# <tr> <th>Nominative</th> <td>susi</td> <td>sudet</td> </tr>
# <tr> <th>Genitive</th> <td>suden</td> <td>susien, sutten</td> </tr>
# <tr> <th>Partitive</th> <td>sutta</td> <td>susia</td> </tr>
# <tr> <th>Inessive</th> <td>sudessa</td> <td>susissa</td> </tr>
# <tr> <th>Elative</th> <td>sudesta</td> <td>susista</td> </tr>
# <tr> <th>Illative</th> <td>suteen</td> <td>susiin</td> </tr>
# <tr> <th>Adessive</th> <td>sudella</td> <td>susilla</td> </tr>
# <tr> <th>Ablative</th> <td>sudelta</td> <td>susilta</td> </tr>
# <tr> <th>Allative</th> <td>sudelle</td> <td>susille</td> </tr>
# <tr> <th>Essive</th> <td>sutena</td> <td>susina</td> </tr>
# <tr> <th>Translative</th> <td>sudeksi</td> <td>susiksi</td> </tr>
# <tr> <th>Instructive</th> <td>-</td> <td>susin</td> </tr>
# <tr> <th>Abessive</th> <td>sudetta</td> <td>susitta</td> </tr>
# <tr> <th>Comitative</th> <td>-</td> <td>susine(en)</td> </tr>
# </table>

# ### 4.2. Item and Arrangement (I&A)
#
# #### Morphemes and allomorphs
#
# <ul>
#  <li>"SUSI": susi, sude-, sute-, sut-, sus-</li>
#  <li>Number:</li>
#   <ul>
#    <li>Singular: ∅ (or no morpheme at all: unmarked)</li>
#    <li>Plural: -t, -i-, -j-</li>
#   </ul>
#  <li>Case:</li>
#   <ul>
#     <li>Genitive: -n, -en, -den, -tten</li>
#     <li>Partitive: -a, -ä, -ta, -tä</li>
#     <li>Etc.</li>
#   </ul>
# </ul>
#
# #### The allomorphs occur in a specific distribution
#
# <ul>
#  <li>E.g., sus- in all plural forms except nominative.</li>
#  <li>No allomorph is more "basic" than any other.</li>
# </ul>
#
# ### 4.3. Item and Process (I&P)
#
# We have roots or bases of morphemes and different processes apply to them.
#
# <ul>
#  <li>Nominative: word final 'e' becomes 'i'; 't' in front of 'i' becomes 's' 🡒 "susi"</li>
#  <li>Genitive: add suffix '+n'; soften 't' to 'd' in closed syllable 🡒 "suden"</li>
#  <li>Etc.</li>
# </ul>
#
# ### 4.4. Corresponding HFST tools
#
# <table>
# <tr> <th>Model/Tool</th> <th><a href="https://github.com/hfst/python-hfst-4.0/wiki/PackageHfst#compile_twolc_file-inputfilename-outputfilename-kwargs">twolc</a></th> <th><a href="https://github.com/hfst/python-hfst-4.0/wiki/PackageHfst#compile_lexc_file-filename-kwargs">lexc</a></th> <th><a href="https://github.com/hfst/python-hfst-4.0/wiki/PackageHfst#compile_xfst_file-filename-kwargs">xfst</a></th> </tr>
# <tr> <th>Word & Paradigm</th> <td> </td> <td>✔</td> <td>✔</td> </tr>
# <tr> <th>Item & Arrangement</th> <td> </td> <td>✔</td> <td>✔</td> </tr>
# <tr> <th>Item & Process</th> <td>✔</td> <td> </td> <td>✔</td> </tr>
# </table>
#
# Check how they work with `help` command.
#
# #### twolc:

help(hfst_dev.compile_twolc_file)

# #### lexc:

help(hfst_dev.compile_lexc_file)

# #### xfst:

help(hfst_dev.compile_xfst_file)

# #### interactive version of xfst:

help(hfst_dev.start_xfst)

# We will get back to these tools in later sections.

# ## 5. Morphological generators and analyzers
#
# ### 5.1. Morphological generator
#
# * Input (also called lexical form): `cat+N+Sg+Poss`
# * Output (also called surface form): `cat's`
# * The idea is to create a model that generalizes to new word forms.
#   - Primitive way: List all possible pairs of input and output in the lexeme:
#     * `cat+N+Sg` 🡒 cat
#     * `cat+N+Pl` 🡒 cats
#     * `cat+N+Sg+Poss` 🡒 cat's
#     * `cat+N+Pl+Poss` 🡒 cats'
#   - More sophisticated way: Model the inner regular morphological structure of words.
#     * This makes it possible to add a new lemma, such as `dog`, and the model knows how to inflect this word by analogy to the word `cat`.
#
# ### 5.2. Morphological analyzer
#
# * Input (surface form): `cat's`
# * Output (lexical form): `cat+N+Sg+Poss`
# * An analyzer produces the opposite mapping compared to the generator:
#   - The input of the generator is the output of the analyzer.
#   - The output of the analyzer is the input of the generator.
# * An analyzer is very useful, for instance:
#   - when we want to parse natural language text syntactically
#   - when we want to <i>normalize</i> text, such that we only care about the base form (lemma) of every word in the text; this is used, for instance, in <i>information retrieval</i>.
#
# ### 5.3. Some simple noun paradigms in English
#
# #### Paradigm: N
#
# <table>
# <tr> <td><b>cat</b></td> <td>+Sg (singular)</td> </tr>
# <tr> <td><b>cat|s</b></td> <td>+Pl (plural)</td> </tr>
# <tr> <td><b>cat|'s</b></td> <td>+Sg +Poss (singular possessive)</td> </tr>
# <tr> <td><b>cat|s'</b></td> <td>+Pl +Poss (plural possessive)</td> </tr>
# </table>
#
# <i>Similarly:</i> dog, pet, book, hill, fan
#
# #### Paradigm: N_s

# (The understroke following the part-of-speech marker N with a subsequent mnemonic 's'
# is a transparent way of indicating allomorphic inflection types.)
#
# <table>
# <tr> <td><b>kiss</b></td> <td>+Sg (singular)</td> </tr>
# <tr> <td><b>kiss|es</b></td> <td>+Pl (plural)</td> </tr>
# <tr> <td><b>kiss|'s</b></td> <td>+Sg +Poss (singular possessive)</td> </tr>
# <tr> <td><b>kiss|es|'</b></td> <td>+Pl +Poss (plural possessive)</td> </tr>
# </table>
#
# <i>Similarly:</i> wish, mess, church, search, waitress
#
# Let's create a morphological generator and analyzer for this data.

# ## 6. A Finite-State Transducer that implements a morphological generator
#
# Below is a finite-state transducer (FST) for purely concatenative I&A English noun inflection
# for our simple example data.
# The yellow circles represent _states_ and the arrows represent _transitions_ between the states.
# The state named <i>Root</i> is the initial state and state named <i>#</i> the final one.
# Above each transition, there is the input
# that the transition <i>consumes</i> and the output that it <i>produces</i>, separated by a colon ":".
# The symbol ε stands for the <i>epsilon</i>, i.e. the empty symbol. On the input side it means that no symbol is consumed
# and on the output side that no symbol is produced.
# The "ε:ε" represents the <i>epsilon transition</i> which is possible without consuming
# any input or producing any output.
# We will return to finite-state transducers in more detail in the next part.
#
# <img src="img/noun_inflection.png">

# ## 7. Lexc code that represents this transducer
#
# ### 7.1 Define all symbols consisting of multiple characters
#
# ```
# Multichar_Symbols
#         +N      &#33; Noun tag
#         +Sg     &#33; Singular
#         +Pl     &#33; Plural
#         +Poss   &#33; Possessive form
#                 &#33; Another comment that is ignored by the compiler
# ```

# Anything between an exclamation mark and the end of a line
# is a comment. Comments are ignored by the lexc compiler.
# Use comments a lot!
# Your code will be clearer to yourself and to others.

# ### 7.2 Define the compulsory Root lexicon
#
# ```
# LEXICON Root
#         Nouns ; &#33; No input, no output
# ```
#
# This is equivalent to writing:
#
# ```
# LEXICON Root
# 0:0     Nouns ; &#33; Explicitly showing no input, no output
# ```
#
# This is further equivalent to writing:
#
# ```
# LEXICON Root
# 0       Nouns ; &#33; When the input and output are identical,
#                 &#33; you can type only the input side
# ```
#
# <img src="img/root_lexicon.png">

# ### 7.3 Define the Nouns lexicon
#
# ```
# &#33;
# &#33; NOUNS start here
# &#33;
#
# LEXICON Nouns
#
# &#99;at     N ;
# dog     N ;
#
# church  N_s ;
# kiss    N_s ;
#
# beauty:beaut    N_y ;
# sky:sk          N_y ; 
#
# ```
#
# <img src="img/nouns_lexicon.png">

# ### 7.4 Continuation lexicons for the N paradigm
#
# ```
# &#33; The noun lexica N and Num are used for stems without
# &#33; any alternation
# 
# LEXICON N
# +N:0    Num ;
# 
# LEXICON Num
# +Sg:0   PossWithS ;
# +Pl:s   PossWithoutS ;
# ```
#
# <img src="img/n_paradigm.png">

# ### 7.5 Continuation lexicons for the N_s paradigm
#
# ```
# &#33; The noun lexica N_s and Num_s are used for stems that
# &#33; end in a sibilant and need an extra inserted "e"
#
# LEXICON N_s
# +N:0    Num_s ;
#
# LEXICON Num_s
# +Sg:0   PossWithS ;
# +Pl:es  PossWithoutS ;
# ```
#
# <img src="img/ns_paradigm.png">

# ### 7.6 Continuation lexicons for the N_y paradigm
#
# ```
# &#33; The noun lexica N_y and Num_y are used for stems with
# &#33; "y" -> "ie" alternation
#
# LEXICON N_y
# +N:0    Num_y ;
#
# LEXICON Num_y
# +Sg:y   PossWithS ;
# +Pl:ies PossWithoutS ;
# ```
#
# <img src="img/ny_paradigm.png">

# ### 7.7 Continuation lexicons for possessive marker
#
# ```
# &#33; Possessive markers: usually the singular is 's and
# &#33; the plural is '
#
# LEXICON PossWithS
# +Poss:'s    # ; 
#             # ; &#33; No ending: no input/output
# 
# LEXICON PossWithoutS 
# +Poss:'     # ;
#             # ; &#33; No ending: no input/output
#
# END
# ```
# <img src="img/poss_ending.png">
#
# Note that `END` signifies the end of lexc file. It must be included at the end of each lexc file.

# ### 7.8. Compiling the lexc script into a transducer
#
# Finally, let's compile the lexc script into a transducer:

from hfst_dev import compile_lexc_script

generator = compile_lexc_script(
"""
Multichar_Symbols
        +N      ! Noun tag
        +Sg     ! Singular
        +Pl     ! Plural
        +Poss   ! Possessive form

LEXICON Root
        Nouns ; ! No input, no output

!
! NOUNS start here
!

LEXICON Nouns

cat     N ;
dog     N ;

church    N_s ;
kiss      N_s ;

beauty:beaut    N_y ;
sky:sk          N_y ;


! The noun lexica N and Num are used for stems without any alternation

LEXICON N
+N:0    Num ;

LEXICON Num
+Sg:0   PossWithS ;
+Pl:s   PossWithoutS ;

! The noun lexica N_s and Num_s are used for stems that end in a sibilant
! and need an extra inserted "e"

LEXICON N_s
+N:0    Num_s ;

LEXICON Num_s
+Sg:0   PossWithS ;
+Pl:es  PossWithoutS ;

! The noun lexica N_y and Num_y are used for stems with "y" -> "ie" alternation

LEXICON N_y
+N:0    Num_y ;

LEXICON Num_y
+Sg:y   PossWithS ;
+Pl:ies PossWithoutS ;

! Possessive markers: usually the singular is 's and the plural is '

LEXICON PossWithS
+Poss:'s     # ;
             # ; ! No ending: no input, no output

LEXICON PossWithoutS
+Poss:'      # ;
             # ; ! No ending: no input, no output

END
""", verbosity=2
)

# We could also write the script to a file and then call `compile_lexc_file`. Note that we set the keyword argument `verbosity` to `2`.
# Then we will get more information about the compilation process.
# You can test the above command also with `verbosity=1` and `verbosity=0` (or just leaving the argument out).
#
# Test the transducer:

print(generator.lookup('sky+N+Pl'))

# and expect the result `(('skies', 0.0),)`, i.e. <i>skies</i> with a zero _weight_. We will return to weights in later lectures.
#
# Next, <a href="https://github.com/hfst/python-hfst-4.0/wiki/HfstTransducer#invert-self">invert</a> the transducer to get an analyzer (i.e. swap the symbols of input and output side).
# After inversion, it is good to <a href="https://github.com/hfst/python-hfst-4.0/wiki/HfstTransducer#minimize-self">minimize</a>
# the transducer (i.e. reduce it to an equivalent transducer with the smallest number of states).

from hfst_dev import HfstTransducer
analyzer = HfstTransducer(generator) # create a copy
analyzer.invert()
analyzer.minimize()

print(analyzer.lookup('skies'))

# and expect the result `(('sky+N+Pl', 0.0),)`, i.e. "the noun <i>sky</i> in plural with a zero weight".
#
# Let's check that inverting the analyzer produces a transducer equivalent to the generator with HfstTransducer.compare:

analyzer.invert()
analyzer.minimize()
print(analyzer.compare(generator))


# ## 8. Assignments
#
#
# ### Assignment 1.1: Testing a morphological generator
#
# Compile the lexicon en_ia_morphology_template.lexc into an hfst transducer.
# (The file contains the same lexc code that was used in example 7.8.)

morph = hfst_dev.compile_lexc_file('en_ia_morphology_template.lexc', verbosity=2)

# Optimize the transducer for lookup:

morph.lookup_optimize()

# Then test it:

print(morph.lookup('sky+N+Pl', output='text'))

# ... and expect the result: 'skies'.
#
# Your system works!

# For the noun sky, type in all four possible analyses (= lexical forms = input forms), and collect the corresponding surface forms (= output forms) as given by function HfstTransducer.lookup.

pass # write your solution here

# ### Assignment 1.2: Testing a morphological analyzer
#
# Invert your transducer, such that input becomes output and vice versa.
# Note that a lookup-optimized transducer supports only a couple of functions, so you need to remove optimization with
# <a href="https://github.com/hfst/python-hfst-4.0/wiki/HfstTransducer#remove_optimization-self">HfstTransducer.remove_optimization</a> before calling e.g.
# <a href="https://github.com/hfst/python-hfst-4.0/wiki/HfstTransducer#invert-self">HfstTransducer.invert</a>.
#
# This transducer works as an analyzer that retrieves the lexical form of surface forms.
# Collect the analyses for the following surface forms: dog's, skies, churches', beauty, cat.

pass # write your solution here

# ### Assignment 1.3: Adding English nouns to the lexicon
#
# Add the following missing nouns to the lexc file en_ia_morphology_template.lexc:
# book, doggy, fan, hill, mess, pet, search, waitress, wish.
#
# Go to the browser tab where you chose this lecture (probably the tab on left side)
# and click the file en_ia_morphology_template.lexc. A new tab opens where you can edit
# the file. After you have added the missing nouns, remember to click File -> Save.
# (Tab charaters must be inserted by copying and pasting them.)
#
# Recompile the transducer using function compile_lexc_file.
# Collect the surface forms produced by HfstTransducer.lookup for the lexical forms:
# book+N+Sg, doggy+N+Pl, fan+N+Sg+Poss, mess+N+Pl, wish+N+Pl+Poss.

pass # write your solution here

# Invert the transducer again using HfstTransducer.invert.
# Collect the lexical forms produced by HfstTransducer.lookup for the surface forms: books, doggy, pets', waitresses, waitress's, search.

pass # write your solution here

# ### Assignment 1.4: Adding a new noun paradigm to the lexicon
#
# Add a new type of nouns to the lexc file, with a specific plural form: criterion - criteria, lexicon - lexica, phenomenon - phenomena.
#
# Recompile the transducer using compile_lexc_file. Collect the surface forms produced by HfstTransducer.lookup for the lexical forms: criterion+N+Pl, phenomenon+N+Sg+Poss, phenomenon+N+Pl+Poss.

pass # write your solution here

# For the word "lexicon", also allow the parallel regular plural form lexicon - lexicons. Recompile the transducer and collect the surface forms for the lexical forms:
# lexicon+N+Sg, lexicon+N+Pl, lexicon+N+Pl+Poss. Do you get duplicate surface forms for some lexical forms? If so, can you explain why?

pass # write your solution here

# Invert the transducer and collect the lexical forms for the surface forms: lexicons, lexica, criterion's, phenomenon.

pass # write your solution here

# ### Assignment 1.5: Adding English verb inflection to the lexicon
#
# Add verb inflection to your lexc file. Include the three paradigms from the table below and all the verbs listed:
# jump, look, talk, walk, bake, fake, like, pile, smile, crash, hiss, kiss, miss, search.
#
# <table>
# <tr> <th>Base form</th> <th>Third Person Singular Present</th> <th>Present Participle</th> <th>Past</th> </tr>
# <tr> <td>jump</td> <td>jumps</td> <td>jumping</td> <td>jumped</td> </tr>
# <tr> <td>bake</td> <td>bakes</td> <td>baking</td> <td>baked</td> </tr>
# <tr> <td>crash</td> <td>crashes</td> <td>crashing</td> <td>crashed</td> </tr>
# </table>
#
# Use the tags +V, +Inf,  +Pres3Sg, +Past, +Prog, and remember to declare them as multichar symbols at the top of your lexc file.
#
# You will need seven new lexicons; you can call them: Verbs, V, V_e, V_s, Tense, Tense_e, Tense_s. (This structure is analogous to the noun lexicons Nouns, N, N_s, N_y, Num, Num_s, Num_y.)
#
# When you recompile your transducer, you should be able to generate word forms, such as talk+V+Prog -> talking.

pass # write your solution here

# When you invert your transducer, you should be able to analyze word forms, such as missed -> miss+V+Past.
# Collect the analyses for the following surface forms: like, looked, smiling, crashing, searches.

pass # write your solution here
