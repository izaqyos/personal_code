class Question:
    def __init__(self, text, ans) -> None:
        self.text = text
        self.ans = ans

    def __str__(self) -> str:
        return f"Question: {self.text}, answer {self.ans}"