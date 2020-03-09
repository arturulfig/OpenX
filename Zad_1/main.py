class Node:
    def __init__(self, val):
        self.value = val
        self.children = []

class Calc:
    def count(self, node):
        value = 1
        for i in node.children:
            if len(i.children) > 0:
                value += self.count(i)
            else:
                value += 1
        return value

    def sum(self, node):
        val = node.value
        for j in node.children:
            if len(j.children) > 0:
                val += self.sum(j)
            else:
                val += j.value
        return val

    def avgValue(self, node):
       return self.sum(node) / self.count(node)

    def toList(self, node):
        list = [node.value]
        for k in node.children:
            if len(k.children) > 0:
                list.extend(self.toList(k))
            else:
                list.append(k.value)
        return list

    def median(self, node):
        ls = self.toList(node)
        ls.sort()
        if len(ls) % 2 == 0:
            return (ls[len(ls) // 2] + ls[len(ls) // 2 - 1]) / 2
        else:
            return ls[len(ls) // 2]

