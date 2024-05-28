


# DO_NOT_EDIT_ANYTHING_ABOVE_THIS_LINE
fh = open("in.bib")
content = fh.read()

is_there_an_error = False
if not content.strip().startswith("@"):
    is_there_an_error = True
content_lst = content.split("@")[1:]

file_handle = open("out.html","w")
for el in content_lst:
    if el.strip()[-2:] != "\n}":
        is_there_an_error = True

def bib_to_html(a_dict, mode = True):
    number = ""
    pages = ""
    doi = ""
    authors = ""
    title = ""
    journal = ""
    year = ""
    volume = ""

    global is_there_an_error
    field_number = len(a_dict)

    for key, value in a_dict.items():
        value = value.strip()
        if field_number == 1:
            if value[-1] == ",":
                is_there_an_error = True
                return
        else:
            if value[-1] != ",":
                is_there_an_error = True
                return
            else:
                value = value[:-1]
        if (value[0] in ["{","\""]) and (value[len(value)-1] in ["}","\""]):
            if value[0] == "\"" or value[len(value)-1] == "\"":
                if value[len(value)-1] != "\"" or value[0] != "\"":
                    is_there_an_error = True
                    return
        else:
            is_there_an_error = True
            return
        field_number -= 1

        if key == "author":
            authors = value.strip("{}\",").split(" and ")
        elif key == "title":
            title = value.strip("{}\",")
        elif key == "journal":
             journal = value.strip("{}\",")
        elif key == "year":
            year = value.strip("{}\",")
        elif key == "volume":
             volume = value.strip("{}\",")
        elif key == "number":
            number = value.strip("{}\",")
        elif key == "pages":
            pages = value.strip("{}\",")
        elif key ==  "doi":
            doi = value.strip("{}\",")
        else:
            is_there_an_error = True
            return

    #check if the item contains the necessary fields
    if (authors=="" or title =="" or journal =="" or year =="" or volume ==""):
        is_there_an_error = True
        return
    #check author only contains alphabetic characters, whitespaces and dots (.)

    for check_name in authors:
        check_name_lst = check_name.split(",")
        for words in check_name_lst:
            for ch in words:
                if not(ch.isalpha() or ch == " " or ch =="."):
                    is_there_an_error = True
                    return
    #check title only contains alphanumeric characters, whitespaces and the symbols comma (,), dot (.), underscore (_) dash (-), star (*), equals (=), colon (:)
    for c_title in title:
        if not(c_title.isalnum() or (c_title in [" ",",",".","_","-","*","=",":"])):
            is_there_an_error = True
            return
    #check journal only contains alphanumeric characters, whitespaces and the symbols comma (,), dot (.), underscore (_)
    for c_journal in journal:
        if not(c_journal.isalnum() or c_journal in[" ",",",".","_"]):
            is_there_an_error = True
            return
    #check year is a 4 digit positive number where it is a valid year (starts with either 1 or 2)
    try:
        if not(int(year) < 3000 and int(year) >=1000):
            is_there_an_error = True
            return
    except:
        is_there_an_error = True
        return
    #check volume is a positive number
    try:
        if not(int(volume) > 0):
            is_there_an_error = True
            return
    except:
        is_there_an_error = True
        return
    #check number is a positive number.
    if number != "":
        try:
            if not(int(number) > 0):
                is_there_an_error = True
                return
        except:
            is_there_an_error = True
            return
    #check pages have the following form START--END. Values START and END are positive numbers separated by a double dash (--)
    if pages != "":
        try:
            for c_page in pages.split("--"):
                if not(int(c_page) > 0):
                    is_there_an_error = True
                    return
        except:
            is_there_an_error = True
            return
    #check doi has he following form PREFIX/SUFFIX. Values PREFIX and SUFFIX are separated by a forward slash (/) and may only contain alphanumeric characters and dot (.).
    if doi != "":
        try:
            if not "/" in doi:
                is_there_an_error = True
                return

            for c_doi in doi.split("/"):
                for ch_doi in c_doi:
                    if not(ch_doi.isalnum() or ch_doi == "."):
                        is_there_an_error = True
                        return
        except:
            is_there_an_error = True
            return

    all_authors = ""

    if len(authors) > 1:
        for names in authors[:-1]:
            name_lst = names.strip().split(",")
            all_authors = all_authors + name_lst[1] + " " + name_lst[0] + ","
        last_author = authors[-1].strip().split(",")
        all_authors = all_authors[:-1] + " and" + last_author[1] + " " + last_author[0] + ","
    else:
        for names in authors:
            name_lst = names.strip().split(",")
            all_authors = all_authors + name_lst[1] + " " + name_lst[0] + ","

    pages_lst = pages.split("--")
    pages = "-".join(pages_lst)

    if mode:
        file_handle.write(f"<br> <center> <b> {year} </b> </center>\n<br>\n[J{i}]{all_authors} <b>{title}</b>, <i>{journal}</i>, {volume}")
        if number != "": file_handle.write(f":{number}")
        if pages != "": file_handle.write(f", pp. {pages}")
        file_handle.write(f", {year}.")
        if doi != "": file_handle.write(f" <a href=\"https://doi.org/{doi}\">link</a>")
        file_handle.write(" <br>\n")
    else:
        file_handle.write(f"<br>\n[J{i}]{all_authors} <b>{title}</b>, <i>{journal}</i>, {volume}")
        if number != "":file_handle.write(f":{number}")
        if pages != "":file_handle.write(f", pp. {pages}")
        file_handle.write(f", {year}.")
        if doi != "":file_handle.write(f" <a href=\"https://doi.org/{doi}\">link</a>")
        file_handle.write(" <br>\n")

