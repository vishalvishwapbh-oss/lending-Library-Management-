from abc import ABC, abstractmethod


class LibraryItem(ABC):

    def __init__(self, item_id, title):
        self._item_id = item_id
        self._title = title
        self._available = True

    @property
    def item_id(self):
        return self._item_id

    @property
    def title(self):
        return self._title

    @property
    def available(self):
        return self._available

    def set_availability(self, status):
        self._available = status

    @abstractmethod
    def loan_period_days(self):
        pass


class Book(LibraryItem):

    def loan_period_days(self):
        return 14


class Magazine(LibraryItem):

    def loan_period_days(self):
        return 7


class ReferenceBook(LibraryItem):

    def loan_period_days(self):
        return 0


class Member:

    def __init__(self, member_id, name, borrowing_limit):
        self._member_id = member_id
        self._name = name
        self._borrowing_limit = borrowing_limit
        self._borrowed_items = []

    @property
    def member_id(self):
        return self._member_id

    @property
    def name(self):
        return self._name

    @property
    def borrowing_limit(self):
        return self._borrowing_limit

    @property
    def borrowed_items(self):
        return self._borrowed_items.copy()

    def add_borrowed_item(self, item_id):
        self._borrowed_items.append(item_id)

    def remove_borrowed_item(self, item_id):
        if item_id in self._borrowed_items:
            self._borrowed_items.remove(item_id)

    def can_borrow(self):
        return len(self._borrowed_items) < self._borrowing_limit


class StudentMember(Member):

    def __init__(self, member_id, name):
        super().__init__(member_id, name, 3)


class FacultyMember(Member):

    def __init__(self, member_id, name):
        super().__init__(member_id, name, 5)


class ResearchStudent(StudentMember):

    def __init__(self, member_id, name):
        super().__init__(member_id, name)
        self._borrowing_limit = 5


class NotificationMixin:

    def send_notice(self, message):
        print("Notification:", message)

class NotifiedMember(Member, NotificationMixin):

    def __init__(self, member_id, name, borrowing_limit):
        super().__init__(member_id, name, borrowing_limit)


if __name__ == "__main__":

    book = Book("B101", "Python Programming")
    magazine = Magazine("M101", "Science Monthly")
    reference = ReferenceBook("R101", "Encyclopedia")

    items = [book, magazine, reference]

    for item in items:
        print(item.item_id, item.title, item.available, item.loan_period_days())

    student = StudentMember("S101", "Aman")
    faculty = FacultyMember("F101", "Riya")
    researcher = ResearchStudent("RS101", "Rahul")

    members = [student, faculty, researcher]

    for member in members:
        print(member.member_id, member.name, member.borrowing_limit)

    notified = NotifiedMember("N101", "Priya", 3)
    notified.send_notice("Welcome to Library!")