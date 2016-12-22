#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Documentation string"""

__authors__    = ["Ole Herman Schumacher Elgesem"]
__copyright__  = "Ole Herman Schumacher Elgesem"
__credits__    = []
__license__    = "MIT"
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.

import os
import sys
import json
from bs4 import BeautifulSoup
from collections import OrderedDict

def answer_case(answer_raw):
    answer = answer_raw.upper()
    if answer == "OK":
        return answer
    if len(answer) > 1:
        answer = answer[0] + answer[1:].lower()
    return answer

def convert_answer_case(scales):
    for question, answer_lists in scales.items():
        for answer_list in answer_lists:
            if len(answer_list) > 0 and "EDIT THIS" not in answer_list[0]:
                scales[question][answer_list] = \
                [answer_case(x) for x in scales[question][answer_list]]

def scales_add_course(response_file_path, scales):
    course = OrderedDict()
    with open(response_file_path, "r") as f:
        course = json.load(f, object_pairs_hook=OrderedDict)
    for question, answers in course.items():
        if question in scales:
            if "order" not in scales[question]:
                scales[question]["order"] = ["EDIT THIS, as well as ignore, see README.md."]
            if "all" not in scales[question]:
                scales[question]["all"] = []
            if "ignore" not in scales[question]:
                scales[question]["ignore"] = []
            for answer in answers:
                answer_cap = answer_case(answer)
                if answer_cap not in scales[question]["all"]:
                    scales[question]["all"].append(answer_cap)
                    print('Warning: Adding "{}" to "{}", you will probably have to update scales.json'.format(answer_cap, question))

def get_default_ignore():
    default_ignore = ["", "Not relevant", "Vet ikke", "No opinion", "Ikke aktuelt"]
    default_ignore = [answer_case(x) for x in default_ignore]
    return default_ignore

def get_default_order():
    # This order is just for better readability/usability
    # User has to manually sort into order list, this just makes it easier.
    default_order = [
    "Særdeles bra",   "For høyt",  "For høy", "For vanskelig",  "Exceptionally good", "Too high",  "Too difficult", "Too large",
    "Meget bra",      "Høyt",      "Høy",     "Noe vanskelig",  "Very good",          "High",      "Difficult",     "Large",
    "Bra",            "Good",
    "Grei",           "Greit",     "Passe",                     "OK",
    "Mindre bra",     "Lavt",      "Lav",     "Noe lett",       "Not that good",      "Low",       "Easy",          "Small",
    "Lite bra",       "For lavt",  "For lav", "Lett",           "Not good",           "Too low",   "Too Easy",      "Too small"
    ]

    default_order = [answer_case(x) for x in default_order]
    return default_order

def get_all_default_answers():
    return get_default_ignore() + get_default_order()

def default_sort(old_order):
    default_order = get_default_order()

    new_order = []
    for answer in old_order:
        if answer not in default_order:
            new_order.append(answer)
    for answer in default_order:
        if answer in old_order:
            new_order.append(answer)
    assert len(new_order) == len(old_order)
    return new_order

def default_sort_scales(scales):
    for question in scales:
        if "all" in scales[question]:
            scales[question]["all"] = default_sort(scales[question]["all"])

def autofill_question(answer_lists):
    answer_lists["order"] = []
    answer_lists["ignore"] = []
    default_ignore = get_default_ignore()
    for answer in answer_lists["all"]:
        if answer in default_ignore:
            answer_lists["ignore"].append(answer)
        else:
            answer_lists["order"].append(answer)

def yes_or_no():
    inp = input()
    while inp != "y" and inp != "n":
        print("Please enter either 'y' for yes or 'n' for no.")
        inp = input()
    return inp

def save_prompt_exit(scales, scales_path):
    print("Do you want to save (overwrite) scales before quitting?(y/n)")
    inp = yes_or_no()
    if inp == "y":
        with open(scales_path, "w") as f:
            json.dump(scales, f, indent=4, ensure_ascii=False)
    sys.exit(1)

class AutofillException(Exception):
    pass

def autofill_prompt(scales):
    print("Is this autofill correct?(y/n)")
    inp = yes_or_no()
    if inp == "n":
        print("Please open scales.json to correct this question before running this script again")
        raise AutofillException("Incorrect autofill raised by user")

