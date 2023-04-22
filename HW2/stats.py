import sys
import json
from lxml import etree

# Input XML file name
fsimage = sys.argv[1]
# Output JSON file name
stats = sys.argv[2]


# Generate ElementTree
tree = etree.parse(open(fsimage))


# Number of files
num_file = len(tree.xpath('/fsimage/INodeSection/inode[type = "FILE"]'))
# Number of directories
num_dir = len(tree.xpath('/fsimage/INodeSection/inode[type = "DIRECTORY"]'))


# Generate a directory tree using the relationship in INodeDirectorySection
class Node:
    # Constructuor to initialize the Node object
    def __init__(self, inum):
        self.inum = inum
        self.children = []

    # Add the child node that has a certain iNumber
    def addChild(self, inum):
        self.children.append(Node(inum))

    # Match the parent iNumber and child iNumber to connect the nodes
    def matchChildToParent(self, child_inum, parent_inum):
        queue = [self]
        while len(queue) != 0:
            currentNode = queue.pop(0)
            if parent_inum == currentNode.inum:
                currentNode.addChild(child_inum)
            else:
                queue.extend(currentNode.children)

    # Find the max. depth of the directory tree
    def maxDepth(self):
        depth = 1
        # Base condition that the end of the tree has been reached
        if len(self.children) == 0:
            return depth
        # Call maxDepth() recursively
        else:
            for child in self.children:
                depth = max(depth, child.maxDepth()+1)
        return depth


# Find the root directory
root_inum = tree.xpath('/fsimage/INodeSection/inode[name[not(node())]]/id/text()')[0]
# Initialize the directory tree
root = Node(root_inum)


# Apply the matchChildToParent() method
for i in range(1, num_dir+1):
    # iNumber of the current parent directory
    parent_inum = tree.xpath('/fsimage/INodeDirectorySection/directory['
                             + str(i) + ']/parent/text()')[0]
    # Number of child under this directory
    num_child = len(tree.xpath('/fsimage/INodeDirectorySection/directory['
                               + str(i) + ']/child'))
    for j in range(1, num_child+1):
        # iNumber of the current child directory
        child_inum = tree.xpath('/fsimage/INodeDirectorySection/directory['
                                + str(i) + ']/child[' + str(j) + ']/text()')[0]
        # Match this child directory with its parent directory
        root.matchChildToParent(child_inum, parent_inum)


# Max. depth of directory tree
max_depth = root.maxDepth()


# A file can occupy more than one block,
# so the idea is to calculate the size for each individual file
# and then arrange the sizes into a list for comparison
lst = []
for i in range(1, num_file+1):
    # Sum up the numBytes
    file_size = int(tree.xpath('sum(/fsimage/INodeSection/inode[type = "FILE"]['
                               + str(i) + ']/blocks/block/numBytes)'))
    # Append the result to the list
    lst.append(file_size)


# Max. file size
max_size = max(lst)
# Min. file size
min_size = min(lst)


# Different outputs based on the number of files
if num_file == 0:
    data = {
        "number of files": num_file,
        "number of directories": num_dir,
        "maximum depth of directory tree": max_depth,
        }
else:
    data = {
        "number of files": num_file,
        "number of directories": num_dir,
        "maximum depth of directory tree": max_depth,
        "file size": {
            "max": max_size,
            "min": min_size
            }
        }


# Output a JSON file
with open(stats, "w") as outfile:
    json.dump(data, outfile)
