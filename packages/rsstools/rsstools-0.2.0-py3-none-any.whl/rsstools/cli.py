from rsstools.utils import add_entry, remove_entry, show_feed
from rsstools.feed_manager import FeedManager

def main_menu():
    print("Welcome to the RSS Feed Creator & Editor!")
    print("1. Create a new feed")
    print("2. Add an entry")
    print("3. Remove an entry")
    print("4. Edit feed metadata")
    print("5. Show current feed")
    print("6. Exit")

def create_feed_interactive():
    title = input("Enter feed title: ")
    link = input("Enter feed link: ")
    description = input("Enter feed description: ")
    fm = FeedManager()
    fm.create_feed(title, link, description)
    print("Feed created successfully!")

def add_entry_interactive():
    title = input("Enter entry title: ")
    link = input("Enter entry link: ")
    description = input("Enter entry description: ")
    add_entry(title, link, description)
    print(f"Entry '{title}' added successfully!")

def remove_entry_interactive():
    title = input("Enter the title of the entry to remove: ")
    remove_entry(title)
    print(f"Entry '{title}' removed successfully!")

def edit_metadata_interactive():
    title = input("Enter new feed title: ")
    link = input("Enter new feed link: ")
    description = input("Enter new feed description: ")
    fm = FeedManager()
    fm.edit_metadata(title, link, description)
    print("Feed metadata updated successfully!")

def show_feed_interactive():
    show_feed()

def main():
    while True:
        main_menu()
        choice = input("Choose an option (1-6): ")

        if choice == '1':
            create_feed_interactive()
        elif choice == '2':
            add_entry_interactive()
        elif choice == '3':
            remove_entry_interactive()
        elif choice == '4':
            edit_metadata_interactive()
        elif choice == '5':
            show_feed_interactive()
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid option, please try again :(")

if __name__ == '__main__':
    main()