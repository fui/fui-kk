#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the web reports for each course."""

__authors__    = ["Ole Herman Schumacher Elgesem"]
__copyright__  = "Ole Herman Schumacher Elgesem"
__license__    = "MIT"
# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.

import os
import sys
import json
import re
from collections import OrderedDict
from file_funcs import dump_json, load_json

def get_participation_string(participation, language):
    if language == "EN":
        labels = ["Respondents","of"]
    elif language == "NO":
        labels = ["Antall besvarelser","av"]
    else:
        print("Unknown language: " + str(language))
        sys.exit(1)
    invited = int(participation["invited"])
    answered = int(participation["answered"])
    return "<b>{labels[0]}:</b> {} {labels[1]} {} ({percentage:.1f}%)".format(
        answered,
        invited,
        labels = labels,
        percentage = 0 if invited == 0 else (answered / invited * 100))

def create_chart_js(question, question_stats, scales, chart_id):
    chart_data = []
    answers = scales[question]["order"]
    for answer in answers:
        if answer in question_stats["counts"]:
            count = question_stats["counts"][answer]
        else:
            count = 0
        chart_data.append('{{ label: "{}", value: {} }}'.format(answer, count))
    if len(answers) == 6:
        colors = "['#1a9850', '#91cf60', '#d9ef8b', '#fee08b', '#fc8d59', '#d73027']"
    elif len(answers) == 5:
        colors = "['#d7191c', '#fdae61', '#91cf60', '#abd9e9', '#2c7bb6']"
    else:
        print("Warning: Chart for '{}' omitted. No colors defined for questions with {} alternatives".format(
            question, len(answers)))
        return ''
    return 'insert_chart("#{}", [{}], {});'.format(chart_id, ", ".join(chart_data), colors)

def web_report_course(summary_path, stat_path, output_path, html_templates, courses, scales):
    with open(summary_path,'r') as f:
        summary = f.read()
    summary = summary.replace("</p>\n</blockquote>", "</blockquote>")
    summary = summary.replace("<blockquote>\n<p>", "<blockquote>")

    stats = load_json(stat_path)
    course_code = stats["course"]["code"]
    course_name = stats["course"]["name"]
    language = stats["language"]
    semester = stats["course"]["semester"]
    participation = stats["respondents"]
    participation_string = get_participation_string(participation, language)

    if language == "NO":
        general_question = "Hva er ditt generelle intrykk av kurset?"
    elif language == "EN":
        general_question = "How do you rate the course in general?"
    else:
        print("Error: Unknown language " + str(language))
        sys.exit(1)
    general_average_text = stats["questions"][general_question]["average_text"]
    course_url = "https://www.uio.no/studier/emner/matnat/ifi/"+course_code

    main_contents = []
    additional_js = []
    if language == "NO":
        main_contents.append(r"<h2>Vurdering:</h2>")
        main_contents.append(r"(Gjennomsnittlige svar på de viktigste spørsmålene)<br />")
    else:
        main_contents.append(r"<h2>Assessment:</h2>")
        main_contents.append(r"(Average answers to the most important questions)<br />")

    for question, question_stats in stats["questions"].items():
        main_contents.append(r"<i>"+question+"</i> " + question_stats["average_text"] + " <br />")
        chart_id = 'chart_' + re.sub('[^a-z]+', '', question.lower())
        main_contents.append('<div id="{}" class="chart"></div>'.format(chart_id))
        additional_js.append(create_chart_js(question, question_stats, scales, chart_id))

    if language == "NO":
        main_contents.append(r"<h2>Oppsummering:</h2>")
    else:
        main_contents.append(r"<h2>Summary:</h2>")

    try:
        split_index = summary.index("<blockquote>")
        quotes = summary[split_index:]
        summary = summary[0:split_index]
        main_contents.append(summary)
        if language == "NO":
            main_contents.append(r"<h2>Sitater:</h2>")
        else:
            main_contents.append(r"<h2>Quotes:</h2>")
        main_contents.append(quotes)
    except ValueError:
        main_contents.append(summary)

    main_body = "\n".join(main_contents)

    course_rating = []
    for semester, semester_data in courses[course_code].items():
        # Dirty, some courses have both english and norwegian semesters:
        try:
            average = semester_data["Hva er ditt generelle intrykk av kurset?"]["average"]
        except:
            average = semester_data["How do you rate the course in general?"]["average"]
        course_rating.append([semester, round(average+1.0, 2)])

    # Replace $ keywords from template html:
    replace_tags = {
        "$COURSE_CODE": course_code,
        "$COURSE_NAME": course_name,
        "$PARTICIPATION_STRING": participation_string,
        "$SEMESTER": semester,
        "$GENERAL_AVERAGE_TEXT": general_average_text,
        "$MAIN_BODY": main_body,
        "$ADDITIONAL_JS": "\n".join(additional_js),
        "$COURSE_URL": course_url,
        "$COURSE_RATING": str(course_rating).replace("'", '"')
    }
    html = html_templates[language]
    for tag, replacement in replace_tags.items():
        html = html.replace(tag, replacement)

    with open(output_path,'w') as f:
        f.write(html)
    return course_code, course_name

