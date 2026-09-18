from cli import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Error: KeyBoardInterrupt")
    except EOFError as e:
        print(f"Error: EndOfFileError {e}")
