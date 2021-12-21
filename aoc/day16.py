import math
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Iterator

from aocd import data

test_input1 = "D2FE28"


@dataclass
class Packet:
    version: int
    type_id: int
    literal: Optional[int] = None
    sub_packets: List["Packet"] = field(default_factory=list)

    def version_sum(self) -> int:
        return self.version + sum([p.version_sum() for p in self.sub_packets])

    def value(self) -> int:
        if self.type_id == 0:
            return sum(self.child_values())
        if self.type_id == 1:
            return math.prod(self.child_values())
        if self.type_id == 2:
            return min(self.child_values())
        if self.type_id == 3:
            return max(self.child_values())
        if self.type_id == 4:
            return self.literal
        if self.type_id == 5:
            return 1 if self.sub_packets[0].value() > self.sub_packets[1].value() else 0
        if self.type_id == 6:
            return 1 if self.sub_packets[0].value() < self.sub_packets[1].value() else 0
        if self.type_id == 7:
            return 1 if self.sub_packets[0].value() == self.sub_packets[1].value() else 0

    def child_values(self) -> List[int]:
        return [sp.value() for sp in self.sub_packets]


def part1(packet: str):
    bits = bitstream(packet)
    packet, bits_read = read_packet(bits)
    print(f"BR: {bits_read} Packets: {packet}")
    print(f"VersionSum: {packet.version_sum()}")


def part2(packet: str):
    bits = bitstream(packet)
    packet, bits_read = read_packet(bits)
    print(f"Value: {packet.value()}")


def read_packet(bits: Iterator[int]) -> Tuple[Packet, int]:
    version = read_num(bits, 3)
    type_id = read_num(bits, 3)
    bits_read = 6
    # print(f"Version: {version} Type: {type_id}")
    if type_id == 4:
        # Literal
        literal, br = read_literal(bits)
        bits_read += br
        # print(f"Literal: {literal}")
        return Packet(version, type_id, literal), bits_read
    else:
        # Operator type
        length_type_id = read_num(bits, 1)
        bits_read += 1
        sub_packets: List[Packet] = []
        if length_type_id:
            # 11 bits number of sub-packets
            sub_packet_count = read_num(bits, 11)
            bits_read += 11
            for p in range(sub_packet_count):
                sub_packet, br = read_packet(bits)
                bits_read += br
                sub_packets.append(sub_packet)
        else:
            sub_packet_length = read_num(bits, 15)
            bits_read += 15
            sub_packet_br = 0
            while sub_packet_br < sub_packet_length:
                sub_packet, br = read_packet(bits)
                bits_read += br
                sub_packet_br += br
                sub_packets.append(sub_packet)
        return Packet(version, type_id, None, sub_packets), bits_read


def read_literal(bits: Iterator[int]) -> Tuple[int, int]:
    result = 0
    bits_read = 0
    while True:
        more_to_read = read_num(bits, 1)
        segment = read_num(bits, 4)
        bits_read += 5
        result *= 16
        result += segment
        if not more_to_read:
            break
    return result, bits_read


def read_num(bits: Iterator[int], bit_count: int) -> int:
    result = 0
    for c in range(bit_count):
        result *= 2
        result += next(bits)
    return result


def bitstream(hex_str: str) -> Iterator[int]:
    for c in hex_str:
        num = int(c, base=16)
        num_binary_str = bin(num)[2:].zfill(4)
        for n in num_binary_str:
            yield int(n)


if __name__ == "__main__":
    part1(test_input1)
    part1("38006F45291200")
    part1("EE00D40C823060")
    part1("8A004A801A8002F478")
    part1("620080001611562C8802118E34")
    part1("C0015000016115A2E0802F182340")
    part1("A0016C880162017C3686B18A3D4780")
    part1(data)

    print("== Part 2 ==")
    part2("C200B40A82")
    part2("04005AC33890")
    part2("880086C3E88112")
    part2("CE00C43D881120")
    part2("D8005AC2A8F0")
    part2("F600BC2D8F")
    part2("9C005AC2F8F0")
    part2("9C0141080250320F1802104A08")
    part2(data)
