#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Documentation string"""

__authors__    = ["Ole Herman Schumacher Elgesem"]
__copyright__  = "FUI - Fagutvalget ved Institutt for Informatikk"
__credits__    = []
__license__    = "MIT"
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.

import os
import sys
import json
from bs4 import BeautifulSoup

def gen_dict(key_list, alternative_list = [], alternative_list2 = []):
    num = [x+1 for x in range(len(key_list))]
    dic = dict(zip(key_list,num))

    alternative_lists = [alternative_list, alternative_list2]
    for alt in alternative_lists:
        for i in range(0, len(alt)):
            if(alt[i] != "" and alt[i] != key_list[i]):
                dic[alt[i]] = dic[key_list[i]]

    return dic

def main():
    kvalitet = gen_dict(\
    ["Lite bra","Mindre bra","Greit","Bra","Meget bra","Særdeles bra"],\
    ["","","Grei","","",""])

    nivå = gen_dict(["Lett","Noe lett","Passe","Noe vanskelig","For vanskelig"])

    mengde = gen_dict(["For lav","Lav","Passe","Høy","For høy"],\
                      ["For lavt","Lavt","","Høyt","For høyt"])

    informasjon = gen_dict(["Lite bra","Grei","Bra","Meget bra","Særdeles bra"])

    quality = gen_dict(["Not good","Not that good","OK","Good","Very good",\
    "Exceptionally good"])

    level = gen_dict(["Too easy","Easy","OK","Difficult", "Too difficult"])

    amount = gen_dict(["Too small","Small","OK","Large","Too large"],
                      ["Too low","Low","OK","High","Too high"])

    scales = {}
    scales["kvalitet"] = kvalitet
    scales["nivå"] = nivå
    scales["mengde"] = mengde
    scales["informasjon"] = informasjon
    scales["quality"] = quality
    scales["level"] = level
    scales["amount"] = amount

    lookup = {}
    lookup["Hva er ditt generelle intrykk av kurset?"] = {"qid":"general", "scale": "kvalitet"}
    lookup["Hva synes du om emnets nivå?"] = {"qid":"level", "scale": "nivå"}
    lookup["Hva synes du om arbeidsmengden sett i forhold til antall studiepoeng?"] = {"qid":"workload", "scale": "mengde"}

    lookup["Kvaliteten på forelesningene?"] = {"qid":"lecture_quality", "scale": "kvalitet"}
    lookup["Forelesningenes relevans og nytteverdi i forhold til å formidle det du trenger å lære?"] = {"qid":"lecture_relevance", "scale": "kvalitet"}
    lookup["Kvaliteten på gruppeundervisningen i sin helhet?"] = {"qid":"group_quality", "scale": "kvalitet"}
    lookup["I hvilken grad forbedrer ukesoppgavene og gruppeundervisningen din forståelse av pensum?"] = {"qid":"group_relevance", "scale": "kvalitet"}
    lookup["Er pensum og læringsmål i emnet godt definert?"] = {"qid":"curriculum", "scale": "kvalitet"}
    lookup["Hvordan vurderer du kursmateriellet som benyttes (lærebok m.m.)?"] = {"qid":"materials", "scale": "kvalitet"}

    lookup["Hva synes du om kurspresentasjonen på nett?"] = {"qid":"course_web", "scale": "informasjon"}
    lookup["Hva synes du om kursets semesterside?"] = {"qid":"semester_web", "scale": "informasjon"}

    lookup["Hvordan er nivået på obligene?"] = {"qid":"assignment_level", "scale": "mengde"}
    lookup["Hva synes du om antallet obliger?"] = {"qid":"assignments_amount", "scale": "mengde"}
    lookup["Hva syns du om nivået på deleksamen?"] = {"qid":"midterm_level", "scale": "mengde"}
    lookup["Hva synes du om nivået på avsluttende eksamen?"] = {"qid":"final_level", "scale": "mengde"}

    lookup["How do you rate the course in general?"] = {"qid":"general", "scale": "quality"}
    lookup["How do you rate the level of the course?"] = {"qid":"level", "scale": "level"}
    lookup["How do you rate the work load in proportion to the number of credits achieved?"] = {"qid":"workload", "scale": "amount"}

    lookup["The quality of the lectures?"] = {"qid":"lecture_quality", "scale": "quality"}
    lookup["The lectures' relevance and usefulness in regard to relaying what you need to learn?"] = {"qid":"lecture_relevance", "scale": "quality"}
    lookup["The quality of the group tuition as a whole?"] = {"qid":"group_quality", "scale": "quality"}
    lookup["In what degree does group tuition and weekly assignments give you practical skills and the possibility to make use of the theory at hand?"] = {"qid":"group_relevance", "scale": "quality"}
    lookup["Are the curriculum and learning outcomes of the course sufficiently defined?"] = {"qid":"curriculum", "scale": "quality"}
    lookup["How do you rate the course material used (text book etc.)?"] = {"qid":"materials", "scale": "quality"}

    lookup["How would you assess the online course presentation?"] = {"qid":"course_web", "scale": "quality"}
    lookup["How would you assess the course's term page?"] = {"qid":"semester_web", "scale": "quality"}

    lookup["How do you rate the difficulty level of the obligatory assignments?"] = {"qid":"assignment_level", "scale": "amount"}
    lookup["What is your opinion in regard to the number of obligatory assignments?"] = {"qid":"assignments_amount", "scale": "amount"}
    lookup["How do you rate the difficulty level of the midterm examination(s)?"] = {"qid":"midterm_level", "scale": "amount"}
    lookup["How do you rate the difficulty level of the final examination?"] = {"qid":"final_level", "scale": "amount"}

    invalid = ["No opinion", "Not relevant", "Not applicable", "Ikke relevant", "Ikke aktuelt", "Vet ikke"]
    grades = {"scales":scales, "questions": lookup, "invalid": invalid}


    with open("data/scales.json", "w") as f:
        json.dump(grades,f, sort_keys=True, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    main()
