import logging
import os
from typing import Tuple, List
import math

from year2019.utils import init_logging

logger = logging.getLogger(__name__)

INPUT_FILE = "input.txt"


def read_input() -> List[str]:
    with open(os.path.join(os.path.dirname(__file__), INPUT_FILE)) as f:
        return [line.strip() for line in f if line]


class Packet:
    def __init__(self, version: int, type_id: int) -> None:
        self.version = version
        self.type_id = type_id

    def __repr__(self) -> str:
        return f"V={self.version}, T={self.type_id}"

    def sum_version(self) -> int:
        return self.version

    def calculate(self) -> int:
        raise NotImplementedError()


class PacketLiteral(Packet):
    def __init__(self, version: int, type_id: int, value: int) -> None:
        super().__init__(version, type_id)
        self.value = value

    def __repr__(self) -> str:
        return f"{super().__repr__()} Literal={self.value}"

    def calculate(self) -> int:
        return self.value


class PacketOperator(Packet):
    def __init__(
        self, version: int, type_id: int, length_type_id: int, sub_packets: List[Packet]
    ) -> None:
        super().__init__(version, type_id)
        self.length_type_id = length_type_id
        self.sub_packets = sub_packets

    def __repr__(self) -> str:
        sub_packet_str = ", ".join(f"({packet})" for packet in self.sub_packets)
        return f"{super().__repr__()} LT={self.length_type_id} SP=[{sub_packet_str}]"

    def sum_version(self) -> int:
        return self.version + sum(
            sub_packet.sum_version() for sub_packet in self.sub_packets
        )

    def calculate(self) -> int:
        sub_values = [sub_packet.calculate() for sub_packet in self.sub_packets]
        if self.type_id == 0:
            return sum(sub_values)
        elif self.type_id == 1:
            return math.prod(sub_values)
        elif self.type_id == 2:
            return min(sub_values)
        elif self.type_id == 3:
            return max(sub_values)
        elif self.type_id == 5:
            return int(sub_values[0] > sub_values[1])
        elif self.type_id == 6:
            return int(sub_values[0] < sub_values[1])
        elif self.type_id == 7:
            return int(sub_values[0] == sub_values[1])
        raise ValueError(f"Wrong packet {self}")


def parse_literal_value(
    packet_str: str, idx: int, version: int, type_id: int
) -> Tuple[PacketLiteral, int]:
    value_str = ""
    while True:
        value_str += packet_str[idx + 1: idx + 5]
        idx += 5
        if packet_str[idx - 5] == "0":
            break
    value = int(value_str, base=2)
    return PacketLiteral(version, type_id, value), idx


def parse_operator(
    packet_str: str, idx: int, version: int, type_id: int
) -> Tuple[PacketLiteral, int]:
    length_type_id = int(packet_str[idx], base=2)
    idx += 1
    sub_packets = []
    if length_type_id == 0:
        tot_length_sub = int(packet_str[idx: idx + 15], base=2)
        idx += 15
        sub_end_idx = idx + tot_length_sub
        while idx < sub_end_idx:
            sub_packet, idx = parse_packet(packet_str, idx)
            sub_packets.append(sub_packet)
    else:
        number_of_sub_packets = int(packet_str[idx: idx + 11], base=2)
        idx += 11
        while len(sub_packets) < number_of_sub_packets:
            sub_packet, idx = parse_packet(packet_str, idx)
            sub_packets.append(sub_packet)
    return PacketOperator(version, type_id, length_type_id, sub_packets), idx


def parse_packet(packet_str: str, idx=0) -> Tuple[Packet, int]:
    version, type_id = [
        int(packet_str[idx + i * 3: idx + (i + 1) * 3], base=2) for i in range(2)
    ]
    idx += 6
    if type_id == 4:
        packet, idx = parse_literal_value(packet_str, idx, version, type_id)
    else:
        packet, idx = parse_operator(packet_str, idx, version, type_id)
    return packet, idx


def to_binary_str(hex_str: str) -> str:
    return "".join([format(int(char, base=16), "04b") for char in hex_str])


def main():
    packets = read_input()
    for hex_str in packets:
        binary_str = to_binary_str(hex_str)
        packet, _ = parse_packet(binary_str)
        logger.info(f"Packet {packet}")
        logger.info(f"Res a {packet.sum_version()}")
        logger.info(f"Res b {packet.calculate()}")


if __name__ == "__main__":
    init_logging()
    main()
