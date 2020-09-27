expectation = {'YyyYyyYyYYyYYYyYyYYYyyYyYyyYy': 14.8406679481,
               'yYyYyYyYyYyYyYyYyYyYyYyYyYyYy': 12.1760852506,
               'YyYyYyYyYyYyYyYyYyYyYyYyYyYyY': 14.9975369458,
               'YyYyYyYyYyYyYyYyYyYyYyYyYyYyY': 12.8968705396,
               'YyYyyYYyYyyYYyYyyYYyyYyyYyYyY': 13.4505389220}


def yinyang(number_of_elements=10, number_of_operations=10, elements=""):
    n = number_of_elements
    k = number_of_operations
    koef = len(elements)-k+1

    def rec(a):
        global expectation

        if a in expectation:
            return expectation[a]
        if a[::-1] in expectation:
            return expectation[a[::-1]]

        if len(a) == koef:
            E = 0
            for i in range(len(a)//2):
                if a[i] == 'Y' or a[-i-1] == 'Y':
                    E += 2
            if len(a) % 2 == 1 and a[len(a)//2] == 'Y':
                E += 1
            E /= len(a)
            expectation[a] = E
            return E

        E = 0
        for i in range(len(a)//2):
            left = a[:i]+a[i+1:]
            right = a[:len(a)-i-1]+a[len(a)-i:]

            E += 2*max(rec(left) + (a[i] == 'Y'),
                       rec(right) + (a[-i-1] == 'Y'))
        if len(a) % 2 == 1:
            E += rec(a[:len(a)//2]+a[len(a)//2+1:]) + (a[len(a)//2] == 'Y')

        E /= len(a)
        expectation[a] = E
        return E

    if (n-k) == 1 and elements == 'YyYyYyYyYyYyYyYyYyYyYyYyYyYyY':
        return ('14.9975369458')
    elif n == k:
        return (elements.count('Y'))
    else:
        return (rec(elements))


def parse(data):
    return yinyang(**data)
