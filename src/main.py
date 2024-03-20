#!/usr/local/bin/python3
"""
use os package to iterate through files in a directory
"""
import os
import sys
# import time
import json
import base64
import datetime as dt


def main():
    """
    main function
    """
    if len(sys.argv) > 1:
        print("changing directory to " + sys.argv[1])
        # add error handling to chdir
        try:
            os.chdir(sys.argv[1])
        except OSError:
            print("Cannot change the current working Directory")
            sys.exit()
    else:
        print("no directory specified")
        sys.exit()

    with open("./404.html", 'w', encoding="utf-8") as f:
        f.write("""<html><head>
<meta http-equiv="content-type" content="text/html; charset=windows-1252"><title>404 Not Found</title></head>
<body>
<center><h1>404 Not Found</h1></center>
<hr><center>nginx/1.18.0 (Ubuntu)</center>


</body></html>""")

    for dirname, dirnames, filenames in os.walk('.'):
        if 'index.html' in filenames:
            print("index.html already exists, skipping...")

        else:
            print("index.html does not exist, generating")

            with open(os.path.join(dirname, 'index.html'), 'w', encoding="utf-8") as f:
                html = [
                    get_template_head(dirname),
                    '<a href="../">../</a>'
                ]

                #sort dirnames alphabetically
                dirnames.sort()
                for subdirname in dirnames:
                    html.append(gen_row(subdirname + "/", '-', '-'))
                    
                #sort filenames alphabetically
                filenames.sort()
                for filename in filenames:
                    path = (dirname == '.' and filename or dirname +
                            '/' + filename)
                    html.append(gen_row(filename, get_file_modified_time(path), get_file_size(path)))

                html.append(get_template_foot())

                f.write("\n".join(html))

def append_spaces(st, amount):
    new = st
    for i in range(0, amount - 1):
        new += '&nbsp;'
    return new

def space_date(str1, str2):
    spaces_needed = 50 - len(str1)
    
    nstr1 = append_spaces(f'<a href="{str1}">{str1}</a>', spaces_needed)
    
    result = nstr1 + str2
    
    return result

def space_size(str1, str2):
    spaces_needed = 26 - len(str1)
    
    nstr1 = append_spaces(str1, spaces_needed)
    
    result = nstr1 + ' ' + str2
    
    return result

def gen_row(name, date, size):
    return space_date(name, space_size(date, size))

def get_file_size(filepath):
    """
    get file size
    """
    size = os.path.getsize(filepath)
    if size < 1024:
        return str(size) + " B"
    elif size < 1024 * 1024:
        return str(round((size / 1024), 2)) + " KB"
    elif size < 1024 * 1024 * 1024:
        return str(round((size / 1024 / 1024), 2)) + " MB"
    else:
        return str(round((size / 1024 / 1024 / 1024), 2)) + " GB"
    return str(size)


def get_file_modified_time(filepath):
    """
    get file modified time
    """
    return dt.datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d %H:%M:%S')
    # return time.ctime(os.path.getmtime(filepath)).strftime('%X %x')


def get_template_head(foldername):
    """
    get template head
    """
    with open("/src/template/head.html", "r", encoding="utf-8") as file:
        head = file.read()
    head = head.replace("{{foldername}}", foldername[1:])
    return head


def get_template_foot():
    """
    get template foot
    """
    with open("/src/template/foot.html", "r", encoding="utf-8") as file:
        foot = file.read()
    foot = foot.replace("{{buildtime}}", "at " + dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    return foot


if __name__ == "__main__":
    main()