from itertools import combinations

from tqdm import tqdm

from bcsl.graph_utils import get_all_edges_from


class Hiton:
    def __init__(self, data, conditional_independence_test, max_k=3, verbose=False):
        self.data = data
        self.conditional_independence_test = conditional_independence_test
        self.max_k = max_k
        self.verbose = verbose

    def get_markov_blanket(self, target_var, alpha=0.05, spouses=True):
        """
        HITON algorithm to find the Markov Blanket (MB) set for a target variable.
        This combines HITON-PC for the Parents and Children and the Spouse discovery.
        :param target_var: The target variable index.
        :param alpha: Significance level for the conditional independence test.
        :param spouses: Whether to discover spouses (default: True).
        :return: The MB set (indices of variables in the Markov Blanket), skeleton, sepset, and ci_count.
        """
        n_vars = self.data.shape[1]
        candidate_set = list(range(n_vars))
        candidate_set.remove(target_var)  # Remove the target itself
        ci_count = 0  # Counter for the number of conditional independence tests
        sepset = [[] for _ in range(n_vars)]  # Separating sets

        # Step 1: HITON-PC (Parents and Children discovery)
        variDepSet = []
        for var in candidate_set:
            p_value = self.conditional_independence_test(target_var, var)
            ci_count += 1
            if p_value < alpha:  # Dependent variables
                variDepSet.append([var, p_value])

        # Sort candidate variables by dependency (smaller p-value means stronger dependency)
        variDepSet = sorted(variDepSet, key=lambda x: x[1])
        candidate_PC = [var[0] for var in variDepSet]  # Candidate PC set

        # Shrink phase: Test conditional independence with subsets of other variables in the PC set
        pc_set = candidate_PC[:]
        if self.verbose:
            loop_over = tqdm(candidate_PC, desc="HITON-PC: Shrink Phase", position=2)
        else:
            loop_over = candidate_PC
        for x in loop_over:
            conditions_Set = [i for i in pc_set if i != x]

            # Limit the size of conditional sets based on max_k
            for k in range(1, min(self.max_k, len(conditions_Set)) + 1):
                if x not in pc_set:
                    break
                for subset in combinations(conditions_Set, k):
                    p_value = self.conditional_independence_test(
                        target_var, x, list(subset)
                    )
                    ci_count += 1
                    if p_value >= alpha:  # If conditionally independent
                        sepset[x] = list(subset)  # Store the separating set
                        pc_set.remove(x)
                        break

        currentMB = pc_set.copy()
        current_skeleton = get_all_edges_from(target_var, currentMB)
        direct_neighbors = currentMB.copy()

        # Step 2: Spouse Discovery
        if spouses:
            if self.verbose:
                loop_over = tqdm(pc_set, desc="Spouse Discovery", position=3)
            else:
                loop_over = pc_set
            for x in loop_over:
                PCofPC, _, _, ci_num2 = self(
                    x, alpha, spouses=False
                )  # Find PC of each PC variable (Spouse discovery)
                ci_count += ci_num2

                for y in PCofPC:
                    if y != target_var and y not in direct_neighbors:
                        # Add conditioning on x (spouse candidate) for the target variable
                        conditions_Set = sepset[y] + [x]
                        conditions_Set = list(set(conditions_Set))  # Avoid duplicates
                        pval = self.conditional_independence_test(
                            target_var, y, conditions_Set
                        )
                        ci_count += 1
                        if pval <= alpha:
                            currentMB.append(y)  # Add spouse to the Markov Blanket
                            # X is a collider Target -> X <- Y
                            current_skeleton.append((y, x))  # Add edge from x to y
                            # TODO: BCSL could probably be extended to bootstrap the
                            #  edge orientations as well. Could orient the edges in the skeleton,
                            #  as a collider is detected

        sepsets = {
            (target_var, j): set(sepset[j]) for j in range(n_vars) if j != target_var
        }
        for key in list(sepsets.keys()):
            sepsets[key[::-1]] = sepsets[key]

        return list(set(currentMB)), set(current_skeleton), sepsets, ci_count

    def __call__(self, target_var, alpha=0.05, spouses=True):
        return self.get_markov_blanket(target_var, alpha, spouses)
