from datetime import date, timedelta
from models import LibraryItem, Member, NotificationMixin

class LibraryManager:

    library_name = "My Library"
    fine_per_day = 5

    def __init__(self):
        self.items = {}
        self.members = {}
        self.loans = {}

    @classmethod
    def set_policy(cls, fine):
        cls.fine_per_day = fine

    @staticmethod
    def calculate_fine(overdue_days):
        return overdue_days * LibraryManager.fine_per_day

    def register_item(self, item):
        if item.item_id in self.items:
            print("Item ID already exists.")
            return

        self.items[item.item_id] = item
        print("Item registered successfully.")

    def register_member(self, member):
        if member.member_id in self.members:
            print("Member ID already exists.")
            return

        self.members[member.member_id] = member
        print("Member registered successfully.")

    def borrow_item(self, member_id, item_id):

        if member_id not in self.members:
            print("Member not found.")
            return

        if item_id not in self.items:
            print("Item not found.")
            return

        member = self.members[member_id]
        item = self.items[item_id]

        if not item.available:
            print("Item is not available.")
            return

        if item.loan_period_days() <= 0:
            print("This item cannot be borrowed.")
            return

        if not member.can_borrow():
            print("Borrowing limit exceeded.")
            return

        issue_date = date.today()
        due_date = issue_date + timedelta(days=item.loan_period_days())

        item.set_availability(False)
        member.add_borrowed_item(item_id)

        self.loans[item_id] = {
            "member_id": member_id,
            "issue_date": str(issue_date),
            "due_date": str(due_date)
        }

        print("Borrow successful:", item_id, "issued to", member_id)
        print("Due date:", due_date)

        if isinstance(member, NotificationMixin):
            member.send_notice("Item borrowed successfully: " + item.title)

    def return_item(self, member_id, item_id):

        if item_id not in self.loans:
            print("No active loan found.")
            return

        loan = self.loans[item_id]

        if loan["member_id"] != member_id:
            print("This item was not borrowed by this member.")
            return

        item = self.items[item_id]
        member = self.members[member_id]

        due_date = date.fromisoformat(loan["due_date"])
        return_date = date.today()

        overdue_days = max(0, (return_date - due_date).days)
        fine = self.calculate_fine(overdue_days)

        item.set_availability(True)
        member.remove_borrowed_item(item_id)

        del self.loans[item_id]

        print("Item returned successfully.")
        print("Overdue days:", overdue_days)
        print("Fine:", fine)

    def show_all_items(self):

        for item in self.items.values():
            print(item.item_id, item.title, item.available)

    def show_available_items(self):

        for item in self.items.values():
            if item.available:
                print(item.item_id, item.title)

    def show_active_loans(self):

        for item_id, loan in self.loans.items():
            print(
                item_id,
                loan["member_id"],
                "Due:",
                loan["due_date"]
            )

    def show_overdue_loans(self):

        today = date.today()

        for item_id, loan in self.loans.items():
            due_date = date.fromisoformat(loan["due_date"])

            if today > due_date:
                overdue_days = (today - due_date).days
                print(item_id, "Overdue days:", overdue_days)

    def show_member_report(self):

        for member in self.members.values():
            print(
                member.member_id,
                member.name,
                "Borrowed items:",
                len(member.borrowed_items)
            )