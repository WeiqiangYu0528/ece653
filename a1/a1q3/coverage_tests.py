import unittest

from . import token_with_escape 


class CoverageTests(unittest.TestCase):
    def test_1(self):
        """Node Coverage but not Edge Coverage"""
        # This is impossible to achieve in this question. Detailed can be found in the a1 sub.pdf
        pass

    def test_2(self):
        """Edge Coverage but not Edge Pair Coverage"""
        # YOUR CODE HERE
        # TR = {[8,11],[11,12],[11,23],[12,13],[12,20],[13,14],[13,15],[14,11],[15,16],[15,19],[16,11],[19,11],[20,21],[20,11],[21,11]}
        # the following Edge Pair is not covered by this test set: [8， 11， 23].
        # The edge [20, 11] is excluded because the program only has two states, state 0 and state 1.
        input = "a^|b"
        token_with_escape(input, escape="^", separator="|")

    def test_3(self):
        """Edge Pair Coverage but not Prime Path Coverage"""
        # YOUR CODE HERE
        # the following prime path is not covered by this test set: [16, 11, 12, 13, 15, 16].
        # The edge pairs [12,20,11],[20,11,23],[20,11,12] are excluded because the edge [20, 11] is infeasible.

        # TR = {[8, 11, 23]}
        input = ""
        token_with_escape(input, escape="^", separator="|")

        # TR = {[8, 11, 12], [11, 12, 13], [12, 13, 15], [13, 15, 19], [15, 19, 11], [19, 11, 12], [11, 12, 13], [12, 13, 14], [13, 14, 11], [14, 11, 23]}
        input = "a^"
        token_with_escape(input, escape="^", separator="|")

        # TR = {[8, 11, 12], [11, 12, 13], [12, 13, 15], [13, 15, 19], [15, 19, 11], [19, 11, 12], [11, 12, 13], [12, 13, 15], [13, 15, 16], [15, 16, 11], [16, 11, 23]}
        input = "a|"
        token_with_escape(input, escape="^", separator="|")

        # TR = {[8, 11, 12], [11, 12, 13], [12, 13, 15], [13, 15, 19], [15, 19, 11], [19, 11, 12], [11, 12, 13], [12, 13, 15], [13, 15, 16], [15, 16, 11], [16, 11, 12], [11, 12, 13], [12, 13, 14], [13, 14, 11], [14, 11, 12], [11, 12, 20], [12, 20, 21], [20, 21, 11], [21, 11, 23]}
        input = "a|^b"
        token_with_escape(input, escape="^", separator="|")

        # TR = {[8, 11, 12], [11, 12, 13], [12, 13, 15], [13, 15, 19], [15, 19, 11], [19, 11, 12], [11, 12, 13], [12, 13, 14], [13, 14, 11], [14, 11, 12], [11, 12, 20], [12, 20, 21], [20, 21, 11], [21, 11, 12], [11, 12, 13], [12, 13, 15], [13, 15, 19], [15, 19, 11], [19, 11, 23]}
        input = "a^bc"
        token_with_escape(input, escape="^", separator="|")
