import networkx as nx
import matplotlib.pyplot as plt


class Epruvette:
    def __init__(self, raw):
        self.slots = list(raw)

    def __str__(self):
        return self.raw()

    def raw(self):
        return "".join(self.slots)

    def top(self):
        """Return the top liquid in the epruvette."""
        for slot in self.slots:
            if slot != "E":
                return slot
        return "E"

    def space(self):
        """Return the number of empty slots."""
        return self.slots.count("E")

    def top_volume(self):
        """Return the volume of the top liquid in the epruvette."""
        i = 0
        for slot in self.slots:
            if slot == "E":
                continue
            else:
                i += 1

            if slot != self.top():
                return i - 1
        return i

    def can_pour_into(self, dest):
        """Check if the top liquid can be poured into the destination epruvette."""
        liquid_matches = dest.top() == self.top() or dest.top() == "E"
        has_space = dest.space() >= self.top_volume()
        is_not_empty = self.top() != "E"
        return liquid_matches and has_space and is_not_empty

    def pour_into(self, dest):
        """Pour the top liquid into the destination epruvette."""
        pour = [self.top()] * self.top_volume()
        void = ["E"] * self.top_volume()

        dest.slots[dest.space() - self.top_volume() : dest.space()] = pour
        self.slots[self.space() : self.space() + self.top_volume()] = void

    def is_solved(self):
        """Check if the epruvette is solved."""
        return self.top() == "E" or self.top_volume() == len(self.slots)


class Configuration:
    def __init__(self, raw):
        if isinstance(raw, Configuration):
            self.epruvettes = [Epruvette(e.raw()) for e in raw.epruvettes]
            self.moves = raw.moves.copy()
        else:
            self.epruvettes = [Epruvette(raw_e) for raw_e in raw.split(",")]
            self.moves = []

    def __str__(self):
        return ",".join([e.raw() for e in self.epruvettes])

    def __repr__(self):
        return (
            "Configuration<"
            + ",".join(sorted([e.raw() for e in self.epruvettes]))
            + ">"
        )

    def __hash__(self):
        """Return a hash of the configuration."""
        return hash(self.__repr__())

    def __eq__(self, other):
        """Check if two configurations are equal."""
        return hash(self) == hash(other)

    def valid_moves(self):
        """Assemble a list of valid moves."""
        moves = []
        for i, source in enumerate(self.epruvettes):
            for j, target in enumerate(self.epruvettes):
                if i == j:
                    continue
                if source.can_pour_into(target):
                    moves.append((i, j))
        return moves

    def move(self, source, target):
        """Perform a move."""
        self.moves.append((source, target))
        self.epruvettes[source].pour_into(self.epruvettes[target])

    def is_solved(self):
        """Check if the configuration is solved."""
        return all([e.is_solved() for e in self.epruvettes])

    def colours(self):
        """Return the colours of the epruvettes."""
        return set([slot for e in self.epruvettes for slot in e.slots]) - {"E"}

    def completed(self):
        """Return the completed configuration."""
        epruvette_size = len(self.epruvettes[0].slots)
        epruvette_count = len(self.epruvettes)
        empty_epruvettes = ["E" * epruvette_size] * (
            epruvette_count - len(self.colours())
        )
        full_epruvettes = [colour * epruvette_size for colour in self.colours()]
        return Configuration(",".join(empty_epruvettes + full_epruvettes))


def solution_graph(config):
    """Return a graph of the solution."""
    G = nx.DiGraph()
    G.add_node(config)

    target_configuration = config.completed()
    solution_found = False

    queue = [config]
    seen = set()
    while queue:
        current = queue.pop(0)
        # If solution is found, mark it, then continue creating the rest of the graph
        if current == target_configuration and not solution_found:
            solution_found = True
            solution = current
        for move in current.valid_moves():
            new = Configuration(current)
            if new in seen:
                continue
            seen.add(new)

            new.move(*move)
            if new not in G:
                G.add_node(new)
                queue.append(new)
            G.add_edge(current, new)
    return G, solution


"""
B - Blue
L - Light blue
Y - Yellow
R - Red
T - Teal
O - Orange
I - pInk
G - Gray

E - Empty
"""

level3 = "PRYY,PRYP,RYPR,EEEE,EEEE"
level1 = "RY,YR,EE"
level77 = "BRBL,PORI,IGPL,LLYG,IYYT,TPRR,OOBY,GGBO,PTIT,EEEE,EEEE"
conf = Configuration(level77)
G, final = solution_graph(conf)

# draw the graph
# pos = nx.spring_layout(G, k=0.3, iterations=20)
# nx.draw_planar(G, with_labels=True, font_weight="bold")
# plt.show()

print(final.moves)
