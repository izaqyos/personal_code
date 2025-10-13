from turtle import Turtle
import os

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.scoresfile = 'snake_scores'
        self._loadhighscore()
        self.score = 0
        self.game_over_msg = "Game Over :("
        self.score_msg = "Score: "
        self.highscore_msg = "Highscore: "
        self.text_color = "white"
        self.color( self.text_color)
        self.penup()
        self.hideturtle()
        self._resetText()

    def _loadhighscore(self):
        if os.path.exists(self.scoresfile):
            with open(self.scoresfile, 'r') as inpfile:
                highscore  = inpfile.read()
                if highscore:
                    self.highscore = int(highscore)
                else:
                    self.highscore = 0
        else:
            self.highscore = 0

    def _resetText(self):
        self.clear()
        self.goto(-70, +280)

    def updateScore(self, add_points):
        self.score += add_points
        print(f"Scoreboard::updateScore(), new score {self.score}")

    def getScoreMsg(self):
        return f"{self.score_msg} {self.score}    {self.highscore_msg} {self.highscore}"

    def writeText(self):
        self._resetText()
        self.write(self.getScoreMsg(),True,  align='left', font=('Arial', 20, 'normal'))

    def reset(self):
        self.clear()
        self.highscore = max(self.score, self.highscore)
        with open(self.scoresfile, mode='w') as outfile:
            outfile.write(str(self.highscore))
        self.score = 0

    def gameOverMsg(self):
        self.goto(-70,0)
        self.write(self.game_over_msg,True,  align='left', font=('Arial', 20, 'normal'))


