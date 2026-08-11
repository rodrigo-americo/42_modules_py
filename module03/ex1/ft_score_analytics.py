import sys


def main() -> None:
    score_valid: list[int] = []
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            try:
                score_valid = score_valid + [int(arg)]
            except ValueError:
                print(f"Invalid parameter: '{arg}'")
    if (len(score_valid) > 0):
        print(f"Scores processed: {score_valid}")
        print(f"Total players: {len(score_valid)}")
        print(f"Total score: {sum(score_valid)}")
        print(f"Average score: {sum(score_valid)/len(score_valid)}")
        print(f"High score: {max(score_valid)}")
        print(f"Low score: {min(score_valid)}")
        print(f"Score range: {max(score_valid) - min(score_valid)}")
    else:
        print("No scores provided. "
              "Usage: python3 ft_score_analytics.py <score1> <score2> ...")
    return


if __name__ == "__main__":
    print("=== Player Score Analytics ===")
    main()
