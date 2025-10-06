class Node:
    def __init__(self, feature=None, threshold=None, left=None, right=None, value=None, isDiscrete = None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value
        self.isDiscrete = isDiscrete

    # A node is a leaf node if it has a value, nodes in the middle of a tree
    # shouldn't have a value since we are still determining possible cases
    def isLeaf(self):
        """
        Leaf when there is a label value
        :return: Final label value
        """
        return self.value is not None