def web_reports_semester_folder(semester_path):
    semester = os.path.basename(semester_path)
    courses = load_json(semester_path+"/outputs/courses.json")
    scales = load_json(semester_path+"/outputs/scales.json")
    stats_path = semester_path+"/outputs/stats/"
    summaries_path = semester_path+"/outputs/web/converted"
    upload_path = semester_path+"/outputs/web/upload/"+semester

    html_templates = {}
    with open("./resources/web/course-no.html",'r') as f:
        html_templates["NO"] = f.read()
    with open("./resources/web/course-en.html",'r') as f:
        html_templates["EN"] = f.read()
    with open("./resources/web/semester-index.html",'r') as f:
        html_templates["index"] = f.read()
    with open("./resources/web/semester-index-eng.html",'r') as f:
        html_templates["index-eng"] = f.read()
    with open("./data/courses.json",'r') as f:
        courses_all = json.load(f, object_pairs_hook=OrderedDict)

    links = []
    links.append('<ul class="fui_courses">')
    for course_code in courses:
        summary_path = os.path.join(summaries_path, course_code+".html")
        stat_path = os.path.join(stats_path, course_code+".json")
        output_path = os.path.join(upload_path, course_code+".html")

        web_report_course(summary_path, stat_path, output_path, html_templates, courses_all, scales)

        course_name = courses[course_code]["course"]["name"]
        links.append('<li><a href="'+course_code+'.html">' + course_code + ' - ' + course_name + '</a></li>')
    links.append("</ul>")
    links_str = "\n".join(links)

    letter, year = semester[0],semester[1:]
    title = {}
    if letter == "H":
        title["NO"] = "Høst "+year
        title["EN"] = "Fall "+year
    elif letter == "V":
        title["NO"] = "Vår "+year
        title["EN"] = "Spring "+year
    else:
        print("Error: unknown semester format: " + semester)
        sys.exit(1)

    links_str_no   = "<h2>{}</h2>".format(title["NO"]) + links_str
    links_str_en   = "<h2>{}</h2>".format(title["EN"]) + links_str
    index_html     = html_templates["index"].replace("$COURSE_INDEX", links_str_no)
    index_eng_html = html_templates["index-eng"].replace("$COURSE_INDEX", links_str_en)
    index_html     = index_html.replace("$SEMESTER", semester)
    index_eng_html = index_eng_html.replace("$SEMESTER", semester)

    with open(upload_path+"/index.html", "w") as f:
        f.write(index_html)
    with open(upload_path+"/index-eng.html", "w") as f:
        f.write(index_eng_html)

if __name__ == '__main__':
    web_reports_semester_folder(sys.argv[1])
