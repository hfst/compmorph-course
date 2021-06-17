# # COMPUTATIONAL MORPHOLOGY WITH HFST TOOLS - LECTURE 3
#
# <ul>
#  <li>1. <a href="#1.-Disambiguation">Disambiguation</a></li>
#  <li>2. <a href="#2.-Probabilities,-basics">Probabilities, basics</a></li>
#  <li>3. <a href="#3.-Back-to-disambiguation">Back to disambiguation</a></li>
#  <li>4. <a href="#4.-Spelling-correction">Spelling correction</a></li>
#  <li>5. <a href="#5.-Logprobs">Logprobs</a></li>
#  <li>6. <a href="#6.-Summary-of-types-of-finite-state-automata-and-transducers">Summary of types of finite-state automata and transducers</a></li>
#  <li>7. <a href="#7.-Assignments">Assignments</a></li>
# </ul>
#
# ## 1. Disambiguation
#
# ### 1.1. Some Finnish noun examples:
#
# <ul>
#  <li>nainen</li>
#  <li>lautasilla</li>
#  <li>lautasilta</li>
#  <li>poikasilla</li>
#  <li>poikasilta</li>
# </ul>
#
# ### 1.2. The Finnish noun examples with analyses:
#
# <ul>
#  <li>nainen 🡒 nainen +N +Sg +Nom (“woman”)</li>
#  <li>lautasilla 🡒 lautanen +N +Pl +Ade (“on plates”)</li>
#  <li>lautasilta 🡒 lautanen +N +Pl +Abl (“from plates”)</li>
#  <li>poikasilla 🡒 poikanen +N +Pl +Ade (“with cubs”)</li>
#  <li>poikasilta 🡒 poikanen +N +Pl +Abl (“from cubs”)</li>
# </ul>
#
# ### 1.3. The Finnish noun examples with more analyses:
#
# <ul>
#  <li>nainen 🡒 naida +V +Pot +Pres +Sg1 (“it seems I’ll marry”)</li>
#  <li>lautasilla 🡒 lauta#silla +N +Sg +Nom (“board rayon”)</li>
#  <li>lautasilta:</li>
#  <ul>
#   <li> 🡒 lauta#silta +N +Sg +Nom (“board bridge”)</li>
#   <li> 🡒 lautas#ilta +N +Sg +Nom (“plate evening”)</li>
#  </ul>
#  <li>poikasilla 🡒 poika#silla +N +Sg +Nom (“boy rayon”)</li>
#  <li>poikasilta:</li>
#  <ul>
#   <li> 🡒 poika#silta +N +Sg +Nom (“boy bridge”)</li>
#   <li> 🡒 poikas#ilta +N +Sg +Nom (“cub evening”)</li>
#  </ul>
# </ul>
#
# ### 1.4. How disambiguate?
#
# <ul>
#  <li>We could disambiguate (= find one unambiguous analysis) by looking at the word in context.</li>
#  <li>If we don’t have any context, however, we may still have a sense of which analyses are more likely <i>a priori</i>.</li>
#  <li>A priori = in general, without further information.</li>
#  <li><i>A posteriori</i>, when we have more information, it may turn out that the most likely analysis a priori is not the correct one, but it is the best guess without more information.</li>
# </ul>
#
# #### A priori assumptions:
#
# <ul>
#  <li> "Nainen +N" is more common than "naida +V".</li>
#  <li> Singular (+Sg) is more common than Plural (+Pl).</li>
#  <li> Nominative (+Nom) is more common than the other cases.</li>
#  <li> Adessive (+Ade) is slightly more common than Ablative case (+Abl).</li>
#  <li> Single-stem words are more common than compound words.</li>
# </ul>
#
# #### Model with probabilities
#
# <img src="img/model_with_probabilities.png">

