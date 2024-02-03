import csv
from dataclasses import dataclass
from typing import List
@dataclass
class HighScore:
    rank: int
    name: str
    score: int


def load_high_scores(filename="high_scores.csv") -> List[HighScore]:
    """
    Highscore structure

    rank, name, score

    :param filename:
    :return:
    """

    high_scores = []

    with open(filename, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        line_counter = 0



        for row in csv_reader:
            if line_counter != 0:
                high_scores.append(HighScore(int(row[0]),row[1],int(row[2])))
            else:
                line_counter += 1

    return high_scores

def add_score_to_high_scores(high_scores: List[HighScore], score: int, name) -> List[HighScore]:
    for i in range(len(high_scores)):
        if score> high_scores[i].score:
            high_scores.insert(i, HighScore(i, name, score))
            break

    #rearrange ranks
    high_scores = high_scores[:10]
    for i in range(10):
        high_scores[i].rank = i + 1

    return high_scores

def save_high_scores(high_scores,filename="high_scores.csv"):

    # trim highscores if bigger the n


    with open(filename, "w", newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')


        csv_writer.writerow(["Rank", "Name", "Score"])
        for score in high_scores:
            csv_writer.writerow([score.rank,score.name,score.score])


if __name__ == "__main__":

    high_scores = [HighScore(1,"Bob",85),
                   HighScore(2,"Bob",80),
                   HighScore(3,"Ross",63),
                   HighScore(4,"Karl",61),
                   HighScore(5,"CPU",60),
                   HighScore(6,"CPU",50),
                   HighScore(7,"Jenkins",45),
                   HighScore(8,"Jenkins",44),
                   HighScore(9,"Karl",40),
                   HighScore(10,"Bob",35)]

    save_high_scores(high_scores)