def autofill_scales(scales):
    default_answers = set(get_all_default_answers())
    for question, answer_lists in scales.items():
        if (not question) or ("all" not in answer_lists):
            continue
        list_all    = scales[question]["all"]
        list_order  = scales[question]["order"]
        list_ignore = scales[question]["ignore"]
        num_all     = len(list_all)
        num_order   = len(list_order)
        num_ignore  = len(list_ignore)
        if num_all != num_order + num_ignore:
            if set(list_all).issubset(default_answers):
                autofill_question(scales[question])
                print("")
                print("Warning: The question below has been autofilled and should be reviewed:")
                print("Make sure that the structure below is correct (see README.md).")
                print('"order" is the order used to rank the answers when calculating statistics.')
                print('"all" should contain all possible answers to the question.')
                print('"ignore" decides what answers to skip when calculating statistics.')
                print('\n"{}"'.format(question))
                print(json.dumps(scales[question], indent=4, ensure_ascii=False))
                autofill_prompt(scales)

def add_error(errors, question, message):
    if question not in errors:
        errors[question] = []
    errors[question].append(message)

def error_check(scales):
    errors = OrderedDict()
    for question, answer_lists in scales.items():
        if "all" not in answer_lists:
            add_error(errors, question, "'all' list is missing,"
            " do not delete this, it is used to check for errors.")
        if "order" not in answer_lists:
            add_error(errors, question, "'order' list is missing,"
            " this is needed to rank the different answers.")
        if "ignore" not in answer_lists:
            add_error(errors, question, "'ignore' list is missing,"
            " this is used to exclude answers from ranking.")
        if question in errors:
            continue

        list_all    = scales[question]["all"]
        list_order  = scales[question]["order"]
        list_ignore = scales[question]["ignore"]
        num_all     = len(list_all)
        num_order   = len(list_order)
        num_ignore  = len(list_ignore)
        if num_order  > 0 and "EDIT THIS" in list_order[0] or\
           num_ignore > 0 and "EDIT THIS" in list_ignore[0]:
                add_error(errors, question, "needs to be edited manually. "
                "(contains 'EDIT THIS' answer, remove this when done)")
                continue

        if num_all != (num_order + num_ignore):
            add_error(errors, question, "all != order + ignore,"
            " you should copy the answers from all into order/ignore.")
        for answer in list_all:
            if answer in list_order and answer in list_ignore:
                add_error(errors, question,
                '"{}" cannot be in both order and ignore.'.format(answer))
            elif answer not in list_order and answer not in list_ignore:
                add_error(errors, question,
                '"{}" must be in either order or ignore.'.format(answer))
        for answer in list_order:
            if answer not in list_all:
                add_error(errors, question,
                '"{}" is in order but not in all, typo?'.format(answer))
        for answer in list_ignore:
            if answer not in list_all:
                add_error(errors, question,
                '"{}" is in ignore but not in all, typo?'.format(answer))
    return errors

def print_error_check(scales):
    errors = error_check(scales)
    if not errors:
        return False
    total = 0
    question_counter = 0
    print("")
    print("ERROR SUMMARY - scales.json")
    for question, messages in errors.items():
        print('Error(s) in "' + question + '":')
        counter = 0
        for msg in messages:
            print(" {},{}: {}".format(question_counter+1, counter+1, msg))
            counter += 1
        total += counter
        question_counter += 1
    print("Total errors: {} in {} questions".format(total, question_counter))
    print("END OF ERROR SUMMARY")
    print("")
    return True

def json_loader(path):
    try:
        with open(path, "r") as f:
            scales = json.load(f, object_pairs_hook=OrderedDict)
    except json.decoder.JSONDecodeError as err:
        print("ERROR: The file '{}' contains invalid json syntax: {}".format(path,err))
        sys.exit(1)
    except FileNotFoundError:
        print("ERROR: Could not open '{}' for read, file doesn't exist.".format(path))
        sys.exit(1)
    return scales

def generate_scales(semester):
    scales = OrderedDict()
    scales_path = "./data/"+semester+"/outputs/scales.json"
    default_scales_path = "./resources/scales.json"
    if not os.path.exists(scales_path):
        scales = json_loader(default_scales_path)
    else:
        scales = json_loader(scales_path)

    if not scales:
        scales = OrderedDict()
        q = "Remove this example question - How do you rate the course in general? (Add questions like this)"
        scales[q] = OrderedDict()

    convert_answer_case(scales)

    responses_path = "./data/"+semester+"/outputs/responses/"
    for (dirpath, dirnames, filenames) in os.walk(responses_path):
        for filename in filenames:
            if filename.endswith(".json"):
                file_path = os.path.join(dirpath,filename)
                scales_add_course(file_path, scales)
        break

    default_sort_scales(scales)
    try:
        autofill_scales(scales)
    except AutofillException:
        save_prompt_exit(scales, scales_path)

    with open(scales_path, "w") as f:
        json.dump(scales, f, indent=4, ensure_ascii=False)
    if print_error_check(scales):
        print("One or more inconsistency detected in " + scales_path)
        print("You will have to edit the file manually to add/edit/remove questions.")
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 ./scripts/scales.py SEMESTER")
        sys.exit(1)
    generate_scales(sys.argv[1])
