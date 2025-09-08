class Group:
    def __init__(self, elements, operation):
        self.elements = elements
        self.operation = operation
        self.order = len(elements)

    def identity(self):
        for e in self.elements:
            if all(self.operation(e, a) == a and self.operation(a, e) == a for a in self.elements):
                return e
        return None

    def inverse(self, a):
        for b in self.elements:
            if self.operation(a, b) == self.identity() and self.operation(b, a) == self.identity():
                return b
        return None

    def get_generator(self):
        """Find a generator of the group (only works for cyclic groups)"""
        for g in self.elements:
            generated = set()
            for i in range(1, self.order + 1):
                val = g
                for _ in range(i - 1):
                    val = self.operation(val, g)
                generated.add(val)
            if len(generated) == self.order:
                return g
        return None

    def pow(self, base, exponent):
        """A function to raise with the group's operation"""
        result = self.identity()
        for _ in range(exponent):
            result = self.operation(result, base)
        return result

    def show_structure(self):
        print("Group elements:", self.elements)
        print("Group order:", self.order)
        print("Identity element:", self.identity())
        print("Inverses:", {a: self.inverse(a) for a in self.elements})