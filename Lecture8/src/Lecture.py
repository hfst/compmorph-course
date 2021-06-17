# # COMPUTATIONAL MORPHOLOGY WITH HFST TOOLS - LECTURE 8
#
# <ul>
#  <li>1. <a href="#1.-Optimizing-unweighted-finite-state-networks">Optimizing unweighted finite-state networks</a></li>
#  <li>2. <a href="#2.-Optimizing-weighted-finite-state-networks">Optimizing weighted finite-state networks</a></li>
# </ul>
#
# In this lecture we show how finite-state networks can be optimized,
# i.e. how the number of states and transitions can be made smaller.
# The networks that we use as examples will be created from scratch.
# So this lecture also shows how networks can be constructed state by state
# and transition by transition as opposed to more high-level ways such as
# regular expressions or lexc formalism.
#
# ## 1. Optimizing unweighted finite-state networks
#
# ### 1.1. Example lexicon
#
# Let’s first create a noun lexicon from scratch and add word stems to it.
# We use <code>HfstIterableTransducer</code> for this purpose.
#
# <img src="img/noun_lexicon.png">

from hfst_dev import HfstIterableTransducer, EPSILON
# This will be the entire lexicon. The constructor creates a network
# with one state, numbered as zero, which is an initial state.
lexicon = HfstIterableTransducer()
add_transition = lexicon.add_transition
add_state = lexicon.add_state

# Define a function for adding a path between states state1 and state2:
def add_path(path, state1, state2):
    # This is done mainly to get the number for a new state.
    # States don't need to be explicitly added, because 'add_transition'
    # creates the start and target states of a given transition if they
    # don't already exist.
    state = add_state()
    # Make sure state1 and state2 are skipped
    if state == state1 or state == state2:
        state += 1
    if state == state1 or state == state2:
        state += 1
    add_transition(state1, state, EPSILON, EPSILON, 0.0) # from start state to beginning of path
    for symbol in list(path):
        add_transition(state, state+1, symbol, symbol, 0.0)
        state += 1
    add_transition(state, state2, EPSILON, EPSILON, 0.0) # from end of path to end state

# Control sublexicon start and end state numbering
start_state = 1
end_state = 8
    
# Add the lexemes
for lexeme in ('kisko', 'kissa','koira','kori','koulu','taulu','tori','tuoksu'):
    add_path(lexeme, start_state, end_state)

# Test that the result is as intended:
test_lexicon = HfstIterableTransducer(lexicon)
test_lexicon.add_transition(0, 1, EPSILON, EPSILON, 0.0)
test_lexicon.set_final_weight(8, 0.0)
from hfst_dev import HfstTransducer, regex
tr = HfstTransducer(test_lexicon)
tr.minimize()

result = regex('{kisko}|{kissa}|{koira}|{kori}|{koulu}|{taulu}|{tori}|{tuoksu}')
assert(result.compare(tr))

# Then let’s create a continuation lexicon with case endings and start populating it.
#
# <img src="img/continuation_lexicon.png">

start_state = add_state()
assert(start_state == 50)
end_state = 53

# Add case endings
for ending in ('a','lla','lle','lta','n'):
    add_path(ending, start_state, end_state)
# make case ending optional
add_transition(start_state, end_state, EPSILON, EPSILON, 0.0)

# Then we tie the lexicons together and also add an epsilon transition from the end of the stem lexicon to its beginning in order to allow compound words
# In many languages, this will mean: an epsilon transition from the end of the case ending lexicon at Sg.Nom/absolute.
#
# <img src="img/compound_lexicon.png"> 

add_transition(8, start_state, EPSILON, EPSILON, 0.0)
add_transition(8, 1, EPSILON, EPSILON, 0.0)

# test that the result is as intended
test_lexicon = HfstIterableTransducer(lexicon)
test_lexicon.add_transition(0, 1, EPSILON, EPSILON, 0.0)
test_lexicon.set_final_weight(end_state, 0.0)

