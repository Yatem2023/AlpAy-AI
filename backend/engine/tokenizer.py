"""
AlpAy Engine Tokenizer
Version: 0.1
"""

import re


class Tokenizer:
    """
    Basit regex tabanlı tokenizer.
    """

    TOKEN_PATTERN = re.compile(
        r"\w+|[^\w\s]",
        flags=re.UNICODE
    )

    def tokenize(self, text: str) -> list[str]:
        """
        Metni tokenlara ayırır.
        """

        text = text.strip()

        if not text:
            return []

        return self.TOKEN_PATTERN.findall(text)

    def detokenize(self, tokens: list[str]) -> str:
        """
        Token listesini tekrar metne çevirir.
        """

        if not tokens:
            return ""

        text = ""

        for token in tokens:

            if token in ",.!?:;)]}":
                text += token

            elif text == "":
                text += token

            elif token in "([{":
                text += " " + token

            else:
                text += " " + token

        return text.strip()


if __name__ == "__main__":

    tokenizer = Tokenizer()

    sample = "Merhaba! Ben AlpAy AI'yım :)"

    tokens = tokenizer.tokenize(sample)

    print(tokens)

    print(tokenizer.detokenize(tokens))