# ## 2. Probabilities, basics
#
# ### 2.1. What is probability?
#
# <ul>
# <li>Probability is the measure of the likelihood that an event will occur.</li>
# <li>Probability is quantified as a number between 0 and 1</li>
#  <ul>
#   <li>0 indicates impossibility</li>
#   <li>1 indicates certainty</li>
#  </ul>
# </ul>
#
# ### 2.2. Objective probability
#
# <ul>
# <li>The most popular version of objective probability is frequentist probability.</li>
# <li>Claims that the probability denotes the relative frequency of occurrence of an experiment's outcome.</li>
# <li>The experiment is repeated many times.</li>
# <li>This interpretation considers probability to be the relative frequency "in the long run" of outcomes.</li>
# <li>Typical examples:</li>
#  <ul>
#   <li>throwing dice (1, 2, 3, 4, 5, 6)</li>
#   <li>throwing a coin ("heads or tails")</li>
#  </ul>
# </ul>
#
# #### Discrete probability distribution of outcome from throwing an unbiased six-sided die
#
# <img src="img/one_six_sided_die.png">
#
# Probability of mutually exclusive events 🡒 ADD probabilities together
#
# <pre>
# P(S = 1 or S = 2) =
# P(S = 1) + P (S = 2) =
# 1/6 + 1/6 =
# 2/6 =
# 1/3
# </pre>
#
# Probability of all possible events combined 🡒 The sum must be 1!
#
# <pre>
# P(S = 1 or S = 2  or S = 3 or
#   S = 4  or S = 5  or S = 6) =
# P(S = 1) + P (S = 2) + P (S = 3) +
#   P(S = 4) + P (S = 5) + P (S = 6) =
# 1/6 + 1/6 + 1/6 + 1/6 + 1/6 + 1/6 =
# 6/6 =
# 1
# </pre>
#
# #### Discrete probability distribution of outcome from throwing two unbiased six-sided dice
#
# <img src="img/two_six_sided_dice.png">
#
# Probability of independent events that co-occur 🡒 MULTIPLY probabilities together
#
# <pre>
# P(Sblack = 1 and Swhite = 1) =
# P(Sblack = 1) * P(Swhite = 1) =
# 1/6 * 1/6 =
# 1/36
# </pre>
# 
# Probability of mutually exclusive events 🡒 Involves both addition and multiplication
#
# <pre>
# P((Sblack = 5 and Swhite = 6) or (Sblack = 6 and Swhite = 5)) =
# P(Sblack = 5) * P(Swhite = 6) + P(Sblack = 6) * P(Swhite = 5) =
# 1/6 * 1/6 + 1/6 * 1/6 =
# 1/36 + 1/ 36 =
# 2/36 =
# 1/18
# </pre>
#
# #### For comparison: A continuous probability distribution
#
# <img src="img/continuous_probability_distribution.png">
#
# <i>Image from Wikipedia.</i>
#
# * The variables are here real-valued ("floats") rather than discrete categories ("ints").
# * We get a smooth curve for the probability distribution, such as this Gaussian curve, the so-called normal distribution.
#
# ### 2.3. Subjective probability
#
# <ul>
# <li>The most popular version of subjective probability is Bayesian probability.</li>
# <li>Rather than relative frequency in a series of experiments, subjectivists think of probabilities as degrees of belief.</li>
# <li>"The price at which you would buy or sell a bet that pays 1 unit of utility (such as money) if an event occurs, and 0 if the event does not occur."</li>
# <li>Examples:</li>
#  <ul>
#   <li>Is there life on Mars?</li>
#   <li>Will Trump win a second term in the USA?</li>
#   <li>Will it snow in Helsinki tomorrow?</li>
#   <li>Given specific symptoms, does a patient have cancer?</li>
#  </ul>
# </ul>
#
# #### Prior and posterior probabilities
#
# <ul>
# <li>In Bayesian statistics, there are prior probabilities and posterior probabilities</li>
#  <ul>
#   <li>also called a priori and a posteriori probabilities</li>
#  </ul>
# <li>The prior probability states the general assumptions made in the model, such as:</li>
#  <ul>
#   <li><pre>P("It snows in Helsinki in January")</pre></li>
#  </ul>
# <li>The posterior probability is a product of two probabilities: the prior probability and a conditional probability, such as:</li>
#  <ul>
#   <li><pre>P("It snows in Helsinki on 23 Jan 2018" | "It snows in Helsinki in January") * P("It snows in Helsinki in January")</pre></li>
#  </ul>
# </ul>

