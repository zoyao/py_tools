class CompanyInfoBase:
    def __init__(self, id, name, human, money, create, tel, email, address, base):
        index = 1
        for value in base:
            setattr(self, "a_" + str(index), value)
            index += 1
        self.id = id
        self.name = name
        self.human = human
        self.money = money
        self.create = create
        self.tel = tel
        self.email = email
        self.address = address

    def __eq__(self, other):
        if self.id == other.id:
            return True
        else:
            return False
