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
from file_funcs import dump_json, load_json, path_join

def generate_semesters(start, stop):
    yield start
    current = start
    while current != stop:
        pre, year = current[0], int(current[1:])
        assert pre == "V" or pre == "H"
        assert year in range(1900, 2300)
        if pre == "V":
            pre = "H"
        elif pre == "H":
            pre = "V"
            year += 1
        current = pre + str(year)
        yield current

def get_general_questions():
    general_questions = []
    general_questions.append("Hva er ditt generelle intrykk av kurset?")
    general_questions.append("Hva er ditt generelle inntrykk av kurset?")
    general_questions.append("How do you rate the course in general?")
    general_questions.append("What is your general impression of the course?")
    return general_questions

def look_for_general_question(data):
    for q in get_general_questions():
        if q in data:
            return q
    return None

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
    # TODO: Define 7 and 9 color scale
    if len(answers) == 9:
        colors = "['#00ff00', '#44ff00', '#88ff00', '#ccff00', '#ffff00', '#ffcc00', '#ff8800', '#ff4400', '#ff0000']"
    elif len(answers) == 7:
        colors = "['#00ff00', '#66ff00', '#ccff00', '#ffff00', '#ffcc00', '#ff6600', '#ff0000']"
    elif len(answers) == 6:
        colors = "['#1a9850', '#91cf60', '#d9ef8b', '#fee08b', '#fc8d59', '#d73027']"
    elif len(answers) == 5:
        colors = "['#d7191c', '#fdae61', '#91cf60', '#abd9e9', '#2c7bb6']"
    else:
        print("Warning: Chart for '{}' omitted. No colors defined for questions with {} alternatives".format(
            question, len(answers)))
        return ''
    return 'insert_chart("#{}", [{}], {});'.format(chart_id, ", ".join(chart_data), colors)

def web_report_course(summary_path, stat_path, output_path, html_templates, courses, scales, current_semester):
    stats = load_json(stat_path)

    participation = stats["respondents"]
    if participation["answered"] <= 4:
        return False

    course_code = stats["course"]["code"]
    course_name = stats["course"]["name"]
    semester = stats["course"]["semester"]
    language = stats["language"]
    participation_string = get_participation_string(participation, language)

    with open(summary_path,'r') as f:
        summary = f.read()
    summary = summary.replace("</p>\n</blockquote>", "</blockquote>")
    summary = summary.replace("<blockquote>\n<p>", "<blockquote>")

    general_questions = get_general_questions()
    general_question = None
    for q in general_questions:
        if q in stats["questions"]:
            general_question = q
            break
    if not general_question:
        print("Could not find general question for {}".format(output_path))

    general_average_text = stats["questions"][general_question]["average_text"]
    course_url = "https://www.uio.no/studier/emner/matnat/ifi/"+course_code

    main_contents = []
    additional_js = []
    if language == "NO":
        main_contents.append(r"<h2>Vurdering:</h2>")
        main_contents.append(r"Velg spørsmål for å se data fra studentenes vurdering:<br />")
    else:
        main_contents.append(r"<h2>Assessment:</h2>")
        main_contents.append(r"Choose a question to see data from the student assessment:<br />")

    options = []
    questions = []
    for question, question_stats in stats["questions"].items():
        question_id = re.sub('[^a-z]+', '', question.lower())
        chart_id = 'chart_' + question_id
        questions.append('''
            <div id="{question_id}" class="question">
                <h4>{question_label}: {question}</h4>
                <p>{average_label}: {average}</p>
                <div id="{chart_id}" class="d3kk-chart"></div>
            </div>
        '''.format(
            question_id=question_id,
            question_label='Spørsmål' if language == "NO" else 'Question',
            question=question,
            average_label='Gjennsomsnittlig svar' if language == "NO" else 'Average answer',
            average=question_stats["average_text"],
            chart_id=chart_id
        ))
        additional_js.append(create_chart_js(question, question_stats, scales, chart_id))
        options.append('<option value="{}">{}</option>'.format(question_id, question))

    main_contents.append('<select id="select_question" onchange="show_selected_question();">')
    main_contents.extend(options)
    main_contents.append('</select>')
    main_contents.append('''
        <button id="button_show_all_questions" onclick="show_all_questions();">{}</button>
        <button id="button_hide_all_questions" onclick="show_all_questions();">{}</button>
    '''.format(
        'Vis alle' if language == "NO" else 'Show all',
        'Skjul' if language == "NO" else 'Hide'
    ))
    main_contents.extend(questions)

    additional_js.append('''
        function show_selected_question() {
            var choice = document.getElementById("select_question").value;
            var questions = document.querySelectorAll('.question');
            for (var i = 0; i < questions.length; i++) {
                questions[i].hidden = true;
            }
            document.querySelector('#' + choice).hidden = false;

            document.querySelector('#button_show_all_questions').style.display = 'inline';
            document.querySelector('#button_hide_all_questions').style.display = 'none';
        }

        function show_all_questions() {
            if (!document.querySelector('.question[hidden]')) {
                show_selected_question();
                return;
            }
            var questions = document.querySelectorAll('.question');
            for (var i = 0; i < questions.length; i++) {
                questions[i].hidden = false;
            }

            document.querySelector('#button_show_all_questions').style.display = 'none';
            document.querySelector('#button_hide_all_questions').style.display = 'inline';
        }

        show_selected_question();
    ''')

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
    course_dict = courses[course_code]
    if int(current_semester[1:]) >= 2017:
        for sem in generate_semesters("V2000", "H2016"):
            if sem in course_dict:
                del course_dict[sem]

    for semester, semester_data in course_dict.items():
        # Dirty, some courses have both english and norwegian semesters:
        question_text = look_for_general_question(semester_data)
        average = semester_data[question_text]["average"]
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
    return True

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
        summary_path = path_join(summaries_path, course_code+".html")
        stat_path = path_join(stats_path, course_code+".json")
        output_path = path_join(upload_path, course_code+".html")

        res = web_report_course(summary_path, stat_path, output_path, html_templates, courses_all, scales, semester)
        if res:
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
