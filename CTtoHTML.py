#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, subprocess, shutil
import argparse # parse the command line parameters

def find(name, path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if name in file:
                return os.path.join(root, file)
    return ""

def split_artikle_heading(line):
    article_heading = ""
    numbers = []
    for part in line.split(" "):
        try:
            number = int(part.replace(",",""))
            if number > 1000000000000:
                numbers.append(str(number))
            else:
                article_heading = "%s %s" % (article_heading, part)
        except ValueError as e:
            article_heading = "%s %s" % (article_heading, part)
    return (article_heading.strip(), numbers)

def create_article(line):
    article_heading, numbers = split_artikle_heading(line)
    if len(numbers) == 0:
        return ""
    if find(numbers[0], ct_folder) == "":
        return ""
    folder_name = os.path.dirname( find(numbers[0], ct_folder) )
    article_content = ""
    for root, dirs, files in os.walk(folder_name):
        for file in files:
            if file.endswith("txt"):
                contents = subprocess.check_output(["pandoc", "-t", "html", os.path.join(root, file)])
                article_content = "%s\n%s" % (article_content, contents)
        for file in files:
            if file.endswith("html"):
                contents = subprocess.check_output(["pandoc", "-t", "html", os.path.join(root, file)])
                article_content = "%s\n%s" % (article_content, contents)
    article_filename = "%s_%s.html" % (folder_name.split("/")[-1].split(" ")[0], '_'.join(numbers))
    article_file = open(os.path.join(html_folder, article_filename), "w")
    article_file.write("<!DOCTYPE html>\n\
<html lang=\"de\">\n\
<head>\n\
<meta charset=\"utf-8\">\n\
<title>%s</title>\n\
</head>\n\
<body>\n\
%s\n\
</body>\n\
</html>\n" % (article_heading, article_content))
    article_file.close()
    return "html/%s" % article_filename

##################################
# create the args parser
parser = argparse.ArgumentParser(description="CT to HTML converter")
parser.add_argument("-v", "--version", action="store_true",
                    help="Get current program version")
parser.add_argument("ctfolder", nargs="?", default="",
                    help="Specify the CT source folder")
# parse the command line arguments
args = parser.parse_args()
# version
if args.version == True:
    print "CTConverter version 0.3"
    sys.exit(0)
# ct folder
ct_folder = os.path.abspath(args.ctfolder)
if ct_folder == "":
    print "The path to the ct folder is empty"
    sys.exit(1)
if not os.path.exists(ct_folder):
    print "The folder %s does not exist" % ct_folder
    sys.exit(1)

html_folder = os.path.join(ct_folder, "html")
if os.path.exists(html_folder):
    try:
        shutil.rmtree(html_folder)
    except OSError as e:
        print "Can't remove old html folder\n%s" % e
        sys.exit(1)
try:
    os.makedirs(html_folder)
except OSError as e:
    print "Can't create html folder\n%s" % e
    sys.exit(1)

toc_foldername = ""
for file in os.listdir(ct_folder):
    if file.find("Inhaltsverzeichnis") > 0:
        toc_foldername = file
        break
if toc_foldername == "":
    print "Can't find table of contents"
    sys.exit(1)

toc_content_list = []
for f in os.listdir(os.path.join(ct_folder, toc_foldername)):
    if f.endswith(".txt"):
        toc_file = open(os.path.join(ct_folder, toc_foldername, f), 'r')
        toc_content_list.append(toc_file.read())
        toc_file.close()
if len(toc_content_list) == 0:
    print "Can't find table of contents"
    sys.exit(1)
else:
    toc = '\n\n'.join(toc_content_list)

ct_title = ct_folder.split("/")[-1].replace("_"," ")
html_toc_file = open(os.path.join(ct_folder, "index.html"), "w")
html_toc_file.write("<!DOCTYPE html>\n\
<html lang=\"de\">\n\
<head>\n\
<meta charset=\"utf-8\">\n\
<title>%s Inhaltsverzeichnis</title>\n\
</head>\n\
<body>\n\
<h1>%s</h1>\n\n" % (ct_title, ct_title))

headings = [
        "aktuell", "Magazin", "Internet", "Software", "Hardware", "Know-how",
        "Praxis", "Ständige Rubriken", "Trends & News", "Test & Kaufberatung",
        "Wissen", "Praxis & Tipps", "Rubriken"
]
found_start = False
for line in toc.split("\n"):
    line = line.strip()
    if line == "":
        continue
    if line in headings:
        if not found_start:
            html_toc_file.write("<h2>%s</h2>\n<ul>\n" % line)
            found_start = True
        else:
            html_toc_file.write("</ul>\n\n<h2>%s</h2>\n<ul>\n" % line)
        continue
    if found_start:
        article_heading, numbers = split_artikle_heading(line)
        if article_heading != "":
            article_filename = create_article(line)
            if article_filename == "" or "Inhaltsverzeichnis" in article_heading:
                html_toc_file.write("<li>%s</li>\n" % article_heading)
            else:
                html_toc_file.write("<li><a href=\"%s\">%s</a></li>\n" % (article_filename, article_heading))

html_toc_file.write("</ul>\n</body>\n</html>")
html_toc_file.close()
