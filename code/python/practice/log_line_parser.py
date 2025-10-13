import re
def parse_log_lines(lines: list[str]) -> list[dict]:
    """
    Parse lines in the form: "[LEVEL] YYYY-MM-DD HH:MM:SS - module: message"
    Return list of dicts with keys: "level", "timestamp" (ISO "YYYY-MM-DDT HH:MM:SS"), "module", "message".
    Rules:
      - Trim whitespace
      - Ignore lines that don't match the format
      - Convert "YYYY-MM-DD HH:MM:SS" to "YYYY-MM-DDTHH:MM:SS"
    """
    # TODO: implement
    ret = list()
    pattern = re.compile(
    r'^\[(?P<level>\w+)\] '
    r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - '
    r'(?P<module>\w+): '
    r'(?P<message>.*)$'
    )

    for line in lines:
        match = pattern.match(line)
        if match:
            ret.append({
                'level': match.group('level'),
                'timestamp': match.group('timestamp').replace(' ', 'T'),
                'module': match.group('module'),
                'message': match.group('message')
            })

    return ret


if __name__ == "__main__":
    sample = [
        "[INFO] 2025-03-01 09:15:00 - auth: User login ok",
        "garbage line",
        "[ERROR] 2025-03-01 09:16:00 - db: failed to connect",
    ]
    got = parse_log_lines(sample)
    expected = [
        {"level": "INFO", "timestamp": "2025-03-01T09:15:00", "module": "auth", "message": "User login ok"},
        {"level": "ERROR", "timestamp": "2025-03-01T09:16:00", "module": "db", "message": "failed to connect"},
    ]
    print(got)
    assert got == expected, f"Unexpected parsed logs: {got}"
    print("QOTD #2 OK")
