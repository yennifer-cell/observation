
class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class SingleLinkedList:
    def __init__(self):
        self.start = None
        self.last = None

    def append(self, value):
        newNode = Node(value)  

        if not self.start:
            self.start = newNode
            self.last = newNode
            return newNode

        lastNode = self.last  
        lastNode.next = newNode  
        self.last = newNode
        return self.last

    def print_all_nodes(self):
        # list all items from the start
        currentNode = self.start  

        if not currentNode:
            print("Our list is empty")
            return

        while True:
            print("Current node is")
            print(currentNode.__dict__)

            if not currentNode.next:
                print("Found the last node")
                return

            currentNode = currentNode.next  


myList = SingleLinkedList()
#myList.print_all_nodes()
myList.append(45)
myList.append(99)
myList.append(134)
myList.print_all_nodes()
