import sys
from immutables import Map
from ..repr import newick
from .. import traversal


def run():
    tree = newick.parse(sys.stdin.read())

    tree = traversal.compress(
        lambda zipper: (
            isinstance(zipper.node.data, Map) and zipper.node.data["name"] == "a"
        ),
        tree,
    )

    print(newick.write(tree))
