command = "foo"

match command:
    case "quit":
        print("Exiting...")
    case "start":
        print("Starting...")
    case _:  # Default case
        print("Unknown command")
