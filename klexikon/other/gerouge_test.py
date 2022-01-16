from klexikon.GeRouge.rouge import GeRouge

prediction = """
Berlin ist Hauptstadt und als Land eine parlamentarische Republik und ein teilsouveräner Gliedstaat der Bundesrepublik Deutschland.
Die Stadt ist mit rund 3,7 Millionen Einwohnern die bevölkerungsreichste und mit 892 Quadratkilometern die flächengrößte Gemeinde Deutschlands.
Es ist zugleich die einwohnerstärkste Stadt der Europäischen Union.
"""

reference = """
Berlin ist Hauptstadt der Bundesrepublik Deutschland und ein eigenes Bundesland.
Mit rund 3,7 Millionen Einwohnern ist es die bevölkerungsreichste und mit 892 Quadratkilometern die größte Gemeinde Deutschlands.
Es ist gleichzeitig die einwohnerstärkste Stadt der EU."""


if __name__ == '__main__':
    scorer = GeRouge(alpha=0.5, stemming=True, split_compounds=True, minimal_mode=False)
    print(scorer.rouge_n(reference, prediction))
    print(scorer.rouge_l(reference, prediction))
