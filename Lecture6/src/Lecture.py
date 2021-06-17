# # COMPUTATIONAL MORPHOLOGY WITH HFST TOOLS - LECTURE 6
#
# <ul>
#  <li>1. <a href="#1.-Two-level-rules">Two-level rules</a></li>
#  <li>2. <a href="#2.-Example:-English-adjectives">Example: English adjectives</a></li>
#  <li>3. <a href="#3.-Twol-rule-operators">Twol rule operators</a></li>
#  <li>4. <a href="#4.-Example:-consonant-gradation-in-Finnish">Example: consonant gradation in Finnish</a></li>
#  <li>5. <a href="#5.-Assignments"></a>Assignments</li>
# </ul>
#
# ## 1. Two-level rules
#
# ### 1.1. Xfst rules revisited
#
# Recall the finite-state transducer for I&P English noun inflection (from lecture 1):
#
# <img src="img/noun_inflection.png">
#
# ```
# Example input:    ∅sky+N+Pl+Poss
# Example output:   ∅sky^  s  '
# ```
# 
# Xfst rules are placed in a series.
# We compose our lexicon with our rewrite rules (called “replace rules” in xfst)
# and  produce one single FST that “jumps” from the lexical-form input straight to
# the final output in one go, without producing the intermediate steps.
#
# <i>Figures taken from an unpublished chapter "Two-Level Rule Compiler" of Beesley & Karttunen: Finite State Morphology, CSLI Publications, 2003.</i>
#
# <img src="img/cascade.png">
#
# ```
# Example input:  sky+N+Pl+Poss
# Lexicon output: sky^s'
# Rule 1 output:  sky^es
# Rule 2 output:  ski^es
# Rule 3 output:  skies
# ```
#
# The single FST will directly give: sky+N+Pl+Poss 🡒 skies.
# 
# The order of the rules matters!
#
# ### 1.2. Two-level approach
#
# #### Two-level morphology is different
#
# <img src="img/series.png">
#
# <ul>
#  <li>The order of the rules does not matter</li>
#  <li>The rule transducers are combined by intersection rather than composition</li>
# </ul>
#
# #### Compare rule declarations for xfst vs. twol:
#
# <img src="img/rule_declarations_compared.png">
#
# #### Some of the twol notation explained:
#
# <img src="img/twol_notation_explained.png">

# ## 2. Example: English adjectives
#
# ### 2.1. The lexicon
#
# Recall the lexicon (lexc) of some English adjectives from lecture 2:
#
# ```
# Multichar_Symbols
# +A       ! Adjective tag
# +Pos     ! Positive
# +Cmp     ! Comparative
# +Sup     ! Superlative
#
# LEXICON Root
# Adjectives ;
#
# LEXICON Adjectives
# big     A ;
# cool    A ;
# crazy   A ;
# great   A ;
# grim    A ;
# happy   A ;
# hot     A ;
# long    A ;
# quick   A ;
# sad     A ;
# short   A ;
# slow    A ;
# small   A ;
# warm    A ;
#
# LEXICON A
# +A:^    Comparison ;
#
# LEXICON Comparison
# +Pos:0  # ;
# +Cmp:er # ;
# +Sup:est  # ;
#
# END
# ```
#
# ### 1.2. xfst vs. twolc
#
# Also recall the corrected script (xfst) from Lecture 2 that is shown below with an equivalent script implemented with twolc:
#
# <img src="img/xfst_and_twolc_scripts.png">
#
# Which one to use is mostly a matter of taste. The xfst syntax allows lexicon to be read from file
# and composed with the rules. In twolc, this must be done by hand. Compare the following:

from hfst_dev import compile_xfst_file, compile_twolc_file, compile_lexc_file
from hfst_dev import intersect, compose, HfstTransducer

# The xfst script reads en_ip_adjectives_lexicon.lexc, composes it
# with the xfst rules, and stores the result to en_adjectives.xfst.hfst.
compile_xfst_file('en_adjectives.xfst')
xfst = HfstTransducer.read_from_file('en_adjectives.xfst.hfst')
print(xfst.lookup('big+A+Pos'))

# Explicitely compile the lexicon.
lexicon = compile_lexc_file('en_adjectives.lexc')
# Compile the twolc file
twolc_rules = compile_twolc_file('en_adjectives.twolc')
# intersect the rules (not compose!),
twolc_rule = intersect(twolc_rules)
# and the lexicon with them.
twolc = compose((lexicon, twolc_rule))
print(twolc.lookup('big+A+Pos'))

# The results should be the same.
assert(twolc.compare(xfst))

# ## 3. Twol rule operators
#
# <i>Figures taken from an unpublished chapter "Two-Level Rule Compiler" of Beesley & Karttunen: Finite State Morphology, CSLI Publications, 2003."</i>
#
# ### 3.1. twolc rule operators
#
# <img src="img/twolc_rule_operators.png">
#
# ### 3.2. Examples of twolc operators in context
#
# <img src="img/twolc_rule_operator_examples.png">
#
# ### 3.3. Resolving conflicting rules
#
# <img src="img/resolving_conflicting_rules.png">

