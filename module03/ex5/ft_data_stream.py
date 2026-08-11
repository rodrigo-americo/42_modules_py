from typing import Generator
import random

players: list[str] = ["mira", "toko", "vex", "hana", "orin"]
actions: list[str] = [
    "jump", "attack", "defend", "heal", "craft", "trade", "dance",
]


def gen_event() -> Generator[tuple[str, str], None, None]:
    while True:
        name = random.choice(players)
        action = random.choice(actions)
        yield (name, action)


def consome_event(
    events: list[tuple[str, str]]
) -> Generator[tuple[str, str], None, None]:
    while len(events) > 0:
        index = random.randint(0, len(events) - 1)
        item = events[index]
        events[index:index + 1] = []
        yield item


if __name__ == "__main__":
    print("=== Game Data Stream Processor ===")
    gen: Generator[tuple[str, str], None, None] = gen_event()
    for i in range(1, 1001):
        player, action = next(gen)
        print(f"Event {i}: Player {player} did action {action}")
    list_events: list[tuple[str, str]] = []
    for i in range(10):
        list_events += [next(gen)]
    print(f"Built list of 10 events: {list_events}")
    for event in consome_event(list_events):
        print(f"Got event from list: {event}")
        print(f"Remains in list: {list_events}")
