def check_blocks(blocks: list[list[int]]):
    """Perform check on block information passed to a Block diagonal covariance Gaussian

    Block information is passed as a list of index list. Each index list describes which parameter
    are in each group.
    Checks:
        - that no index is in two groups
        - that all index in 0 ... n_max - 1 is in one group
    """
    items = [i for group in blocks for i in group]
    set_items = set(items)
    n_tot = len(set_items)

    if n_tot != len(items):
        raise ValueError("An index should be in only one group")

    if set_items != set(range(n_tot)):
        raise ValueError(f"All indexes between 0 and {n_tot} should belong to a group")
