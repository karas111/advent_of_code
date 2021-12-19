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

    def test_sum1(self):
        self.add_sum(
            "[[[[4,3],4],4],[7,[[8,4],9]]]",
            "[1,1]",
            expected="[[[[0,7],4],[[7,8],[6,0]]],[8,1]]",
        )

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
        self.add_sum(
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


if __name__ == "__main__":
    main()
