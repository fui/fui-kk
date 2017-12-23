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
from file_funcs import dump_json, load_json, path_join

def generate_stats(responses, participation, scales, stats=None):
    if stats is None:
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

    language = None

    for question in responses:
        if question in scales:
            if language is None:
                if "Hva" in question or "Hvordan" in question:
                    language = "NO"
                elif "How" in question or "What" in question:
                    language = "EN"
                else:
                    print("Unable to detect language in question:")
                    print(question)
                    sys.exit(1)
            question_answers = responses[question]
            answer_order = list(reversed(scales[question]["order"]))
            answer_ignore = scales[question]["ignore"]
            questions[question] = OrderedDict()

            counts = OrderedDict()
            total = 0;
            ctr = 0;
            for answer in question_answers:
                if answer not in answer_ignore:
                    ctr += 1
                    total += answer_order.index(answer)
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
                rounded = int(round(average, 0))
                average_text = answer_order[rounded]
            questions[question]["counts"] = counts
            questions[question]["average"] = average
            questions[question]["average_text"] = average_text

            # max_people = 0
            # most_common = []
            # for c in counts:
            #     if counts[c] > max_people:
            #         most_common = [c]
            #         max_people = counts[c]
            #     elif counts[c] == max_people:
            #         most_common.append(c)
            # questions[question]["most_common_answer"] = OrderedDict()
            # questions[question]["most_common_answer"]["text"] = most_common
            # questions[question]["most_common_answer"]["people"] = max_people
            # questions[question]["most_common_answer"]["percentage"] = max_people/answered

    stats["language"] = language
    stats["questions"] = questions
    return stats

def generate_stats_file(responses_path, participation_path, output_path, scales, course):
    responses = load_json(responses_path)
    participation = load_json(participation_path)
    stats = OrderedDict()
    stats["course"] = course
    stats = generate_stats(responses, participation, scales, stats)
    if not stats:
        print("Skipping course with 0 answers:")
        print(json.dumps(course, indent=2))
        return
    if not stats["language"]:
        print("Unable to detect language in course:")
        print(json.dumps(course, indent=2))
        print("This most likely means that the questions have changed and need to be added to scales.json")
        sys.exit(1)

    dump_json(stats, output_path)

def generate_stats_dir(responses_dir, participation_dir, output_dir, scales, course_names, semester_name):
    for filename in os.listdir(responses_dir):
        if ".json" in filename:
            course = OrderedDict()
            course_code = os.path.splitext(filename)[0]
            try:
                course_name = course_names[course_code]
            except KeyError:
                course_name = "Unknown"
                print("Warning: could not find name for course " + course_code)
            course["code"] = course_code
            course["name"] = course_name
            course["semester"] = semester_name
            responses_path = path_join(responses_dir,filename)
            participation_path = path_join(participation_dir,filename)
            output_path = path_join(output_dir, filename)
            generate_stats_file(responses_path, participation_path, output_path, scales, course)

def generate_stats_semester(semester_path, semester_name):
    scales_path = semester_path+"/outputs/scales.json"
    scales = load_json(scales_path)
    course_names = load_json("./resources/course_names/all.json")
    generate_stats_dir(semester_path+"/outputs/responses",
                       semester_path+"/downloads/participation",
                       semester_path+"/outputs/stats",
                       scales, course_names, semester_name)

if __name__ == '__main__':
    if len(sys.argv) == 1 or not os.path.isdir(sys.argv[1]):
        sys.exit("Must specify dir")
    directory = sys.argv[1]
    semester_dirs = []
    for (root, dirs, files) in os.walk(directory):
        for d in dirs:
            if "." not in d:
                semester_dirs.append(path_join(root, d))
                # TODO: Move this somewhere else:
                os.makedirs(path_join(root,d,"inputs","md"), exist_ok=True)
                os.makedirs(path_join(root,d,"inputs","tex"), exist_ok=True)
        break
    for d in semester_dirs:
        generate_stats_semester(d, os.path.basename(d))
