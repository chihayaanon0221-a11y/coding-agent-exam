def parse_index(raw_index, tasks):
    if raw_index is None:
        print("Error: Missing index.")
        return None
    if not raw_index.isdigit():
        print("Error: Index must be a number.")
        return None

    index = int(raw_index)
    if index < 1 or index > len(tasks):
        print("Error: Index out of range.")
        return None
    return index - 1


def print_tasks(tasks):
    if not tasks:
        print("No tasks.")
        return

    for index, task in enumerate(tasks, start=1):
        marker = "[x]" if task["done"] else "[ ]"
        print(f"{index}. {marker} {task['title']}")


def main() -> None:
    tasks = []

    while True:
        try:
            line = input("> ").strip()
        except EOFError:
            break

        if not line:
            print("Error: Invalid command.")
            continue

        command, _, argument = line.partition(" ")

        if command == "add":
            title = argument.strip()
            if not title:
                print("Error: Missing task title.")
                continue
            tasks.append({"title": title, "done": False})
        elif command == "list":
            if argument.strip():
                print("Error: Invalid command.")
                continue
            print_tasks(tasks)
        elif command == "done":
            task_index = parse_index(argument.strip() or None, tasks)
            if task_index is not None:
                tasks[task_index]["done"] = True
        elif command == "delete":
            task_index = parse_index(argument.strip() or None, tasks)
            if task_index is not None:
                del tasks[task_index]
        elif command == "quit":
            if argument.strip():
                print("Error: Invalid command.")
                continue
            break
        else:
            print("Error: Invalid command.")


if __name__ == "__main__":
    main()
