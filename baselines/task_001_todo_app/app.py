import json


def main() -> None:
    payload = {
        "app": "todo",
        "items": [],
    }
    print(json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    main()

