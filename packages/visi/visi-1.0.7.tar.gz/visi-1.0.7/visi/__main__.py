import argparse

def main():
    # parse args
    parser = argparse.ArgumentParser(description="A CLI for the visi app")
    parser.add_argument("name", help="Your name")
    args = parser.parse_args()