# ## 3. Back to disambiguation
#
# ### 3.1. The "poikasilla" ambiguity: poikanen +N +Pl +Ade
#
# <img src="img/poikanen_n_pl_ade.png">
#
# Do the calculations
#
# <pre>
# Prob(poikanen +N +Pl +Ade)
# = Prob(+N) * Prob("poikanen") * Prob(+Pl) * Prob(+Ade)
# = 0.5 * 0.0001 * 0.3 * 0.05
# = 0.00000075
# = 7.5 * 10^-7
# </pre>
#
# ### 3.2. The "poikasilla" ambiguity: poika#silla +N +Sg +Nom
#
# <img src="img/poika_silla_n_sg_nom.png">
#
# Do the calculations:
#
# <pre>
# Prob(poika#silla +N +Sg +Nom)
# = Prob(+N) * Prob(“poika”) * Prob(Compound word) * Prob(“silla”) * Prob(+Sg) * Prob(+Nom)
# = 0.5 * 0.001 * 0.1 * 0.000001 * 0.6 * 0.55
# = 0.0000000000165
# = 1.65 * 10^-11
# </pre>
#
# ### 3.3. Formulate a model with probabilities
#
# Compare and pick the more likely alternative 🡒 The analysis <pre>poikanen +N +Pl +Ade</pre> is almost 50000 times more likely
# than <pre>poika#silla +N +Sg +Nom</pre> (in this invented model).
#
# Formulated in lexc format with weights (The syntax is correct, but don't do it exactly like this yet):
#
# <pre>
# Multichar_Symbols +N +Sg +Pl +Nom +Ade +Abl ^A ^I ^J ^K ^S ^T
# 
# LEXICON Root
# Nouns "weight: 0.5" ;
# Verbs "weight: 0.3" ;
# ...
# 
# LEXICON Nouns
# ilta:il^Ta          Number "weight: 0.0002" ;
# lauta:lau^Ta        Number "weight: 0.00001" ;
# lautanen:lauta^S    Number "weight: 0.0001" ;
# nainen:nai^S        Number "weight: 0.001" ;
# poika:po^J^Ka       Number "weight: 0.001" ;
# poikanen:poika^S    Number "weight: 0.0001" ;
# silla:silla         Number "weight: 0.000001" ;
# silta:sil^Ta        Number "weight: 0.0005" ;
# ...
# 
# LEXICON Number
# +Sg:0               Case "weight: 0.6" ;
# +Pl:^I              Case "weight: 0.3" ;
# &#35;:0  Nouns "weight: 0.1" ; &#33; Back to collect more stems
# 
# LEXICON Case
# +Nom:0              # "weight: 0.55" ;
# +Ade:ll^A           # "weight: 0.05" ;
# ...
# </pre>

# ## 4. Spelling correction
#
# ### 4.1. Virtual keyboard of a mobile device
#
# The D key was "pressed" (that is, touched).
#
# <img src="img/d_pressed.png">
#
# ### 4.2. Noisy virtual keyboard of a mobile device
#
# The D key was "pressed" (that is, touched), but the intended key was actually F!
#
# <img src="img/f_intended.png">
#
# Assume probabilities:
#
# <pre>
# P(p = F | i = F) = 0.7
# P(p = D | i = F) = 0.1
# P(p = G | i = F) = 0.1
# P(p = R | i = F) = 0.025
# P(p = T | i = F) = 0.025
# P(p = C | i = F) = 0.025
# P(p = X | i = F) = 0.0125
# P(p = V | i = F) = 0.0125
# </pre>
#
# For instance, read the last line as: "The Probability that V was
# pressed when actually F was the intended key  is 0.0125."
#
# Create an FST that generates "noise" (errors) and invert it to get a spell checker
#
# <img src="img/spell_checker_model.png">
#
# <pre>
# Noisy surface 1:  poikasilla   (no error)
# Noisy surface 2:  loikasilla   (substitution)
# Noisy surface 3:  poikaslla    (deletion)
# Noisy surface 4:  ppoikasilla  (insertion)
# Noisy surface 5:  opikasilla   (transposition)
# ... etc
# </pre>
#
# #### xfst script snippet for a spell checker
#
# <pre>
# &#33; Use the .l operator to project only lower level (= surface forms) of the
# &#33; transducer; we are not interested in the upper level (= lexical forms)
# define Vocabulary [ Lexicon .o. AlternationRules ].l ;
# 
# &#33; Add "noise" (spelling errors); replace rules are optional when in brackets ()
# define Substitution  [ f (->) d::0.1 ] .o. [ f (->) g::0.1 ] .o.
#                      [ f (->) r::0.025 ] .o. [ f (->) t::0.025 ] .o.
#                      etc ... ;
# 
# &#33; Define a transducer from correctly spelled words to words containing errors
# define NoisyVocabulary  Vocabulary .o. Substitution ;
# 
# &#33; Use the .i operator to invert the transducer, such that the input is noisy
# &#33; words and the output is correctly spelled words
# define SpellChecker  [ NoisyVocabulary ].i ;
# 
# &#33; The spell checker is ready to use
# regex SpellChecker ;
# 
# </pre>
#
# Again, the syntax is correct, but there is something left to fix with the weights...

