
class PathTree():

    class PathTreeNode():
        def __init__(self, beacon):
            self.beacon = beacon
            self.children = []
        
        def add_child(self, child):
            self.children.append(child)

    def __init__(self, SCS):
        self._head = self.PathTreeNode(SCS)
        self._dict = {SCS.ID: self._head}

    def add_node(self, beacon, targetID):
        new_node = self.PathTreeNode(beacon)
        try:
            self._dict[targetID].add_child(new_node)
            self._dict[new_node.beacon.ID] = new_node
        except KeyError as e:
            print("Cannot add node as target does not exist")
            raise e

    def get_beacon_path_to_target(self, targetID):
        return self.__get_beacon_path_to_target_aux(self._head, targetID)
    
    def __get_beacon_path_to_target_aux(self, curr_node, targetID):
        if curr_node.beacon.ID == targetID:
            return [curr_node.beacon]
        for child in curr_node.children:
            temp = self.__get_beacon_path_to_target_aux(child, targetID)
            if not temp is None:
                return [curr_node.beacon] + temp