tr = HfstTransducer(test_lexicon)
tr.minimize()
result = regex('[{kisko}|{kissa}|{koira}|{kori}|{koulu}|{taulu}|{tori}|{tuoksu}]+ ({a}|{lla}|{lle}|{lta}|{n})')
assert(result.compare(tr))

# Next let’s add a lexicon for verb stems.
#
# <img src="img/lexicon_verb_stems.png">

start_state = add_state()
assert(start_state == 68)
end_state = 75

# Add verb stem endings
for stem in ('kisko','tuoksu'):
    add_path(stem, start_state, end_state)

# ... and a continuation lexicon for present-tense person endings (mainly)
#
# <img src="img/lexicon_person_endings.png">

start_state = add_state()
assert(start_state == 83)
end_state = 86

# Add person endings
for ending in ('a','mme','n','t','tte','vat'):
    add_path(ending, start_state, end_state)

# make person ending optional
add_transition(start_state, end_state, EPSILON, EPSILON, 0.0)

# Let’s tie the verb stem lexicon together with the endings lexicon.
#
# <img src="img/lexicon_verbs_and_endings.png">

add_transition(75, 83, EPSILON, EPSILON, 0.0)

# ... and let’s tie the whole network together with a start state and end state
#
# <img src="img/lexicon_tied_together.png">

add_transition(0, 1, EPSILON, EPSILON, 0.0)
add_transition(0, 68, EPSILON, EPSILON, 0.0)
add_transition(53, 103, EPSILON, EPSILON, 0.0)
add_transition(86, 103, EPSILON, EPSILON, 0.0)
lexicon.set_final_weight(103, 0.0)

# test that the result is as intended
tr = HfstTransducer(lexicon)
tr.minimize()
result = regex("""
[ [{kisko}|{kissa}|{koira}|{kori}|{koulu}|{taulu}|{tori}|{tuoksu}]+ ({a}|{lla}|{lle}|{lta}|{n}) ]
| 
[ [{kisko}|{tuoksu}] ({a}|{mme}|{n}|{t}|{tte}|{vat}) ]
""")
assert(result.compare(tr))

# ### 1.2. The resulting network
#
# The network is now ready. It has some advantages
#
# <ul>
#  <li>The structure is logical</li>
#  <li>Building the network by adding words and endings to it (through the union operation) is simple and fast</li>
# </ul>
#
# However, there are also some disadvantages
#
# <ul>
# <li>The automaton is non-deterministic and contains epsilon transitions</li>
#  <ul>
#   <li>This means that from a specific state, some symbol s can take you to more than one other state.</li>
#   <li>For instance, from the initial state 0, the symbol “k” could take you to state 3, 10, 16, 22, 27, or 70.</li>
#   <li>Imagine a scenario with a more realistic, larger vocabulary: using the network would be very slow, because of all the paths that have to be investigated.</li>
#  </ul>
# </ul>
#
# <img src="img/lexicon_epsilon_transitions.png">
#
# ### 1.3. Determinization of the network
#
# To start determinizing the network...
#
# <ul>
#  <li>1. We would merge the states 3, 10, 16, 22, 27, and 70 into one single, new state.</li>
#  <li>2. We would create one transition with the symbol “k” from the initial state to our new state. (Not shown in the picture on the next page.)</li>
# </ul>
#
# <img src="img/determinizing_the_network_1.png">
#
# <ul>
#  <li>3. Then, from the new state, the symbol “o” takes us to the states 17, 23 or 28, so we would merge these states into one new state, too.</li>
# </ul>
#
# <img src="img/determinizing_the_network_2.png">
#
# <ul>
#  <li>4. And the symbol “i” takes us to the states 4, 11, and 71, so we keep merging states and updating the transitions.</li>
# </ul>
#
# <img src="img/determinizing_the_network_3.png">

tr = HfstTransducer(lexicon)
tr.determinize()

