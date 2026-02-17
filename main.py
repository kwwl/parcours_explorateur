import pandas


def prepare_data(edges_df):
    starting_nodes = edges_df[edges_df["type_aretes"] == "depart"][
        "noeud_amont"
    ].tolist()
    dict_upstream_downstream = {
        row["noeud_amont"]: row["noeud_aval"] for _, row in edges_df.iterrows()
    }
    dict_distances = {
        row["noeud_amont"]: row["distance"] for _, row in edges_df.iterrows()
    }
    ending_nodes = set(edges_df[edges_df["type_aretes"] == "arrivee"]["noeud_aval"])

    return starting_nodes, dict_upstream_downstream, dict_distances, ending_nodes


def build_explorators_paths(starting_nodes, dict_upstream_downstream, ending_nodes):
    explorators_paths = {}

    for index, starting_node in enumerate(starting_nodes):
        current_path = [starting_node]

        while current_path[-1] not in ending_nodes:
            current_node = current_path[-1]
            next_node = dict_upstream_downstream[current_node]

            current_path.append(next_node)

        explorators_paths[f"explorator_{index}"] = current_path

    return explorators_paths


def calculate_explorators_distances(explorators_paths, dict_distances):
    explorators_distances = {}

    for explorator_id, explorator_path in explorators_paths.items():
        total_distance = 0

        for i in range(len(explorator_path) - 1):
            current_node = explorator_path[i]
            total_distance += dict_distances[current_node]

        explorators_distances[explorator_id] = total_distance

    return explorators_distances


if __name__ == "__main__":
    edges_df = pandas.read_csv("./parcours_explorateurs.csv")

    starting_nodes, dict_upstream_downstream, dict_distances, ending_nodes = (
        prepare_data(edges_df)
    )

    explorators_paths = build_explorators_paths(
        starting_nodes, dict_upstream_downstream, ending_nodes
    )

    explorators_distances = calculate_explorators_distances(
        explorators_paths, dict_distances
    )

    for explorator_id, explorator_path in explorators_paths.items():
        print(explorator_id)
        print(explorator_path)
        print(f"Distance totale: {explorators_distances[explorator_id]}")
