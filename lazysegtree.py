def ceil_pow2(n):
    x = 0
    while((1 << x) < n):
        x += 1
    return x


class lazysegtree:
    def __init__(self, op, e, mapping, composition, id, n=0, ary=[]) -> None:
        self.op = op
        self.e = e
        self.mapping = mapping
        self.composition = composition
        self.id = id
        
        if n:
            ary = [e()] * n
        else:
            n = len(ary)
        
        self.n = n

        self.log = ceil_pow2(n)
        self.size = 1 << self.log
        self.d = [e()] * (2 * self.size)
        self.lz = [id()] * (2 * self.size)

        for i in range(self.n):
            self.d[self.size + i] = ary[i]
        for i in range(self.size - 1, 0, -1):
            self.update(i)
    
    def set(self, p, x):
        assert(0 <= p < self.n)
        p += self.size
        for i in range(self.log, 0, -1):
            self.push(p >> i)
        self.d[p] = x
        for i in range(1, self.log + 1):
            self.updte(p >> i)
    
    def get(self, p):
        assert(0 <= p < self.n)
        p += self.size
        for i in range(self.log, 0, -1):
            self.push(p >> i)
        return self.d[p]
    
    def prod(self, l, r):
        assert(0 <= l <= r <= self.n)
        if l == r:
            return self.e()
        
        l += self.size
        r += self.size

        msk = 2
        for i in range(self.log, 0, -1):
            if (l & (msk - 1)) != 0:
                self.push(l >> i)
            if (r & (msk - 1)) != 0:
                self.push((r - 1) >> i)
            msk <<= 1
        
        sml = self.e()
        smr = self.e()

        while l < r:
            if l & 1:
                sml = self.op(sml, self.d[l])
                l += 1
            if r & 1:
                r -= 1
                smr = self.op(self.d[r], smr)
            l >>= 1
            r >>= 1
        
        return self.op(sml, smr)

    def all_prod(self):
        return self.d[1]
    
    # def apply(self, p, f):
    #     assert(0 <= p < self.n)
    #     p += self.size
    #     for i in reversed(range(1, self.log + 1)):
    #         self.push(p >> i)
    #     self.d[p] = self.mapping(f, self.d[p])
    #     for i in range(1, self.log + 1):
    #         self.update(p >> i)
    def apply(self, *args):
        if len(args) == 2:
            p, f = args
            assert(0 <= p < self.n)
            p += self.size
            for i in range(self.log, 0, -1):
                self.push(p >> i)
            self.d[p] = self.mapping(f, self.d[p])
            for i in range(1, self.log + 1):
                self.update(p >> i)
        elif len(args) == 3:
            l, r, f = args
            assert(0 <= l <= r <= self.n)
            if l == r:
                return
            
            l += self.size
            r += self.size

            msk = 2
            for i in range(self.log, 0, -1):
                # if ((l >> i) << i) != l:
                #     self.push(l >> i)
                # if ((r >> i) << i) != r:
                #     self.push((r - 1) >> i)
                if (l & (msk - 1)) != 0:
                    self.push(l >> i)
                if (r & (msk - 1)) != 0:
                    self.push((r - 1) >> i)
                msk <<= 1
            
            l2 = l
            r2 = r
            while l < r:
                if l & 1:
                    self.all_apply(l, f)
                    l += 1
                if r & 1:
                    r -= 1
                    self.all_apply(r, f)
                l >>= 1
                r >>= 1
            l = l2
            r = r2

            msk = 2
            for i in range(1, self.log + 1):
                # if ((l >> i) << i) != l:
                #     self.update(l >> i)
                # if ((r >> i) << i) != r:
                #     self.update((r - 1) >> i)
                if (l & (msk - 1)) != 0:
                    self.update(l >> i)
                if (r & (msk - 1)) != 0:
                    self.update((r - 1) >> i)
                msk <<= 1

    def update(self, p):
        self.d[p] = self.op(self.d[p * 2], self.d[p * 2 + 1])
    
    def all_apply(self, k, f):
        self.d[k] = self.mapping(f, self.d[k])
        if k < self.size:
            self.lz[k] = self.composition(f, self.lz[k])
    
    def push(self, p):
        self.all_apply(p * 2, self.lz[p])
        self.all_apply(p * 2 + 1, self.lz[p])
        self.lz[p] = self.id()


# solve nikkei2019-2-qual D
class Query:
    def __init__(self, l, r, c):
        self.l = l
        self.r = r
        self.c = c

inf = 10**18
op = lambda x, y: min(x, y)
e = lambda: inf
mapping = lambda f, x: min(x, f)
composition = lambda f, g: min(f, g)
id = lambda: inf

def solve():
    n, m = map(int, input().split())
    a = [Query(*map(int, input().split())) for _ in range(m)]
    a.sort(key=lambda x: x.l)

    d = [inf - 1] * n
    d[0] = 0
    seg = lazysegtree(op, e, mapping, composition, id, ary=d)

    for i in range(m):
        cur = seg.prod(a[i].l - 1, a[i].r)
        seg.apply(a[i].l - 1, a[i].r, cur + a[i].c)
    
    ans = seg.prod(n - 1, n)
    print(ans if ans != inf - 1 else -1)

solve()