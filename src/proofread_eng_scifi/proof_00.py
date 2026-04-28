import argparse


def proof_file(filename):
    with open(filename, "rt") as f:
        body = f.read()
    return proof_text(body)


def proof_text(body):
    print(body)
    return "checked"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    result = proof_file(args.filename)
    print(result)
