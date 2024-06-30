from query import query_eq

if __name__ == "__main__":
    from pathlib import Path
    DIR = Path(__file__).parent
    test = DIR / "test" / "test.typ"
    print(query_eq(test))
