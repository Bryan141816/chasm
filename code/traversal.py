from collections import deque
class Traversal:
    def __init__(self):
        pass
    def bfs_traversal(self, root):
        result = []
        if not root:
            return result

        queue = deque([root])

        while queue:
            node = queue.popleft()
            result.append(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        return result

    # Depth-first search (DFS) - Pre-order
    def dfs_preorder(self, root):
        result = []
        def dfs(node):
            if not node:
                return
            result.append(node.val)
            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return result

    # Depth-first search (DFS) - In-order
    def dfs_inorder(self, root):
        result = []
        def dfs(node):
            if not node:
                return
            dfs(node.left)
            result.append(node.val)
            dfs(node.right)

        dfs(root)
        return result

    # Depth-first search (DFS) - Post-order
    def dfs_postorder(self, root):
        result = []
        def dfs(node):
            if not node:
                return
            dfs(node.left)
            dfs(node.right)
            result.append(node.val)

        dfs(root)
        return result