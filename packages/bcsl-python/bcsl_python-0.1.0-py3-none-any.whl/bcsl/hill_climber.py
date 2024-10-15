class HillClimber:
    def __init__(self, score_function, get_neighbors_func):
        """
        Initialize the HillClimber.
        :param score_function: A scoring function (e.g., BDeuScore) to guide the search.
        :param get_neighbors_func: A function from BCSL class to generate neighboring graphs.
        """
        self.score_function = score_function
        self.get_neighbors_func = get_neighbors_func  # Passed function to generate neighbors

    def run(self, initial_graph, max_iter=1000):
        """
        Perform hill-climbing search to find the best graph configuration.
        This method will optimize the edge orientations in the graph.
        :param initial_graph: The starting point of the hill-climbing (global skeleton).
        """
        current_graph = initial_graph
        current_score = self.score_function.calculate(current_graph)
        i = 0
        print(f"Hill Climbing started with {max_iter} iterations.")
        print(f"Initial score = {current_score}")
        while i < max_iter:
            if i % 100 == 0:
                print(f"Iteration {i}: Best score = {current_score}")
            neighbors = self.get_neighbors_func(current_graph)  # Use BCSL's get_neighbors
            best_neighbor = None
            best_score = current_score

            for neighbor in neighbors:
                neighbor_score = self.score_function.calculate(neighbor)
                if neighbor_score > best_score:
                    best_score = neighbor_score
                    best_neighbor = neighbor

            # If no better neighbor is found, stop
            if best_neighbor is None:
                print(f"Iteration {i}: No better neighbor found. Stopping. Best score = {current_score}")
                break

            current_graph = best_neighbor
            current_score = best_score
            i += 1
            if i == max_iter:
                print(f"Max iteration reached without convergence. Best score = {current_score}")

        return current_graph