# ### 1.4. Minimization of the network
#
# Furthermore, there is another disadvantage with the original network
#
# <ul>
# <li>The network is unnecessarily large</li>
#  <ul>
#   <li>There are some “tails” that occur in many places that could be merged.</li>
#   <li>For instance, the ends of the stems “kori” and “tori” are identical, as are the ends of the stems “koulu” and “taulu”.</li>
#   <li>Determinization will not fix these issues, so we can use a separate minimization algorithm.</li>
#  </ul>
# </ul>
#
# <img src="img/minimizing_the_network_1.png">
#
# <img src="img/minimizing_the_network_2.png">

tr = HfstTransducer(lexicon)
tr.minimize()

# ### 1.5. Further issues
#
# <ul>
# <li>The epsilon transition back to the beginning that produces compound words is nasty:</li>
#  <ul>
#   <li>Full determinization may actually bloat the size of the network.</li>
#   <li>Consider, for instance, if we had the stem “koulu”, which can take an “a” appended for partitive (“koulua”), but in addition, “a” could be the beginning of a second stem, such as “aamiainen” (“kouluaamiainen”).</li>
#   <li>Then, we would need one node in the network that is the starting point for all stems starting in “a” as the first stem in a word and another node with all the stems starting in “a” plus the endings starting in “a”.</li>
#  </ul>
# </ul>
#
# <img src="img/full_determinization.png">
#
# <ul>
#  <li>One might actually choose not to do a full determinization, but keep the epsilon transitions, for instance.</li>
# </ul>
#
# #### Acceptors vs. transducers?
#
# <ul>
# <li>In the examples above, we have shown acceptors, with only an input symbol on the arcs</li>
#  <ul>
#   <li>Such as: <code>a b c d</code></li>
#  </ul>
# <li>If we had a transducer, we would have pairs of symbols (<code>input:output</code>)</li>
#  <ul>
#   <li>Such as: <code>a:a a:b b:b c:e</code></li>
#  </ul>
# <li>Determinization and minimization work the same in both cases.</li>
#  <ul>
#   <li>We just need to interpret the pairs of symbols as one single symbol, so <code>a:a</code> is a different symbol from <code>a:b</code>.</li>
#  </ul>
# </ul>
#
# #### Algorithms explained
#
# For instance, at www.tutorialspoint.com:
#
# <ul>
# <li><a href="https://www.tutorialspoint.com/automata_theory/ndfa_to_dfa_conversion.htm">determinization</a></li>
# <li><a href="https://www.tutorialspoint.com/automata_theory/dfa_minimization.htm">minimization</a></li>
# </ul>