# ## 5. Logprobs
#
# ### 5.1. Back to the probabilities
#
# We had the probability:
#
# <pre>
# Prob(poika#silla +N +Sg +Nom)
# = Prob(+N) * Prob("poika") * Prob(Compound word) * Prob("silla") * Prob(+Sg) * Prob(+Nom)
# = 0.5 * 0.001 * 0.1 * 0.000001 * 0.6 * 0.55
# = 0.0000000000165
# = 1.65 * 10^-11    
# </pre>
#
# This product of probabilities can also be written as addition of so called
# <i>negative logarithms</i>. Some mathematical background is needed to understand this transformation,
# i.e. concepts of <a href="https://en.wikipedia.org/wiki/Exponentiation">exponentiation</a> and
# <a href="https://en.wikipedia.org/wiki/Logarithm">logarithm</a>.
#
# #### 5.1.2 Logarithms
#
# With logarithms, the above probability can be expressed as:
#
# <pre>
# (5 * 10^-1) * 10^-3 * 10^-1 * 10^-6 * (6 * 10^-1) * (5.5 * 10^-1)
# = 10^-0.301 * 10^-3 * 10^-1 * 10^-6 * 10^-0.222 * 10^-0.260
# = 10^-(0.301 + 3 + 1 + 6 + 0.222 + 0.260) =
# = 10^-10.783
# = 0.0000000000165
# </pre>
#
# If we agree on some base, such as 10, then instead of multiplying actual probabilities
# of co-occuring independent events, we can add the (negative) exponents of the probabilities,
# which is faster and more manageable.
#
# Instead of <pre>0.5 * 0.001 * 0.1 * 0.000001 * 0.6 * 0.55 = 0.0000000000165</pre>,
# we get: <pre>0.301 + 3 + 1 + 6 + 0.222 + 0.260 = 10.783</pre>
#
# What we are doing is taking the negative logarithm of the probabilities:
# <pre>10^-10.783 = 0.0000000000165 🡒 -log10 0.0000000000165 = 10.783</pre>
#
# <ul>
# <li>A negative logarithm of a probability is called a <i>logprob</i>.</li>
# <li>A logprob can be seen as a penalty term or a cost: "if you do this operation you'll have to pay this much."</li>
# <li>Logprobs add up from operations performed in a sequence.</li>
# <li>If the probability of some operation is 1, that is, there is only one possible outcome:</li>
#  <ul>
#   <li>The logprob is <pre>-log10 1 = 0</pre></li>
#   <li>That is, there is no penalty if there is only one certain outcome.</li>
#   <li>This makes sense.</li>
#  </ul>
# </ul>
#
# ### 5.2. Weights in HFST
#
# <ul>
# <li>HFST does not really support probabilities as such.</li>
# <li>HFST supports additive weights, such as logprobs.</li>
# <li>Weights in lexc could look like:
# <pre>
# LEXICON Nouns
# ilta:il^Ta          Number "weight: 3.69897" ;
# lauta:lau^Ta        Number "weight: 5.00000" ;
# ...
# </pre></li>
# <li>Weights in xfst rules could look like:
# <pre>[ f (->) g::1.000 ] .o. [ f (->) r::1.602 ]</pre></li>
# </ul>
#
# ### 5.3. Lexc with weights revisited
#
# <img src="img/lexc_with_weights_revisited.png">

