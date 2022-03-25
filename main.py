def super_num(num_list):
    super_s = ["⁰", "¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
    if len(num_list) == 1:
        if 0 in num_list or 1 in num_list:
            return ""
    return "".join([super_s[a] for a in num_list])


class Term:
    def __init__(self, coeff, var="", exp=0):
        self.coeff = coeff
        self.var = var
        self.exp = exp

        if self.exp == 0 and var != "":
            self.exp = 1

    def __str__(self):
        exp_lst = [int(a) for a in str(self.exp)]
        return f"{self.coeff}{self.var}{super_num(exp_lst)}"

    def __repr__(self):
        exp_lst = [int(a) for a in str(self.exp)]
        return f"Term({self.coeff}{self.var}{super_num(exp_lst)})"

    def __eq__(self, other):
        if self.coeff == other.coeff:
            if self.exp == other.exp:
                if self.var == other.var:
                    return True
        return False

    def __mul__(self, other):
        new_coeff = self.coeff * other.coeff
        new_exp = self.exp + other.exp
        return Term(new_coeff, self.var, new_exp)

    def __truediv__(self,other):
        return Term(self.coeff / other.coeff, self.var, self.exp - other.exp)


class Polynomial:
    def __init__(self, terms):
        self.degree = 0

        alldegrees = []

        for term in terms:
            if term.exp not in alldegrees:
                alldegrees.append(term.exp)
            if term.exp > self.degree:
                self.degree = term.exp
                self.lc = term.coeff

        alldegrees.sort()

        terms_dict = {}
        for term in terms:
            if term.exp not in terms_dict.keys():
                terms_dict[term.exp] = term
            else:
                terms_dict[term.exp] = [term, terms_dict[term.exp]]
        sorted_terms = dict(sorted(terms_dict.items(), reverse=True))

        for k, v in sorted_terms.items():
            if type(v) == list:
                new_coeff = 0
                for term in v:
                    new_coeff += term.coeff
                term_var = v[0].var
                new_term = Term(new_coeff, term_var, k)
                sorted_terms[k] = new_term

        self.terms = []
        for v in sorted_terms.values():
            self.terms.append(v)
        self.numItems = len(self.terms)

        self.degree = self.terms[0].exp
        self.lc = self.terms[0].coeff

    def __str__(self):
        return " + ".join([str(a) for a in self.terms])

    def __repr__(self):
        return "Polynomial(" + " + ".join([str(a) for a in self.terms]) + ")"

    def __mul__(self, other):
        new = Polynomial([Term(0),Term(0,'x')])
        for selfTerm in self.terms:
            for otherTerm in other.terms:
                new.add_term(otherTerm * selfTerm)
        return new

    def __truediv__(self, other):
        if len(other) == 2:
            if other[0].exp == 1 and other[0].coeff == 1:
                if other[1].exp == 0 and other[1].var == "":
                    # Do synthetic division if the equation is in the form P(x) / x-a
                    return self._synth_div(other, return_remainder=False)

        # Do regular division if the equation is not in the form P(x) / x-a

        raise NotImplementedError("Can only do synthetic division")

    def __add__(self, other):
        new = Polynomial(self.terms)
        for term in other.terms:
            new.add_term(term)
        return new

    def __sub__(self, other):
        distributed = []
        for term in other.terms:
            new_coeff = term.coeff * -1
            new_term = Term(new_coeff, term.var, term.exp)
            distributed.append(new_term)
        distributed_poly = Polynomial(distributed)
        return self + distributed_poly

    def __getitem__(self, index):
        return self.terms[index]

    def __setitem__(self, key, value):
        raise NotImplementedError("TODO")

    def __delitem__(self, key):
        term = self.terms[key]
        if term.exp != self.degree and term.exp != 0:
            raise ValueError("Cannot delete a middle degree")
        self.terms.pop(key)
        self.numItems -= 1

    def __contains__(self, item):
        for term in self.terms:
            if term == item:
                return True
        return False

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        for i in range(len(self.terms)):
            if self[i] != other[i]:
                return False
        return True

    def __iter__(self):
        for term in self.terms:
            yield term

    def __len__(self):
        return self.numItems

    def _synth_div(self, other, return_remainder=True):
        if other[1].coeff < 1:
            multiplier = abs(other[1].coeff)
        else:
            multiplier = other[1].coeff * -1
        coeffs = [term.coeff for term in self.terms]
        final = [coeffs[0]]
        coeffs.pop(0)

        final.append((i + (final[-1] * multiplier)) for i in coeffs)

        newDeg = self.degree - 1
        remainder = final[-1]
        final.pop(-1)

        newTerms = []
        for i in final:
            if newDeg != 0:
                newTerms.append(Term(i, 'x', newDeg))
                newDeg -= 1
            else:
                newTerms.append(Term(i))

        newPoly = Polynomial(newTerms)
        if return_remainder:
            return newPoly, remainder
        else:
            return newPoly

    def add_term(self, term):
        for selfterm in self.terms:
            if selfterm.exp == term.exp:
                new_coeff = selfterm.coeff + term.coeff
                new_term = Term(new_coeff, selfterm.var, selfterm.exp)

                i = self.terms.index(selfterm)
                self.terms = self.terms[:i] + [new_term] + self.terms[i + 1:]
                if i == 0:
                    self.lc = new_term.coeff
                return

        for i in self.terms:
            if i.exp < term.exp:
                self.terms.insert(self.terms.index(i), term)
                if self.terms.index(i) == 1:
                    self.degree = term.exp
                    self.lc = term.coeff
                self.numItems += 1
                return

    def is_factor(self, other):
        if len(other) == 2:
            if other[0].exp == 1 and other[0].coeff == 1:
                if other[1].exp == 0 and other[1].var == "":
                    _, remainder = self._synth_div(other, return_remainder=True)
                    if remainder == 0:
                        return True
                    return False
        raise NotImplementedError("Can only perform synthetic division")


"""
Testing code below this line


test_term = Term(-3, "x")
term_2 = Term(2, "x", 2)
term_4 = Term(4, 'x', 2)
term_3 = Term(4)

polynomial = Polynomial([test_term, term_2, term_3, term_4])
print(polynomial)
print(f"Degree: {polynomial.degree}, L.C: {polynomial.lc}")

polynomial.add_term(Term(2, 'x', 2))
polynomial.add_term(Term(3, 'x', 3))
polynomial.add_term(Term(3))

print(polynomial)
print(f"Degree: {polynomial.degree}, L.C: {polynomial.lc}")

tpoly1 = Polynomial([Term(2, 'x', 3), Term(-3, 'x', 2), Term(4, 'x'), Term(2)])
print(tpoly1)

added = polynomial + tpoly1
print(added)

copy_term = Term(2, 'x', 2)
if copy_term == term_2:
    print("Test 1 passed")
else:
    print("Test 1 failed")

if Term(5, 'x', 3) in added:
    print("Test 2 passed")
else:
    print("Test 2 failed")

print(polynomial)
print(tpoly1)
subbed = polynomial - tpoly1
print(subbed)

copy_poly = Polynomial(polynomial.terms)
print(copy_poly[0])
if polynomial == copy_poly:
    print("Test 3 passed")
else:
    print("Test 3 failed")

if polynomial != tpoly1:
    print("Test 4 passed")
else:
    print("Test 4 failed")

for term in polynomial:
    print(term)

tpoly2 = Polynomial([Term(-3, 'x', 2), Term(4, 'x'), Term(2)])
del tpoly1[0]
if tpoly1 == tpoly2:
    print("Test 5 passed")
else:
    print("Test 5 failed")
"""

div1 = Polynomial([Term(1, 'x', 3), Term(-2, 'x', 2), Term(-14, 'x'), Term(-3)])
div2 = Polynomial([Term(1, 'x'), Term(3)])
print(div1/div2)
print(div1.is_factor(div2))

print("\n")

#Starting my tests
tpoly3 = Polynomial([Term(2,'x'),Term(2)])
tpoly4 = Polynomial([Term(3,'x'),Term(3)])
tpoly5 = Polynomial([Term(6,'x',2),Term(12,'x'),Term(6)])
print(tpoly3*tpoly4)
if tpoly3 * tpoly4 == tpoly5:
	print("Test 6 passed")


print(Term(3, 'x', 2)*Term(-4, 'x', 3))
