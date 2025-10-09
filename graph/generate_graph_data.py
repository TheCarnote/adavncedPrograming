import csv
import random
import string
import argparse


def generate_random_string(length=4):
    """Génère une chaîne de caractères aléatoire de la longueur spécifiée."""
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def generate_graph_files(num_nodes, num_connections, coord_min, coord_max):
    """
    Génère les fichiers nodes.csv et connections.csv.
    """
    node_ids = [generate_random_string() for _ in range(num_nodes)]

    # Écriture du fichier nodes.csv
    with open('nodes.csv', 'w', newline='') as node_file:
        writer = csv.writer(node_file)
        writer.writerow(['node_id', 'x', 'y', 'z'])
        for node_id in node_ids:
            x = random.randint(coord_min, coord_max)
            y = random.randint(coord_min, coord_max)
            z = random.randint(coord_min, coord_max)
            writer.writerow([node_id, x, y, z])

    # Écriture du fichier connections.csv
    with open('connections.csv', 'w', newline='') as conn_file:
        writer = csv.writer(conn_file)
        writer.writerow(['source', 'target'])

        # S'assure de ne pas générer des connexions redondantes
        added_connections = set()
        while len(added_connections) < num_connections:
            source, target = random.sample(node_ids, 2)
            if source != target and (source, target) not in added_connections and (
            target, source) not in added_connections:
                writer.writerow([source, target])
                added_connections.add((source, target))

    print(f"Génération terminée. {num_nodes} nœuds et {len(added_connections)} connexions ont été créés.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Générateur de fichiers de graphe pour le problème du plus court chemin.")
    parser.add_argument('-n', '--num_nodes', type=int, default=5000, help="Nombre de nœuds à générer.")
    parser.add_argument('-c', '--num_connections', type=int, default=20000, help="Nombre de connexions à générer.")
    parser.add_argument('-min', '--coord_min', type=int, default=-1000, help="Coordonnée minimale.")
    parser.add_argument('-max', '--coord_max', type=int, default=1000, help="Coordonnée maximale.")

    args = parser.parse_args()
    generate_graph_files(args.num_nodes, args.num_connections, args.coord_min, args.coord_max)
