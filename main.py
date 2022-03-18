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
        for i in range(len(alldegrees)):
            if alldegrees[i] != i:
                raise ValueError("Cannot skip degrees")

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
        raise NotImplementedError("TODO")

    def __add__(self, other):
        new = Polynomial(self.terms)
        for term in other.terms:
            new.append(term)
        return new

    def __sub__(self, other):
        raise NotImplementedError("TODO")

    def __getitem__(self, item):
        raise NotImplementedError("TODO")

    def __contains__(self, item):
        raise NotImplementedError("TODO")

    def __eq__(self, other):
        raise NotImplementedError("TODO")

    def __iter__(self):
        raise NotImplementedError("TODO")

    def __len__(self):
        raise NotImplementedError("TODO")

    def append(self, term):
        if term.exp > self.degree + 1:
            raise ValueError("Cannot skip degrees")

        for selfterm in self.terms:
            if selfterm.exp == term.exp:
                new_coeff = selfterm.coeff + term.coeff
                new_term = Term(new_coeff, selfterm.var, selfterm.exp)

                i = self.terms.index(selfterm)
                self.terms = self.terms[:i]+[new_term]+self.terms[i+1:]
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


test_term = Term(-3, "x")
term_2 = Term(2, "x", 2)
term_4 = Term(4, 'x', 2)
term_3 = Term(4)

polynomial = Polynomial([test_term, term_2, term_3, term_4])
print(polynomial)
print(f"Degree: {polynomial.degree}, L.C: {polynomial.lc}")

polynomial.append(Term(2, 'x', 2))
polynomial.append(Term(3, 'x', 3))
polynomial.append(Term(3))

print(polynomial)
print(f"Degree: {polynomial.degree}, L.C: {polynomial.lc}")

tpoly1 = Polynomial([Term(2, 'x', 3), Term(-3, 'x', 2), Term(4, 'x'), Term(2)])
print(tpoly1)

added = polynomial + tpoly1
print(added)
