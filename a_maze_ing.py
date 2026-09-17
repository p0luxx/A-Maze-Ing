from cli import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        print(e)
    except EOFError as e:
        print(e)
    except ValueError as e:
        print(f"Value error: {e}")
