# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 14:07:43 2018
@author: Simon
"""

import codecs
from nltk.translate.bleu_score import sentence_bleu
from nltk.translate.bleu_score import SmoothingFunction

def bleu(answerFilePath, standardAnswerFilePath):
    with codecs.open(answerFilePath, 'r', "utf-8") as rf_answer:
        with codecs.open(standardAnswerFilePath, 'r', "utf-8") as rf_standardAnswer:
            score = []
            answerLines = rf_answer.readlines()
            standardAnswerLines = rf_standardAnswer.readlines()
            chencherry = SmoothingFunction()
            for i in range(len(answerLines)):
                candidate = list(answerLines[i].strip())
                eachScore = 0
                #10个标准答案
                for j in range(10):
                    reference = []
                    standardAnswerLine = standardAnswerLines[i*11+j].strip().split('\t')
                    reference.append(list(standardAnswerLine[0].strip()))
                    standardScore = standardAnswerLine[1]
                    #bleu
                    bleuScore = sentence_bleu(reference,candidate,weights=(0.35,0.45,0.1,0.1),smoothing_function=chencherry.method1)
                    #加权平均
                    eachScore = bleuScore * float(standardScore) + eachScore
                score.append(eachScore/10)
                eachScore = 0
            
            rf_answer.close()
            rf_standardAnswer.close()
            #最终得分
            scoreFinal = sum(score)/float(len(answerLines))
            #最终得分精确到小数点后6位
            precisionScore = round(scoreFinal,6)
            return precisionScore
                    

if __name__ == "__main__":
    candidateFilePath = "result.txt"
    referenceFilePath = "true_result.txt"
    score_final = bleu(candidateFilePath,referenceFilePath)
    print(score_final)               
