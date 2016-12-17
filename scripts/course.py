#!/usr/bin/env python3
"""Create relevant statistics from individual responses"""

__authors__    = ["Ole Herman Schumacher Elgesem"]
__copyright__  = "Ole Herman Schumacher Elgesem"
__license__    = "MIT"
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.

import os
import sys
from bs4 import BeautifulSoup
import json
from collections import OrderedDict

def dump_to_file(data, filename):
    folder = os.path.dirname(filename)
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(filename, 'w') as out_file:
        json.dump(data, out_file, indent=4, ensure_ascii=False)

def read_from_file(filename):
    with open(filename, 'r') as in_file:
        return json.load(in_file, object_pairs_hook=OrderedDict)

def generate_stats(responses, participation):
    stats = OrderedDict()
    started = int(participation["started"])
    answered = int(participation["answered"])
    if(answered == 0):
        return None
    invited = int(participation["invited"])
    percentage = 100;
    if(invited > 0):
        percentage = 100 * answered/invited;
    respondents = OrderedDict()
    respondents["started"] = started
    respondents["answered"] = answered
    respondents["invited"] = invited
    stats["respondents"] = respondents
    stats["answer_percentage"] = percentage

    questions = OrderedDict()

    language = ""

    scales = json.load(open("data/scales.json"))
    for question in responses:
        if question in scales["questions"]:
            if language == "":
                if question[0:3] == "Hva":
                    language = "NO"
                if question[0:3] == "How":
                    language = "EN"
            question_answers = responses[question]
            scale_key = scales["questions"][question]["scale"]
            qid = scales["questions"][question]["qid"]
            scale = scales["scales"][scale_key]

            questions[qid] = OrderedDict()
            questions[qid]["text"] = question

            counts = {}
            total = 0;
            ctr = 0;
            for answer in question_answers:
                if answer not in scales["invalid"]:
                    ctr += 1
                    total += scale[answer]
                if answer in counts:
                    counts[answer] += 1
                else:
                    counts[answer] = 1
            if ctr == 0:
                average = "None"
            else:
                average = total/ctr
            delta = 1000
            average_text = ""
            if average != "None":
                for grade in scale:
                    d = abs(average - scale[grade])
                    if d < delta:
                        delta = d
                        average_text = grade
            questions[qid]["counts"] = counts
            questions[qid]["average"] = average
            questions[qid]["average_text"] = average_text

            max_people = 0
            most_common = []
            for c in counts:
                if counts[c] > max_people:
                    most_common = [c]
                    max_people = counts[c]
                elif counts[c] == max_people:
                    most_common.append(c)
            questions[qid]["most_common"] = OrderedDict()
            questions[qid]["most_common"]["words"] = most_common
            questions[qid]["most_common"]["num"] = max_people
            questions[qid]["most_common"]["per"] = max_people/answered

    stats["language"] = language
    stats["questions"] = questions
    return stats

def generate_stats_file(responses_path, participation_path, output_path):
    responses = read_from_file(responses_path)
    participation = read_from_file(participation_path)
    stats = generate_stats(responses, participation)
    if stats is not None:
        dump_to_file(stats, output_path)

def generate_stats_dir(responses_dir, participation_dir, output_dir):
    for filename in os.listdir(responses_dir):
        if ".json" in filename:
            responses_path = os.path.join(responses_dir,filename)
            participation_path = os.path.join(participation_dir,filename)
            output_path = os.path.join(output_dir, filename)
            generate_stats_file(responses_path, participation_path, output_path)

def generate_stats_semester(semester_path):
    generate_stats_dir(semester_path+"/outputs/responses",
                       semester_path+"/downloads/participation",
                       semester_path+"/outputs/stats")

if __name__ == '__main__':
    if len(sys.argv) == 1 or not os.path.isdir(sys.argv[1]):
        sys.exit("Must specify dir")
    directory = sys.argv[1]
    semester_dirs = []
    for (root, dirs, files) in os.walk(directory):
        for d in dirs:
            if "." not in d:
                semester_dirs.append(os.path.join(root, d))
                # TODO: Move this somewhere else:
                os.makedirs(os.path.join(root,d,"inputs","md"), exist_ok=True)
                os.makedirs(os.path.join(root,d,"inputs","tex"), exist_ok=True)
        break
    for d in semester_dirs:
        generate_stats_semester(d)
