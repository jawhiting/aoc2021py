from typing import List

import utils


def part1(lines: List[str], ):
    fish: List[int] = [0] * 9
    print(fish)
    for l in lines:
        ints = utils.extractInts(l)
        for i in ints:
            fish[i] += 1

    print(fish)
    after18 = multi_tick(fish, 18)
    after80 = multi_tick(fish, 80)
    after256 = multi_tick(fish, 256)
    print(f"After 18: {sum(after18)} Fish: {after18}")
    print(f"After 80: {sum(after80)} Fish: {after80}")
    print(f"After 256: {sum(after256)} Fish: {after256}")

def multi_tick(fish: List[int], count: int) -> List[int]:
    current = fish
    for i in range(count):
        current = tick(current)
    return current

def tick(fish: List[int]) -> List[int]:
    result = [0]*9
    for i in range(len(fish)):
        if i == 0:
            # spawn new and reset old
            result[8] += fish[i]
            result[6] += fish[i]
        else:
            # decrement
            result[i-1] += fish[i]
    return result


test_input = "3,4,3,1,2"
input = "3,3,5,1,1,3,4,2,3,4,3,1,1,3,3,1,5,4,4,1,4,1,1,1,3,3,2,3,3,4,2,5,1,4,1,2,2,4,2,5,1,2,2,1,1,1,1,4,5,4,3,1,4,4,4,5,1,1,4,3,4,2,1,1,1,1,5,2,1,4,2,4,2,5,5,5,3,3,5,4,5,1,1,5,5,5,2,1,3,1,1,2,2,2,2,1,1,2,1,5,1,2,1,2,5,5,2,1,1,4,2,1,4,2,1,1,1,4,2,5,1,5,1,1,3,1,4,3,1,3,2,1,3,1,4,1,2,1,5,1,2,1,4,4,1,3,1,1,1,1,1,5,2,1,5,5,5,3,3,1,2,4,3,2,2,2,2,2,4,3,4,4,4,1,2,2,3,1,1,4,1,1,1,2,1,4,2,1,2,1,1,2,1,5,1,1,3,1,4,3,2,1,1,1,5,4,1,2,5,2,2,1,1,1,1,2,3,3,2,5,1,2,1,2,3,4,3,2,1,1,2,4,3,3,1,1,2,5,1,3,3,4,2,3,1,2,1,4,3,2,2,1,1,2,1,4,2,4,1,4,1,4,4,1,4,4,5,4,1,1,1,3,1,1,1,4,3,5,1,1,1,3,4,1,1,4,3,1,4,1,1,5,1,2,2,5,5,2,1,5"

if __name__ == "__main__":
    part1([test_input])
    part1([input])