year_dict ={}
unique_keys = []
dict_lst = []
i = len(content_lst)

for item in content_lst:
    field_names = {}
    new_item = []
    field_dct = {}
    item = item.split("\n")
    unique_keys.append(item.pop(0))

    for field in item:
        if field == "" or field == "}":
            continue
        elif "=" not in field:
            is_there_an_error = True
            break
        else:
            field_list = []
            field = field.strip(" ")
            field_list.append(field[:field.find("=")])
            field_list.append(field[field.find("=") + 1:])
            field_names[field_list[0]] = field_names.get(field_list[0], 0) + 1
            if field_list[1] == "":
                is_there_an_error = True
                break
            for value2 in field_names.values():
                if value2 > 1:
                    is_there_an_error = True
                    break

            field_dct[field_list[0].strip()] = field_list[1].strip()
    dict_lst.append(field_dct)
    try:
        year_dict[field_dct.get("year").strip("{}\"")] = int(year_dict.get(field_dct.get("year").strip("{}\""), 0)) + 1
    except:
        is_there_an_error =True

real_unique_keys = []
for key in unique_keys:
    real_unique_keys.append(key.split("{")[1].strip(" ,"))
    if key.split("{")[0] != "article":
        is_there_an_error = True
#check UNIQKEY is unique and contains only alphanumeric characters
for unikey in real_unique_keys:
    if not unikey.isalnum():
        is_there_an_error = True
        break
comparison_lst = []
for unikey2 in real_unique_keys:
    if unikey2 in comparison_lst:
        is_there_an_error = True
    else:
        comparison_lst.append(unikey2)


while not is_there_an_error:
    file_handle.write("<html>\n")
    for times,el in sorted(year_dict.items())[::-1]:
        compare_lst = []
        mode = True
        for sub_dict1 in dict_lst:
            if sub_dict1.get("year").strip("{}\"") == times:
                compare_lst.append(sub_dict1["title"])
        for titles in sorted(compare_lst):
            for items in dict_lst:
                if items["title"] == titles:
                    bib_to_html(items,mode=mode)
                    i -= 1
                    if el > 1:
                        mode = False
    file_handle.write("</html>")
    break
file_handle.close()

if is_there_an_error:
    new_handle = open("out.html","w")
    new_handle.write("Input file in.bib is not a valid .bib file!")
    new_handle.close()
fh.close()
# DO_NOT_EDIT_ANYTHING_BELOW_THIS_LINE


