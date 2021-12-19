from unittest import TestCase, main
import unittest

from year2021.day18.a import Node, sum_nodes


class TestNodes(TestCase):
    def test_reduce(self):

        in_data = [
            "[[[[[9,8],1],2],3],4]",
            "[7,[6,[5,[4,[3,2]]]]]",
            "[[6,[5,[4,[3,2]]]],1]",
            "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]",
        ]
        expected_data = [
            "[[[[0,9],2],3],4]",
            "[7,[6,[5,[7,0]]]]",
            "[[6,[5,[7,0]]],3]",
            "[[3,[2,[8,0]]],[9,[5,[7,0]]]]",
        ]
        for node_str, exptected in zip(in_data, expected_data):
            with self.subTest(node_str=node_str):
                node = Node.parse(node_str)
                node.reduce()
                self.assertEqual(exptected, str(node))

        self.assertTrue(True)

    def add_sum(self, *nodes_str, expected):
        nodes = [Node.parse(node_str) for node_str in nodes_str]
        res = sum_nodes(nodes)
        self.assertEqual(expected, str(res))
        return res

    def test_sum1(self):
        res = self.add_sum(
            "[[[[4,3],4],4],[7,[[8,4],9]]]",
            "[1,1]",
            expected="[[[[0,7],4],[[7,8],[6,0]]],[8,1]]",
        )
        leaf = res.left.left.left.left
        leaves = []
        while leaf is not None:
            leaves.append(leaf)
            leaf = leaf.right_leaf
        leaves_rev = []
        leaf = res.right.right
        while leaf is not None:
            leaves_rev.append(leaf)
            leaf = leaf.left_leaf
        self.assertEqual(list(reversed(leaves_rev)), leaves)
        self.assertEqual([x.val for x in leaves], [0, 7, 4, 7, 8, 6, 0, 8, 1])

    def test_sum2(self):
        self.add_sum(
            "[1,1]",
            "[2,2]",
            "[3,3]",
            "[4,4]",
            "[5,5]",
            "[6,6]",
            expected="[[[[5,0],[7,4]],[5,5]],[6,6]]",
        )

    def test_sum3(self):
        res = self.add_sum(
            "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]",
            "[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]",
            expected="[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]",
        )

    def test_sum4(self):
        self.add_sum(
            "[0,[0,[0,[8,9]]]]",
            "[[[0,8],0],0]",
            expected="[[0,[0,[8,0]]],[[[9,8],0],0]]",
        )

    def test_sum5(self):
        self.add_sum(
            "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]",
            "[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]",
            "[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]",
            "[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]",
            "[7,[5,[[3,8],[1,4]]]]",
            "[[2,[2,2]],[8,[8,1]]]",
            "[2,9]",
            "[1,[[[9,3],9],[[9,0],[0,7]]]]",
            "[[[5,[7,4]],7],1]",
            "[[[[4,2],2],6],[8,7]]",
            expected="[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]",
        )

    def test_sum6(self):
        res = self.add_sum(
            "[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]",
            "[[[5,[2,8]],4],[5,[[9,9],0]]]",
            "[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]",
            "[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]",
            "[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]",
            "[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]",
            "[[[[5,4],[7,7]],8],[[8,3],8]]",
            "[[9,3],[[9,9],[6,[4,9]]]]",
            "[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]",
            "[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]",
            expected="[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]",
        )
        self.assertEqual(res.magnitude(), 4140)


if __name__ == "__main__":
    main()
