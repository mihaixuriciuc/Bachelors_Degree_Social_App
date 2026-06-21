"""
Follow-graph analysis for bot-network detection.

Models the follow relationships as a directed graph and finds dense
mutual-follow clusters — groups of accounts that heavily follow each
other, which is characteristic of bot farms inflating each other's
follower counts.

Kept separate from detection.py because building and analyzing a graph
is a distinct responsibility from scoring individual users.
"""

import networkx as nx

from apps.user.models import Follow


class FollowGraphService:

    @staticmethod
    def build_graph():
        """
        Build a directed graph from the entire Follow table.

        Each user is a node. Each follow is a directed edge from follower
        to following. We load all follows in one query (values_list) rather
        than iterating model instances, to keep it fast.
        """
        graph = nx.DiGraph()

        # One query: all (follower_id, following_id) pairs.
        edges = Follow.objects.values_list('follower_id', 'following_id')
        graph.add_edges_from(edges)

        return graph

    @staticmethod
    def find_dense_clusters(min_size, min_density):
        """
        Find clusters of accounts that mutually follow each other densely.

        Steps:
        1. Build the directed follow graph.
        2. Reduce it to MUTUAL follows only — keep an edge between two users
           only if BOTH follow each other. Bot farms are characterized by
           reciprocal following; one-directional follows are normal.
        3. Treat those mutual relationships as an undirected graph and find
           connected components (the isolated clusters).
        4. For each component at or above min_size, compute its density
           (how many of the possible connections actually exist). Flag
           components whose density is at or above min_density.

        Returns a list of clusters, each a set of user IDs.
        """
        directed = FollowGraphService.build_graph()

        # Step 2: build an undirected graph of mutual follows only.
        mutual = nx.Graph()
        for u, v in directed.edges():
            # If v also follows u, it's a mutual follow.
            if directed.has_edge(v, u):
                mutual.add_edge(u, v)

        if mutual.number_of_nodes() == 0:
            return []

        dense_clusters = []

        # Step 3: each connected component is a candidate cluster.
        for component in nx.connected_components(mutual):
            if len(component) < min_size:
                continue

            # Step 4: measure density of this component.
            subgraph = mutual.subgraph(component)
            density = nx.density(subgraph)

            if density >= min_density:
                dense_clusters.append(set(component))

        return dense_clusters

    @staticmethod
    def get_user_cluster(user_id, min_size, min_density):
        """
        Returns the dense cluster a given user belongs to, or None.
        Used by the per-user detection check.
        """
        clusters = FollowGraphService.find_dense_clusters(min_size, min_density)
        for cluster in clusters:
            if user_id in cluster:
                return cluster
        return None