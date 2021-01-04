from collections import OrderedDict, deque, namedtuple
from enum import Enum
import sys

OPEN_CHARS = ['.', 'G', 'E']
INITIAL_LIVE = 200
INPUT = 'input.txt'

class PlayerKind(Enum):
    ELVE = 'E'
    GOBLIN = 'G'


QueueUnit = namedtuple('QueueUnit', ['coordinates', 'path'])


class Player:
    def __init__(self, kind):
        self.kind = kind
        self.live = INITIAL_LIVE

    def __repr__(self):
        return '%s(%d)' % (self.kind.value, self.live)


def read_graph():
    players = {}
    graph = OrderedDict()
    with open(INPUT) as f:
        field = list(f)
    for x in range(1, len(field)-1):
        for y in range(1, len(field[x].strip())-1):
            if field[x][y] in OPEN_CHARS:
                neighbours_to_check = [(x-1, y), (x, y-1), (x, y+1), (x+1, y)]
                graph[(x, y)] = [(xn, yn) for xn, yn in neighbours_to_check if field[xn][yn] in OPEN_CHARS]
            if field[x][y] in ['G', 'E']:
                players[(x, y)] = Player(PlayerKind(field[x][y]))
    field = [row.replace('G', '.').replace('E', '.') for row in field]
    return graph, players, field


def game_finished(players):
    return len(set(p.kind for p in players.values())) == 1


def is_better_enemy(current_enemy, new_enemy):
    if current_enemy is None:
        return True

    if new_enemy.coordinates < current_enemy.coordinates:
        return True

    if new_enemy.coordinates == current_enemy.coordinates and new_enemy.path < current_enemy.path:
        return True

    return False


def get_move(player_coord, players, graph):
    queue = deque()
    queue.append(QueueUnit(player_coord, path=[]))
    found_enemy = None
    visited = set()
    while queue:
        q_u = queue.popleft()
        if q_u.coordinates in visited:
            continue

        if found_enemy is not None and len(found_enemy.path) < len(q_u.path):
            return found_enemy

        if not player_coord == q_u.coordinates:
            other_player = players.get(q_u.coordinates)
            if other_player is not None and other_player.kind != players[player_coord].kind:
                # Enemy found
                if is_better_enemy(found_enemy, q_u):
                    found_enemy = q_u
                continue

        for neighbour in graph[q_u.coordinates]:
            neighbour_player = players.get(neighbour)
            if neighbour_player is None or neighbour_player.kind != players[player_coord].kind:
                queue.append(QueueUnit(neighbour, path=q_u.path + [neighbour]))

        visited.add(q_u.coordinates)
    return found_enemy


def choose_target(player_coord, players, graph):
    player = players[player_coord]
    best_target = None, None
    for neighbour in graph[player_coord]:
        other_player = players.get(neighbour)
        if other_player is not None and other_player.kind != player.kind:
            if best_target[0] is None or best_target[1].live > other_player.live:
                best_target = neighbour, other_player
     #       print('Target found %s, %s' % (neighbour, other_player))
    #print('Best target found %s, %s' % best_target)
    return best_target


def attack(player_coord, players, graph):
    target_coord, target = choose_target(player_coord, players, graph)
    if target is not None:
        target.live -= 3
        if target.live <= 0:
            players.pop(target_coord)


def can_attack(player_coord, players, graph):
    target_coord, _ = choose_target(player_coord, players, graph)
    return target_coord is not None


def play_round(graph, players):
    player_keys = list(sorted(players.keys()))
    for player_coord in player_keys:
        if player_coord in players:
            if game_finished(players):
                return True
            if not can_attack(player_coord, players, graph):
                best_move = get_move(player_coord, players, graph)
                if best_move is not None:
                    new_coord = best_move.path[0]
                    players[new_coord] = players.pop(player_coord)
                    player_coord = new_coord
            attack(player_coord, players, graph)
    return False


def get_score(players, round_n):
    return sum(p.live for p in players.values()) * (round_n - 1)


def print_cave(players, org_field):
    for x, row in enumerate(org_field):
        line = ''
        for y, c in enumerate(row.strip()):
            player = players.get((x, y))
            if player is None:
                line += c
            else:
                line += player.kind.value
        print(line)


def main():
    graph, players, org_field = read_graph()
    print(dict(graph))
    print(players)
    round_n = 0
    print_cave(players, org_field)
    finished = False
    while not finished:
        round_n += 1
        finished = play_round(graph, players)
        print('After %d' % round_n)
        print_cave(players, org_field)
        print(players)
    print(get_score(players, round_n))


if __name__ == '__main__':
    main()
