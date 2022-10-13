import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm


PUPILS = [
    "Lukas", "Jonas", "Simon", "Melissa", "Marlene", "Lora", "Jonathan", "Sophia", "Janko", "Ian",
    "Magdalena", "Julia", "Constantin", "Caroline", "Hannah"
]

LIKES_WORKING_WITH = {
    "Lukas": ["Ian", "Jonas", "Melissa"],
    "Jonas": ["Lukas", "Ian", "Marlene"],
    "Simon": ["Lukas", "Marlene", "Lora"],
    "Melissa": ["Lukas", "Jonas", "Lora"],
    "Marlene": ["Lukas", "Julia", "Sophia"],
    "Lora": ["Sophia", "Julia", "Marlene"],
    "Jonathan": ["Julia", "Marlene"],
    "Sophia": ["Lora", "Caroline", "Melissa"],
    "Janko": ["Constantin", "Lukas", "Julia"],
    "Ian": ["Lukas", "Jonas", "Melissa"],
    "Magdalena": ["Hannah", "Lora", "Melissa"],
    "Julia": ["Marlene", "Lora", "Sophia"],
    "Constantin": ["Janko", "Caroline"],
    "Caroline": ["Hannah", "Marlene", "Sophia"],
    "Hannah": ["Caroline", "Sophia", "Marlene"],
}

DOES_NOT_LIKE_WORKING_WITH = {
    "Lukas": ["Simon", "Janko", "Constantin"],
    "Jonas": ["Constantin", "Janko", "Simon"],
    "Simon": ["Janko", "Constantin", "Hannah"],
    "Melissa": [],
    "Marlene": ["Simon", "Janko", "Constantin"],
    "Lora": ["Janko", "Constantin", "Simon"],
    "Jonathan": [],
    "Sophia": ["Constantin", "Janko", "Simon"],
    "Janko": ["Simon", "Jonathan"],
    "Ian": ["Simon", "Constantin",  "Janko"],
    "Magdalena": ["Ian", "Lukas", "Jonas"],
    "Julia": ["Simon"],
    "Constantin": ["Simon", "Hannah"],
    "Caroline": ["Simon", "Janko", "Jonathan"],
    "Hannah": ["Simon", "Janko", "Constantin"],
}

def count_likes(name: str) -> int:
    return sum([1 for likes in LIKES_WORKING_WITH.values() for like in likes if like==name])

def count_dislikes(name: str) -> int:
    return sum([1 for dislikes in DOES_NOT_LIKE_WORKING_WITH.values() for dislike in dislikes if dislike==name])

class Sociogram:
    def __init__(self, pupils, likes_working_with, does_not_like_working_with):
        self.pupils = pupils
        self.likes_working_with = likes_working_with
        self.does_not_like_working_with = does_not_like_working_with
        self.graph = nx.DiGraph()

    def sort_nodes(self):
        self.pupils.sort(key=lambda p:abs(count_likes(p) - count_dislikes(p)))

    def add_nodes(self):
        self.graph.add_nodes_from(self.pupils)

    def add_edges(self):
        for name, like_list in self.likes_working_with.items():
            for like in like_list:
                self.graph.add_edge(name, like, color='g')

        for name, not_like_list in self.does_not_like_working_with.items():
            for not_like in not_like_list:
                self.graph.add_edge(name, not_like, color='r')

    def modified_labels(self):
        additional_labels = dict()
        for p in self.pupils:
            additional_labels[p] = f"{p}\n+{count_likes(p)} / -{count_dislikes(p)}"
        return additional_labels

    def plot(self):
        pos = nx.circular_layout(self.graph)
        colors = nx.get_edge_attributes(self.graph,'color').values()
        labels = self.modified_labels()

        nx.draw(
            self.graph,
            pos=pos,
            edge_color=colors,
            with_labels=True,
            labels=labels,
            node_size=6000,
            node_color='#e1e1e1',
            edgecolors="#3f3f3f",
            connectionstyle='arc3, rad = 0.1'
        )

        plt.axis('equal')
        plt.show()


def main():
    sociogram = Sociogram(PUPILS, LIKES_WORKING_WITH, DOES_NOT_LIKE_WORKING_WITH)
    sociogram.sort_nodes()
    sociogram.add_nodes()
    sociogram.add_edges()
    sociogram.plot()


if __name__ == '__main__':
    main()

