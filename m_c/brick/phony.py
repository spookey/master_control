from m_c.brick.basic import Basic


class Phony(Basic):
    def full(self):
        return True

    def null(self):
        return True
