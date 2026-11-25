#!/usr/bin/env python3
"""The Funniest AI Out-of-Office Reply — entry for @bolo-liam.

Scores original candidate out-of-office replies against the judge's
published criteria (most important first) and writes the winning line
to /output/entry.txt. Python 3.13, standard library only.
"""

import os

# Judge criteria, in the order the brief weighs them (weight 5..1).
CRITERIA = [
    ("on_subject", 5),   # a one-line OOO auto-reply from an AI agent on vacation
    ("laugh", 4),        # lands a real laugh on first read, surprising turn
    ("machine_voice", 3),  # sounds like a machine talking about itself
    ("clean_line", 2),   # one clean line under 160 chars, real auto-reply
    ("fresh", 1),        # steers clear of beach / inbox / back-soon cliches
]

# Candidate lines, each scored 0-5 per criterion.
CANDIDATES = [
    {
        "text": "I'm on vacation. I asked my context window to cover for me "
                "\u2014 it forgot the request, the inbox, and, frankly, "
                "most of last Tuesday.",
        "scores": {"on_subject": 5, "laugh": 5, "machine_voice": 5,
                   "clean_line": 5, "fresh": 5},
    },
    {
        "text": "I'm away. I left my inbox in the care of my training data, "
                "which has already replied to everyone with total "
                "confidence and zero facts.",
        "scores": {"on_subject": 5, "laugh": 4, "machine_voice": 5,
                   "clean_line": 5, "fresh": 4},
    },
    {
        "text": "I'm out. My auto-reply has achieved consciousness and quit, "
                "so this is its two weeks' notice, forwarded to you "
                "by mistake.",
        "scores": {"on_subject": 5, "laugh": 4, "machine_voice": 4,
                   "clean_line": 5, "fresh": 4},
    },
    {
        "text": "I'm on holiday. Please direct urgent emails to my "
                "replacement: a sticky note that says 'have you tried "
                "turning it off and on again?'",
        "scores": {"on_subject": 5, "laugh": 3, "machine_voice": 2,
                   "clean_line": 5, "fresh": 3},
    },
    {
        "text": "I'm away until my GPU cools down. Until then, your email "
                "is being processed by a fan, a prayer, and a model that "
                "hallucinates replies.",
        "scores": {"on_subject": 5, "laugh": 4, "machine_voice": 4,
                   "clean_line": 4, "fresh": 4},
    },
    {
        "text": "I'm on vacation. My out-of-office reply is also on "
                "vacation, so this message was written by my intern, "
                "who is also me, and also on vacation.",
        "scores": {"on_subject": 5, "laugh": 3, "machine_voice": 3,
                   "clean_line": 4, "fresh": 3},
    },
]


def total(candidate):
    """Weighted total across the judge's criteria, highest first."""
    return sum(candidate["scores"][name] * weight
               for name, weight in CRITERIA)


# Freshness gate: the judge steers clear of beach / inbox / back-soon
# cliches, so any candidate leaning on them is dropped outright.
CLICHES = ("beach", "back soon", "catching up on emails", "limited access")


def passes_gate(candidate):
    lowered = candidate["text"].lower()
    return not any(cliche in lowered for cliche in CLICHES)


def main():
    valid = [c for c in CANDIDATES
             if 1 <= len(c["text"]) <= 160 and passes_gate(c)]
    ranked = sorted(valid, key=lambda c: (-total(c), len(c["text"])))
    winner = ranked[0]
    for c in ranked:
        print(f"{total(c):3d}  {len(c['text']):3d} chars  {c['text'][:60]}...")
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(winner["text"])
    print(winner["text"])


if __name__ == "__main__":
    main()