from hfst_dev import compile_lexc_script

tr = compile_lexc_script("""
Multichar_Symbols +N +Sg +Pl +Nom +Ade +Abl ^A ^I ^J ^K ^S ^T 

LEXICON Root
           Nouns "weight: 0.30103" ;   ! Probability: 0.5
           Verbs "weight: 0.52288" ;   ! Probability: 0.3

LEXICON Nouns
ilta:il^Ta          Number "weight: 3.69897" ; ! Probability: 0.0002
lauta:lau^Ta        Number "weight: 5.00000" ; ! Probability: 0.00001
lautanen:lauta^S    Number "weight: 4.00000" ; ! Probability: 0.0001
nainen:nai^S        Number "weight: 3.00000" ; ! Probability: 0.001
poika:po^J^Ka       Number "weight: 3.00000" ; ! Probability: 0.001
poikanen:poika^S    Number "weight: 4.00000" ; ! Probability: 0.0001
silla:silla         Number "weight: 6.00000" ; ! Probability: 0.000001
silta:sil^Ta        Number "weight: 3.30103" ; ! Probability: 0.0005

LEXICON Number
+Sg:0               Case "weight: 0.22185" ;  ! Probability: 0.6
+Pl:^I              Case "weight: 0.52288" ;  ! Probability: 0.3
#:0  Nouns "weight: 1.00000" ; ! Back to collect more stems
                                              ! Probability: 0.1
LEXICON Case
+Nom:0              # "weight: 0.259637" ;    ! Probability: 0.55
+Ade:ll^A           # "weight: 1.301030" ;    ! Probability: 0.05

END
""")

# Invert and test the transducer:

tr.invert()
tr.minimize()
print(tr.lookup('poika^S^Ill^A'))
print(tr.lookup('poika^Sil^Ta'))
print(tr.lookup('po^J^Kasil^Ta'))

# ### 5.4. Revisited xfst script for a spell checker
#
# <img src="img/xfst_with_weights_revisited.png">

from hfst_dev import compile_xfst_script
compile_xfst_script("""
! Toy example
define Lexicon {for}|{fight}|{right}|{tight}|{of}|{or} ;
define AlternationRules ?* ;

! Use the .l operator to project only lower level (= surface forms) of the 
! transducer; we are not interested in the upper level (= lexical forms)
define Vocabulary [ Lexicon .o. AlternationRules ].l ;

! Add "noise" (spelling errors); replace rules are optional when in brackets ()
define Substitution  [ f (->) d::1.000 ] .o. [ f (->) g::1.000 ] .o. 
                     [ f (->) r::1.602 ] .o. [ f (->) t::1.602 ] ; 
!                                                                .o. etc ... ;

! Define a transducer from correctly spelled words to words containing errors
define NoisyVocabulary  Vocabulary .o. Substitution ;

! Use the .i operator to invert the transducer, such that the input is noisy
! words and the output is correctly spelled words
define SpellChecker  [ NoisyVocabulary ].i ;

! The spell checker is ready to use
regex SpellChecker ;
invert net
minimize net
set print-weight ON

apply up right
echo --
apply up or
echo --
apply up for
""")

# ## 6. Summary of types of finite-state automata and transducers
#
# ### 6.1. Finite-state automaton (FSA)
#
# A finite-state automaton (FSA) - or finite automaton - is a network consisting of nodes,
# which represent states, and directed arcs connecting the states,
# which represent transitions between states.
# Every arc is labeled with a symbol that is consumed from input.
# State transitions can also take place without consuming any input;
# these transitions are called epsilon transitions.
#
# <img src="img/fsa.png">
#
# <code>HfstIterableTransducer</code> is a special class for generating transducers
# from scratch or iterating them state by state and transition by transition.
# It does not support most of the ordinary transducer functions.

from hfst_dev import HfstIterableTransducer, EPSILON

