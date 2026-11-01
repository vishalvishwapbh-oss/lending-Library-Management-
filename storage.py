import json
import os
from models import Book, Magazine, ReferenceBook
from models import StudentMember, FacultyMember, ResearchStudent, NotifiedMember


def save_data(manager):

    data = {
        "items": [],
        "members": [],
        "loans": manager.loans
    }

    for item in manager.items.values():

        if isinstance(item, Book):
            item_type = "Book"
        elif isinstance(item, Magazine):
            item_type = "Magazine"
        elif isinstance(item, ReferenceBook):
            item_type = "ReferenceBook"

        data["items"].append({
            "type": item_type,
            "item_id": item.item_id,
            "title": item.title,
            "available": item.available
        })

    for member in manager.members.values():

        if isinstance(member, ResearchStudent):
            member_type = "ResearchStudent"
        elif isinstance(member, StudentMember):
            member_type = "StudentMember"
        elif isinstance(member, FacultyMember):
            member_type = "FacultyMember"
        elif isinstance(member, NotifiedMember):
            member_type = "NotifiedMember"

        data["members"].append({
            "type": member_type,
            "member_id": member.member_id,
            "name": member.name,
            "borrowed_items": member.borrowed_items
        })

    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

    print("Data saved successfully.")


def load_data(manager):

    if not os.path.exists("data.json"):
        return

    try:
        with open("data.json", "r") as file:
            data = json.load(file)

        item_classes = {
            "Book": Book,
            "Magazine": Magazine,
            "ReferenceBook": ReferenceBook
        }

        member_classes = {
            "StudentMember": StudentMember,
            "FacultyMember": FacultyMember,
            "ResearchStudent": ResearchStudent,
            "NotifiedMember": NotifiedMember
        }

        for item_data in data["items"]:

            item_class = item_classes[item_data["type"]]

            item = item_class(
                item_data["item_id"],
                item_data["title"]
            )

            item.set_availability(item_data["available"])
            manager.items[item.item_id] = item

        for member_data in data["members"]:

            member_class = member_classes[member_data["type"]]

            member = member_class(
                member_data["member_id"],
                member_data["name"]
            )

            for item_id in member_data["borrowed_items"]:
                member.add_borrowed_item(item_id)

            manager.members[member.member_id] = member

        manager.loans = data["loans"]

        print("Data loaded successfully.")

    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        print("Error: Invalid data file.")