twolc_rules = compile_twolc_file('conflicting_rules.twolc')
twolc = intersect(twolc_rules)
print(twolc.lookup('rar'))
print(twolc.lookup('lar'))

# Expect the result:
# ```
# rar: (('rbr', 0.0),)
# lar: (('lcr', 0.0),)
# ```

# ## 4. Example: consonant gradation in Finnish
#
# <i>Examples taken from an unpublished chapter "Two-Level Rule Compiler" of Beesley & Karttunen: Finite State Morphology, CSLI Publications, 2003..</i>
#
# ### 4.1. Consonant gradation in Finnish
#
# <img src="img/consonant_gradation_in_finnish.png"> 
#
# ### 4.2. Two-level grammar for consonant gradation
#
# <img src="img/consonant_gradation_twolc.png">
#
# ## More information
#
# <ul>
#  <li>Unpublished chapter of Beesley & Karttunen (2003): <a href="http://web.stanford.edu/~laurik/.book2software/twolc.pdf">“Two-Level Rule Compiler”</a></li>
#  <li>Karttunen & Beesley (1992): Two-Level Rule Compiler. Technical Report. ISTL-92-2. Xerox Palo Alto Research Center, California.</li>
#  <li><a href="https://github.com/hfst/hfst/wiki/HfstTwolc">hfst-twolc</a> command line tool</li>
# </ul>
#

# ## 5. Assignments
#
# ### Assignment 6.1: Test twolc
#
# In this task, you will test how two-level rules, so-called twol rules, work.
#
# First, compile the lexicon and twol rules.
# They are the same that were presented in section 1.2 of this lecture.

# Compile the twolc file
lexicon = compile_lexc_file('en_adjectives.lexc')
# Compile the twolc file
twolc_rules = compile_twolc_file('en_adjectives.twolc')
# intersect the rules (not compose!),
twolc_rule = intersect(twolc_rules)
# and the lexicon with them.
twolc = compose((lexicon, twolc_rule))
print(twolc.lookup('big+A+Pos'))

# Write the transducer to file.
twolc.write_to_file('en_adjectives_generator.hfst')

# Then, invert the transducer to get an analyzer

twolc.invert()
twolc.minimize()
print(twolc.lookup('craziest'))

# Finally, test the xfst shell.
# When you see the prompt <tt>hfst[0]</tt>, load the twol transducer as follows:
# `load stack en_adjectives_generator.hfst`
# Then collect some random surface forms by typing random-lower a couple of times.

from hfst_dev import start_xfst
start_xfst()

# ### Assignment 6.2: English adjectives using twolc
#
# If you have done Assignment 2.1, you will need the file en_ip_adjectives_lexicon.lexc with your modifications.
#
# If you have not done Assignment 2.1, you need to add four new adjectives to the Adjectives lexicon in the file en_ip_adjectives_lexicon.lexc: cute, nice, safe, wise.
#
# Next, modify the twol rules in the file en_adjectives.twolc to produce the correct inflections for the new adjectives “cute”, “nice”, “safe”, and “wise”.
# Remember to update the alphabet section at the top of the twol file as well.
#
# Rebuild the FST as described in Assignment 6.1.
#
# Test the FST using xfst shell as described in Assignment 6.1.
#
# Collect all surface forms using the command lower-words. Verify that all forms are correct.
#
# See <a href="https://github.com/hfst/hfst/wiki/HfstLexcAndTwolcTutorial">lexc and twolc tutorial</a> and also instructions of <a href="https://github.com/hfst/hfst/wiki/HfstTwolc">hfst-twolc command line tool</a>.

pass # <write your solution here>

# ### Assignment 6.3: Consonant gradation for Finnish nouns with lexc and twolc
#
# In this assignment you will work on Finnish consonant gradation. You have the following files: fin_cons_grad.lexc and fin_cons_grad.twolc.
#
# In Assignment 6.1, there are detailed instruction how to build a transducer out of these files.
# You just need to replace the file names.
# The model file that you produce and should load into xfst shell using the load stack command will be called fin_cons_grad_generator.hfst (rather than en_adjectives_generator.hfst).
#
# Start the task by verifying that you can load the existing model into xfst shell and run `upper-words` and `lower-words`.

pass # <write your solution here>

# Next, your task is to extend the vocabulary in the lexc file. You don't need to modify any other file. Don't change the two-level rules.
#
# Add at least ten new Finnish nouns to the lexicon.
#
# * The nouns should have different morpho-phonological structure, such that you demonstrate the different consonant gradation patterns through these nouns.
# * At least five of the new nouns should contain front-vowels (ä, ö, y, e, i) and take the ending -ä in partitive singular. Currently, there are no such nouns in the lexicon file.
# * If you don't know Finnish, you are allowed to invent your own nonsense words, as long as they behave as Finnish words with consonant gradation.
# * After you have added your words, recompile your model. Load it into xfst shell and run `upper-words` and `lower-words`.

pass # <write your solution here>

# PS: Vowel harmony can be implemented using two-level rules as well,
# but in this assignment we create two different inflection paradigms in the lexc file:
# stems with back vowels, on the one hand, and stems with front vowels, on the other hand.