tr = HfstIterableTransducer()
tr.add_transition(0, 1, EPSILON, EPSILON, 0)
tr.add_transition(0, 2, EPSILON, EPSILON, 0)
tr.add_transition(1, 3, 'b', 'b', 0)
tr.add_transition(2, 1, EPSILON, EPSILON, 0)
tr.add_transition(2, 2, 'b', 'b', 0)
tr.add_transition(3, 3, 'b', 'b', 0)
tr.add_transition(3, 4, EPSILON, EPSILON, 0)
tr.add_transition(3, 4, 'c', 'c', 0)
tr.set_final_weight(4, 0)

# View the transducer.
tr.view()

# ### 6.2. Weighted finite-state automaton (WFSA)
#
# A weighted finite-state automaton (WFSA) is an FSA with weights on the arcs.
# Weights make it possible to find the best way “through" an automaton for the given input;
# you want to take the path with the lowest weight.
#
# <img src="img/wfsa.png">

tr = HfstIterableTransducer()
tr.add_transition(0, 1, 'a', 'a', 2.7002)
tr.add_transition(0, 2, 'b', 'b', 1.0)
tr.add_transition(1, 1, 'a', 'a', 1.0)
tr.add_transition(1, 2, 'b', 'b', 0)
tr.add_transition(2, 2, 'b', 'b', 0.59961)
tr.add_transition(2, 3, 'c', 'c', 0)
tr.set_final_weight(2, 0)
tr.set_final_weight(3, 1.0)
tr.view()

# Weighted automata can be used to decide between two alternatives.
# For example, you’re running a speech recognition system and the user says "I have to go."
# How do you know the user didn’t say, "I have two go"?
# First, you come up with a probability of words occurring next to each other
# (for example, <code>P("to go")</code> and <code>P("two go")</code>) - a language model.
# Then, you translate those probabilities into weights for your finite state machine.
# Then, when you’re deciding between "to" and "two," you pick the sentence with lower weight ("to").
#
# ### 6.3. Finite-state transducer (FST)
#
# A finite-state transducer (FST) is a finite automaton for which
# each transition has an input label and an output label.
#
# <img src="img/fst.png">
#
# It recognizes whether the two strings are valid correspondences (or translations)
# of each other.

tr = HfstIterableTransducer()
tr.add_transition(0, 1, 'a', 'a', 0)
tr.add_transition(1, 2, 'b', 'b', 0)
tr.add_transition(1, 3, 'a', 'a', 0)
tr.add_transition(2, 1, 'b', 'c', 0)
tr.add_transition(2, 3, 'a', 'a', 0)
tr.set_final_weight(3, 0)
tr.view()

# ### 6.4. Weighted finite-state transducer (WFST)
#
# A weighted finite-state transducer (WFST) is a finite automaton for which
# each transition has an input label, an output label, and a weight.
#
# <img src="img/wfst.png">
#
# The initial state is labeled 0. The final state is 2 with final weight of 3.5.
# Any state with non-infinite final weight is a final state. There is a transition
# from state 0 to 1 with input label "a", output label "x", and weight 0.5.
# This machine transduces, for instance, the string "ac" to "xz" with weight 6.5
# (the sum of the arc and final weights).

tr = HfstIterableTransducer()
tr.add_transition(0, 1, 'a', 'x', 0.5)
tr.add_transition(0, 1, 'b', 'y', 1.5)
tr.add_transition(1, 2, 'c', 'z', 2.5)
tr.set_final_weight(2, 3.5)
tr.view()

# Convert to HfstTransducer before lookup.
from hfst_dev import HfstTransducer
TR = HfstTransducer(tr)
print(TR.lookup('ac'))

# ## More information
#
# <ul>
#  <li>The Beesley & Karttunen book does not cover weighted finite-state machines. Weights were fairly new at about the time when the book was published in 2003.</li>
#  <li>HFST: <a href="https://github.com/hfst/python-hfst-4.0/wiki/Weights">Using weights</a></li>
#  <li>HFST: <a href="https://github.com/hfst/hfst-ospell/wiki">ospell</a> (currently available only as a separate command line tool)</li>
# </ul>

