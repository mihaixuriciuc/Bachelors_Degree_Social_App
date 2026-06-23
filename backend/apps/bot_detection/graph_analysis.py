import networkx as nx
from apps.user.models import Follow
class FollowGraphService:

    @staticmethod
    def build_graph():
        """
        this one builds the grapgh
        """
        graph = nx.DiGraph() # directed graph


        edges = Follow.objects.values_list('follower_id', 'following_id')  # extracts directed who folows who
        graph.add_edges_from(edges)  #adds them to the graph

        return graph

    @staticmethod
    def find_dense_clusters(min_size, min_density):
        directed = FollowGraphService.build_graph() #directed graph above


        mutual = nx.Graph() #empty undirected graph
        for u, v in directed.edges():
            # If v also follows u, it's a mutual follow.
            if directed.has_edge(v, u):
                mutual.add_edge(u, v)       # verifies if there is a (1,2) there is also a (2,1) and it adds it as unidirectional

        if mutual.number_of_nodes() == 0:
            return []       #if there are not any nodes, if there is not a mutual follow at all

        dense_clusters = []


        for component in nx.connected_components(mutual): # nx conn components measuers how many different components are there, this also goes from node to node to determine the clusters
            if len(component) < min_size:
                continue # asta continua mereu uit care e care, break o rupe


            subgraph = mutual.subgraph(component) #make a graph with a found cluster to check its density
            density = nx.density(subgraph) # computes density nr of connections / nr of possible conections

            if density >= min_density:
                dense_clusters.append(set(component))

        return dense_clusters

    @staticmethod
    def get_user_cluster(user_id, min_size, min_density):   # iterate to each cluster to see if an user is there

        clusters = FollowGraphService.find_dense_clusters(min_size, min_density)
        for cluster in clusters:
            if user_id in cluster:
                return cluster
        return None