# ## 2. Optimizing weighted finite-state networks
#
# Optimizing weighted finite-state networks is basically the same as unweighted networks, but the weights may mess things up.
# We would like the optimized weighted network to produce the same weights as the unoptimized network.
#
# Assume the following probabilities:
#
# ```
# Prob(Noun) = 0.5
# Prob(Verb) = 0.3
# Prob(tuoksu | Noun) = 0.0001
# Prob(Noun ending -a for partitive case) = 0.1
# Prob(tuoksu | Verb) = 0.001
# Prob(Verb ending -a for infinitive) = 0.05
# ```
#
# Then we get the following probabilities for the full word forms “tuoksua”:
#
# <ul>
#  <li><code>Prob(tuoksua as a noun) = Prob(Noun) × Prob(tuoksu | Noun) × Prob(Noun ending -a for partitive case) = 0.5 × 0.0001 × 0.1 = 0.000005</code></li>
#  <li><code>Prob(tuoksua as a verb) = Prob(Verb) × Prob(tuoksu | Verb) × Prob(Verb ending -a for infinitive) = 0.3 × 0.001 × 0.05 = 0.000015</code></li>
#  <li><code>Prob(tuoksua as a noun or verb) = Prob(tuoksua as a noun) + Prob(tuoksua as a verb) =  0.000005 + 0.000015 = 0.00002</code></li>
# </ul>
#
# Shown as a network with probability weights:
#
# <img src="img/network_with_probability_weights.png">
#
# However, usually weights are not probabilities as such.
#
# ### 2.1. Semirings
#
# <ul>
# <li>Let’s replace the probabilities with some generic weights and replace the operators × and + with the generic semiring operators ⊗ and ⊕</li>
#  <ul>
#   <li><code>Weight(tuoksua as a noun) = Weight(Noun) ⊗ Weight(tuoksu | Noun) ⊗ Weight(Noun ending -a for partitive case)</code></li>
#   <li><code>Weight(tuoksua as a verb) = Weight(Verb) ⊗ Weight(tuoksu | Verb) ⊗ Weight(Verb ending -a for infinitive)</code></li>
#   <li><code>Weight(tuoksua as a noun or verb) = Weight(tuoksua as a noun) ⊕ Weight(tuoksua as a verb)</code></li>
#  </ul>
# </ul>
#
# ### 2.2. Probability semiring
#
# <ul>
#  <li>The weights should be interpreted as probabilties</li>
#  <li>The operator ⊗ should be interpreted as multiplication ×</li>
#  <li>The operator ⊕ should be interpreted as addition +</li>
#  <li>This is exactly what we have seen in our example already</li>
# </ul>
#
# ### 2.3. Log semiring
#
# <ul>
#  <li>The weights should be interpreted as negative logprobs: for instance, – log Prob(tuoksu | Noun)</li>
#  <li>The operator ⊗ should be interpreted as addition +</li>
#  <li>The operator ⊕ should be interpreted as the rather complex operation: w1 ⊕ w2 = – log (10<sup>-w1</sup> + 10<sup>-w2</sup>)  (if we use 10 as our base; it can be something else, too)</li>
#  <li>Why? Because if w1 = – log<sub>10</sub> p1 and w2 = – log<sub>10</sub> p2 and p1 and p2 are probabilities, then w1 ⊕ w2 = – log<sub>10</sub>(10<sup>– log<sub>10</sub> p1</sup> + 10<sup>– log<sub>10</sub> p2</sup>) =  – log<sub>10</sub>(p1 + p2) (This is the logprob of the sum of two probabilities)</li>
# </ul>
#
# Shown as a network with logprob weights in the log semiring
#
# <img src="img/network_with_logprob_weights.png">
#
# ### 2.4. Tropical semiring
#
# <ul>
#  <li>The weights can still be interpreted as negative logprobs: for instance, –log(Prob(tuoksu | Noun))</li>
#  <li>The operator ⊗ should still be interpreted as addition +</li>
#  <li>The operator ⊕ is simplified and picks the minimum, that is, the path with lower overall weight: w1 ⊕ w2 = min(w1, w2) = { w1 if w1 < w2; w2 otherwise }</li>
# </ul>
#
# Shown as a network with logprob weights in the tropical semiring:
#
# <img src="img/network_with_tropical_weights.png">
#
# #### Another example of weighted determinization in the tropical semiring
#
# <img src="img/weighted_determinization_example.png">

# Create the network from ATT format:
from hfst_dev import read_att_string
tr = read_att_string(
"""0 1 a a 0
0 1 b b 1
0 1 c c 4
0 2 a a 3
0 2 b b 4
0 2 c c 7
0 2 d d 0
0 2 e e 1
1 3 f f 1
1 3 e e 0
1 3 e e 2
2 3 e e 10
2 3 f f 11
2 3 f f 13
3 0
""")
tr.view()

tr.determinize()
tr.view()

# Weights must be pushed before minimization can take place:
#
# <img src="img/weight_pushing_and_minimization.png">

tr.minimize()
tr.view()

# #### Other uses
#
# Mehryar Mohri did not work on morphology, but on automatic speech recognition:
#
# <img src="img/speech_recognition.png">
#
# ## Further reading
#
# <ul>
#  <li>To learn more, you can read the <a href="http://www.cs.nyu.edu/~mohri/pub/csl01.pdf">full article</a> by Mohri et al.</li>
#  <li>There are more similar articles, such as the version that was actually published in Computer Speech and Language in 2002.</li>
#  <li>Or look at the <a href="http://www.openfst.org">OpenFST library</a></li>
# </ul>
