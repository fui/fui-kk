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
    lookup["Hva er ditt generelle intrykk av kurset?"] = "kvalitet"
    lookup["Hva synes du om emnets nivå?"] = "nivå"
    lookup["Hva synes du om arbeidsmengden sett i forhold til antall studiepoeng?"] = "mengde"

    lookup["Kvaliteten på forelesningene?"] =\
    lookup["Forelesningenes relevans og nytteverdi i forhold til å formidle det du trenger å lære?"] =\
    lookup["Kvaliteten på gruppeundervisningen i sin helhet?"] =\
    lookup["I hvilken grad forbedrer ukesoppgavene og gruppeundervisningen din forståelse av pensum?"] =\
    lookup["Er pensum og læringsmål i emnet godt definert?"] =\
    lookup["Hvordan vurderer du kursmateriellet som benyttes (lærebok m.m.)?"] = "kvalitet"

    lookup["Hva synes du om kurspresentasjonen på nett?"] = "informasjon"
    lookup["Hva synes du om kursets semesterside?"] = "informasjon"

    lookup["Hvordan er nivået på obligene?"] =\
    lookup["Hva synes du om antallet obliger?"] =\
    lookup["Hva syns du om nivået på deleksamen?"] =\
    lookup["Hva synes du om nivået på avsluttende eksamen?"] = "mengde"

    lookup["How do you rate the course in general?"] = "quality"
    lookup["How do you rate the level of the course?"] = "level"
    lookup["How do you rate the work load in proportion to the number of credits achieved?"] = "load"

    lookup["The quality of the lectures?"] =\
    lookup["The lectures' relevance and usefulness in regard to relaying what you need to learn?"] =\
    lookup["The quality of the group tuition as a whole?"] =\
    lookup["In what degree does group tuition and weekly assignments give you practical skills and the possibility to make use of the theory at hand?"] =\
    lookup["Are the curriculum and learning outcomes of the course sufficiently defined?"] =\
    lookup["How do you rate the course material used (text book etc.)?"] = "quality"

    lookup["How would you assess the online course presentation?"] = "quality"
    lookup["How would you assess the course's term page?"] = "quality"

    lookup["How do you rate the difficulty level of the obligatory assignments?"] =\
    lookup["What is your opinion in regard to the number of obligatory assignments?"] =\
    lookup["How do you rate the difficulty level of the midterm examination(s)?"] =\
    lookup["How do you rate the difficulty level of the final examination?"] = "amount"

    grades = {"scales":scales, "questions": lookup}

    with open("data/answer-values.json", "w") as f:
        json.dump(grades,f, sort_keys=True, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    main()
