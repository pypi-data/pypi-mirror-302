# Recursive function for Tower of Hanoi
import os
import inspect
from datetime import datetime
import networkx as nx
from pyvis.network import Network


class Track:
    instances = {}
    os.makedirs("../data", exist_ok=True)

    def __init__(self, input_function):
        self.lista_relazioni = {}
        self.ordine_frame = {}
        self.parameters = {}
        self.returns = {}
        self.input_function = input_function
        self.prev_frame = None
        self.n_call = 1
        self.output_file_path = f'{datetime.now().strftime("%Y%m%dT%H%M%S")}.txt'
        self.G = nx.DiGraph()

        Track.instances[input_function.__name__] = self

    def __get__(self, instance, owner):
        def wrapper(*args, **kwargs):
            current_frame = inspect.currentframe()
            self._register_parameters(str(id(current_frame)), args, kwargs)
            self._get_f_back_from_history(self.prev_frame, current_frame)

            with open(os.path.join("../data", self.output_file_path), "a") as f:
                f.write(self._create_log())

            self.prev_frame = current_frame

            result = self.input_function(instance, *args, **kwargs)
            self.returns[str(id(current_frame))] = result
            return result

        return wrapper

    def __call__(self, *args, **kwargs):
        current_frame = inspect.currentframe()
        self._register_parameters(str(id(current_frame)), args, kwargs)
        self._get_f_back_from_history(self.prev_frame, current_frame)

        with open(os.path.join("../data", self.output_file_path), "a") as f:
            f.write(self._create_log())

        self.prev_frame = current_frame
        result = self.input_function(*args, **kwargs)
        self.returns[str(id(current_frame))] = result
        return result

    def _get_f_back_from_history(self, last_frame, current_frame):
        nodo_figlio = str(id(current_frame))

        if (
            last_frame is not None
            and current_frame.f_back == last_frame.f_back  # same (DECORATED!) caller
        ):
            nodo_parente = str(
                id(
                    last_frame.f_back.f_back
                )  # true parent is one level above because input_function is decorated. that's why back.back
            )
            if nodo_figlio not in self.ordine_frame.keys():
                self.G.add_node(nodo_figlio, label=nodo_figlio)
                self.ordine_frame[nodo_figlio] = self.n_call
                self.n_call += 1

            self.G.add_edge(nodo_parente, nodo_figlio)
            self.lista_relazioni[nodo_parente].append(nodo_figlio)

            return

        if last_frame is None:
            return True

        if self._get_f_back_from_history(last_frame.f_back, current_frame):
            nodo_parente = str(id(self.prev_frame))

            if nodo_parente not in self.ordine_frame.keys():
                self.G.add_node(nodo_parente, label=nodo_parente)
                self.ordine_frame[nodo_parente] = self.n_call
                self.n_call += 1

            if nodo_figlio not in self.ordine_frame.keys():
                self.G.add_node(nodo_figlio, label=nodo_figlio)
                self.ordine_frame[nodo_figlio] = self.n_call
                self.n_call += 1

            self.G.add_edge(nodo_parente, nodo_figlio)
            self.lista_relazioni[nodo_parente] = [nodo_figlio]
            return

    def _register_parameters(self, frame_id, args, kwargs):
        self.parameters[frame_id] = {"args": args, "kwargs": kwargs}

    def _create_log(self):
        return f"\nChiamata numero {self.n_call}:\n\
        Albero istanze: {self.lista_relazioni}\n\
        Ordine istanze: {self.ordine_frame}\n\
        "

    @staticmethod
    def _rename_nodes(network_with_nodes, decorated_f):
        for j, node in enumerate(network_with_nodes.nodes):
            old_label = node["label"]
            new_label = (
                f"Call n. {str(decorated_f.ordine_frame[old_label])} "
                f"\nargs: {str(decorated_f.parameters[old_label]['args'])}"
                f"\nkwargs: {str(decorated_f.parameters[old_label]['kwargs'])}"
                f"\nreturn: {str(decorated_f.returns[old_label])}"
            )
            network_with_nodes.nodes[j]["label"] = new_label

    @classmethod
    def get_graph(cls, instance_name):
        decorated_f = cls.instances[instance_name]
        graph = decorated_f.G

        net = Network(notebook=False, directed=True)
        net.from_nx(graph)
        cls._rename_nodes(net, decorated_f)

        net.show_buttons(filter_=["layout", "physics"])

        # Salvataggio del file HTML e aggiunta del CSS personalizzato
        html_filename = f"{instance_name}.html"
        net.write_html(html_filename)

        with open(html_filename, "r") as file:
            html_content = file.read()

        with open("../config/default_graph.css", "r") as f:
            html_content = html_content.replace("</head>", f.read() + "</head>")

        with open(html_filename, "w") as file:
            file.write(html_content)


class Hanoi:
    def __init__(self, disks, source, helper, destination):
        self.disks = disks
        self.source = source
        self.helper = helper
        self.destination = destination

    def __call__(self):
        self.hanoi(self.disks, self.source, self.helper, self.destination)

    @Track
    def hanoi(self, disks, source, helper, destination):
        if disks == 1:
            print(f"disk {disks} goes from {source} to {destination}")
            return

        self.hanoi(disks - 1, source, destination, helper)
        print(f"disk {disks} goes from {source} to {destination}")
        self.hanoi(disks - 1, helper, source, destination)


@Track
def reverse_string(string):
    if len(string) == 0:
        return ""

    return reverse_string(string[1:]) + string[0]


@Track
def nth_fibonacci(n):
    print("f_back: ", id(inspect.currentframe().f_back.f_back))
    print("current_f: ", id(inspect.currentframe()))
    print("n: ", n)
    print("\n")
    # Base case: if n is 0 or 1, return n
    if n <= 1:
        return n

    # Recursive case: sum of the two preceding Fibonacci numbers
    return nth_fibonacci(n - 1) + nth_fibonacci(n - 2)

@Track
def hanoi_autonoma(disks, source, helper, destination):
    if disks == 1:
        print(f"disk {disks} goes from {source} to {destination}")
        return

    hanoi_autonoma(disks - 1, source, destination, helper)
    print(f"disk {disks} goes from {source} to {destination}")
    hanoi_autonoma(disks - 1, helper, source, destination)

if __name__ == "__main__":
    # Driver code
    # disks = int(input("Number of disks to be displaced: "))
    """
    Tower names passed as arguments:
    Source: A
    Helper: B
    Destination: C
    """
    # Actual function call
    hanoi = Hanoi(4, "A", "B", "C")
    hanoi()
    hanoi_autonoma(4, "A", "B", "C")
    print(reverse_string("ABC"))
    print(nth_fibonacci(5))
    Track.get_graph("nth_fibonacci")
    Track.get_graph("hanoi")
    Track.get_graph("hanoi_autonoma")
    Track.get_graph("reverse_string")
    # TODO: return value nel nodo?
