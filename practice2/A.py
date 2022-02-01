import sys
sys.setrecursionlimit(1 << 20)

class dsu :
    def __init__(self, n = 0) -> None:
        self.__n = n
        self.__parentOrSize = [-1 for _ in range(n)]
    
    def merge(self, a, b) -> int:
        assert 0 <= a and a < self.__n
        assert 0 <= b and b < self.__n
        x = self.leader(a)
        y = self.leader(b)
        if x == y:
            return x
        if -self.__parentOrSize[x] < -self.__parentOrSize[y]:
            x, y = y, x
        self.__parentOrSize[x] += self.__parentOrSize[y]
        self.__parentOrSize[y] = x
        return x
    
    def same(self, a, b) -> bool:
        assert 0 <= a and a < self.__n
        assert 0 <= b and b < self.__n
        return self.leader(a) == self.leader(b)
    
    def leader(self, a) -> int:
        assert 0 <= a and a < self.__n
        if self.__parentOrSize[a] < 0:
            return a
        self.__parentOrSize[a] = self.leader(self.__parentOrSize[a])
        return self.__parentOrSize[a]
    
    def size(self, a) -> int:
        assert 0 <= a and a < self.__n
        return -self.__parentOrSize[self.leader(a)]
    
    def groups(self):
        leader_buf = [self.leader(i) for i in range(self.__n)]
        result = [[] for _ in range(self.__n)]
        for i in range(self.__n):
            result[leader_buf[i]].append(i)
        return [elm for elm in result if len(elm)]

n, q = map(int, input().split())

d = dsu(n)

for _ in range(q):
    t, u, v = map(int, input().split())
    if t:
        print(1 if d.same(u, v) else 0)
    else:
        d.merge(u, v)