# ## 7. Assignments
#
# ### Assignment 3.1: Lexicon of Finnish compound words
#
# Your task is to create a lexc file that models compounding in Finnish.
# First create a stem lexicon thath contains the following 14 Finnish nouns:
# <tt>kissa, koira, melu, metsä, peli, päivä, pää, sähkö, talo, tie, tuoli, työ, väri, yö</tt>.
# Then make your lexicon produce compund words, such that <i>any</i> combination of <i>any number</i>
# of these nouns may be produced, for instance: <tt>kissa, kissakoira, päämelutalo, yösähköpeli, päätiepääpäivä</tt>.
#
# Start `hfst_dev.start_xfst()` and load your lexicon into xfst shell:
#
# ```
# hfst[0]: read lexc the_name_of_your_lexicon.lexc
# <hfst-xfst prints something here>
# hfst[1]: define Lexicon ;
# hfst[0]: regex Lexicon ;
# <hfst-xfst prints something here>
# ```
#
# Then have xfst print some random surface forms that your lexicon can produce.

pass # <insert your solution here>

# ### Assignment 3.2: Finnish vowel harmony
#
# In this task you should model Finnish vowel harmony with xfst rules.
# You need to solve Assignment 3.1 before solving this task.
#
# Below you see an incomplete lexc file, with some inflection lexicons included.
# Vowel harmony is here implemented using archiphonemes, written A and O, which will be realized
# as a or ä vs o or ö in surface forms. Not all inflected forms are implemented here, but that is ok.
# You don't have to add any missing case endings.
#
# What you need to do is:
#
# Incorporate your compound-word vocabulary from Assignment 3.1 into this file.
# Add the clitic -han/-hän as a last possible suffix, so that words like talossakinkohan can be modeled properly.
# Write rules for vowel harmony in an xfst script.
# Copy-paste the lexc code below into a text editor and make your own modifications:
#
# ```
# Multichar_Symbols
#         +Nom +Gen +Ade +Abl +All +Ine +Ela +Tra +Ess
#         +kin +kAAn +kO
#         &#33; TO DO: Add more multicharacter symbols as needed
#
# LEXICON Root
# &#33; TO DO: Add your compound-words lexicons here
#
# LEXICON Case
# +Nom:0          kinkAAn ;
# +Gen:n          kinkAAn ;
# +Ade:llA        kinkAAn ;
# +Abl:ltA        kinkAAn ;
# +All:lle        kinkAAn ;
# +Ine:ssA        kinkAAn ;
# +Ela:stA        kinkAAn ;
# +Tra:ksi        kinkAAn ;
# +Ess:nA         kinkAAn ;
#
# LEXICON kinkAAn
# +kin:kin        kO ;
# +kAAn:kAAn      kO ;
#                 kO ; &#33; continue without any suffix
#
# LEXICON kO
# +kO:kO          # ;
#                 # ; &#33; continue without any suffix
#
# &#33; TO DO: Add the -han/-hän lexicon somewhere
#
# END
# ```
#
# Besides the lexc file you will need an xfst file with your rules.
# If you need to refresh your memory on how to work with lexc combined with xfst, have a look at Lecture 2 or 3 or Assignment 2.1.
#
# Your rules should state the following:
#
# * The archiphoneme ‘A’ in a suffix (such as -ssA) should be realized as ‘a’ if it is preceded by a back vowel ‘a’, ‘o’ or ‘u’ anywhere in the word, such that there is no front vowel ‘ä’, ‘ö’ or ‘y’ anywhere between the back vowel and the suffix.
# * Otherwise the archiphoneme ‘A’ should be realized as ‘ä’.
# * Similarly, the archiphoneme ‘O’ in a suffix (such as -kO) should be realized as ‘o’ if it is preceded by a back vowel ‘a’, ‘o’ or ‘u’ anywhere in the word, such that there is no front vowel ‘ä’, ‘ö’ or ‘y’ anywhere between the back vowel and the suffix.
# * Otherwise the archiphoneme ‘O’ should be realized as ‘ö’.
#
# Some hints on xfst syntax:
#
# * `[a|b|c]` means one character a, b or c.
# * `$[a|b|c]` means any string of characters containing a, b or c.
# * `~$[a|b|c]` means any other string of characters than a string of characters containing a, b or c.
# * You can also define sets of characters as: `define MyAbc [a|b|c];` and use them in your expressions, for instance, `~$MyAbc`.
# * Contexts of rules can consist of multiple elements, e.g. `$[d|e|f] ~$[a|b|c] $[d|e|f] _ $[a|b|c] ~$[d|e|f]`.
#
# Compose your lexicon with your rules (as described in the earlier Assignment 2.1 mentioned above).

