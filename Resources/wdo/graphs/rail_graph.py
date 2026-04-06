def extract_endpoints(feature):
    """Extract endpoints from a line-like feature."""
    raise NotImplementedError


def make_edge_weights(edges):
    """Attach weights (distances) to edges."""
    raise NotImplementedError


def build_graph_from_lines(features):
    """Convert railroad features into a graph structure."""
    raise NotImplementedError
