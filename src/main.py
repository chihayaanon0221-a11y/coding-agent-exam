import json


def main() -> None:
    payload = {"status": "ok"}
    print(json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    main()