pass # <insert your solution here>

# Generate the following surface forms and verify that they are correct:
#
# * `down talo+Ine+kAAn+kO` (should be: talossakaanko)
# * `down metsäkissa+Gen+kin+hAn` (should be: metsäkissankinhan)
# * `down yö+Tra+kO` (should be: yöksikö)
# * `down päivätyö+Ess` (should be: päivätyönä)
# * `down tuolipeli+Ela+hAn` (should be: tuolipelistähän)
#
# Also output at least 20 random surface forms.
#
# At this point it is very likely that the surface form tuolipelistähän did not come out correctly.
# There are also some other word forms that may be incorrect. Can you explain why? Any idea how to solve the problem by modifying the lexc file and your rules slighty?

pass # <insert your solution here>

# ### Assignment 3.3: Adding weights to a lexicon
#
# In this task you shall build on your vocabulary of Finnish compound words from Assignment 3.2.
# If you did not manage to solve Assignment 3.2, you can use your result from Assignment 3.1 instead, but Assignment 3.2 is the preferred alternative.
#
# a. Modify your lexc file from Assignment 3.2 (or 3.1) in such a way that compound words "cost more" than single-stem words.
# That is, insert a weight each time you append a new stem to an existing stem.
# The weight does not have to be a proper logprob; it is sufficient for the weight to be a positive number,
# such that the more stems you add, the more "expensive" the generated word form becomes.
#
# b. Start the xfst shell with `hfst_dev.start_xfst()`.
# First run `set print-weight ON`.
# This makes the program show the weights of every word form it displays.
#
# c. Output some random lexical forms (upper level) and random surface forms (lower level) sorted by weight.
# The most probable ("cheapest") forms should be on the top and the least probable ("most expensive") words should be at the bottom of your list.
# The sorting happens automatically; you don't have to use any special command for that. Make sure the weights show, not just the word forms.

pass # <insert your solution here>

# ### Assignment 3.4: Creating a spell checker with xfst
#
# Create an xfst script that implements a spell checker for your Finnish compound-word vocabulary.
# Do it step by step as follows:
#
# a. First add one substitution rule that permits the substitution of the letter 'k' by the letter 'j' with some weight.
# Again, the weight does not have to be a logprob; some positive number is sufficient.
# Do not yet project your vocabulary transducer (using the .l operator), nor invert the final transducer (using the .i operator).
#
# b. Again, start the xfst shell and run `set print-weight ON`, so that the weights are displayed.
# (Two xfst shells cannot be run at the same time - exit any running shells with command "exit" first.)
# Generate all surface forms for the lexical string “kissa+Nom+kO”.
# The command “down kissa+Nom+kO” should produce four forms: “kissako”, “jissako”, “kissajo”, and “jissajo”.
#
# c. Next, project the vocabulary transducer to its lower level and invert the final transducer.
# Now, you should have a “proper” spell checker; for instance, when you type “down jissajo” the output should be the corrected form: “kissako”.
#
# d. Add more noise-introducing alternations with weights:
# you should have at least 5 different cases of each of the following types: substitutions, insertions, deletions and transpositions.
#
# e. Start the xfst shell and run `set print-weight ON`, and output some random upper (noisy) and lower (corrected) forms sorted by weight.
#
# f. Figure out what the correct spellings are for some of the weirdest noisy random words you produced in e).
# Depending on your model, you would type something like: down ähmöpäiialo (a misspelled variant of the funny word “sähköpääkissako”).
#
# g. Generate all possible erroneous spelling variants that your model can produce for “kissa”: up kissa

pass # <insert your solution here>
