from collections import defaultdict


def bron_kerbosch(R, P, X, G, C):
    if len(P) == 0 and len(X) == 0:
        if len(R) > 2:
            C.append(sorted(R))
        return

    for v in P.union(set([])):
        bron_kerbosch(
            R.union(set([v])), P.intersection(G[v]), X.intersection(G[v]), G, C
        )
        P.remove(v)
        X.add(v)


def part1(connections: dict[str, set[str]]) -> int:
    result_sets = set()

    for x in connections:
        for y in connections[x]:
            for z in connections[y]:
                if z not in connections[x]:
                    continue
                three = frozenset({x, y, z})
                if len(three) < 3:
                    continue
                if not any(c.startswith("t") for c in three):
                    continue
                result_sets.add(three)

    return len(result_sets)


def part2(connections: dict[str, set[str]]) -> str:
    p2_result = []
    bron_kerbosch(set(), set(connections.keys()), set(), connections, p2_result)
    biggest_lan = max(p2_result, key=len)
    return ",".join(sorted(biggest_lan))


if __name__ == "__main__":
    with open("input.txt") as f:
        f = map(str.strip, f)
        f = list(map(lambda pair: pair.split("-"), f))
    connections = defaultdict(set)

    for a, b in f:
        connections[a].add(b)
        connections[b].add(a)

    print("p1", part1(connections))
    print("p2", part2(connections))
