import json
from functools import cmp_to_key

syntax_1 = "<!-- MARKDOWN_TABLE BEGIN -->"
syntax_2 = "<!-- WARNING: THIS TABLE IS MAINTAINED BY PROGRAMME, YOU SHOULD ADD DATA TO COLLECTION JSON -->"
syntax_3 = "<!-- MARKDOWN_TABLE END -->"


def x_sort(data):
    def compare(dict_a: dict, dict_b: dict):
        dict_a_packagename = (
            dict_a["package_name"].replace("_", "").replace("-", "").lower()
        )
        dict_b_packagename = (
            dict_b["package_name"].replace("_", "").replace("-", "").lower()
        )
        dict_a_ctan = dict_a["ctan_package"]
        dict_b_ctan = dict_b["ctan_package"]
        if dict_a_ctan == "" and dict_b_ctan == "":
            if dict_a_packagename < dict_b_packagename:
                return -1
            if dict_a_packagename > dict_b_packagename:
                return 1
        elif dict_a_ctan == "" and dict_b_ctan != "":
            return 1
        elif dict_b_ctan == "" and dict_a_ctan != "":
            return -1
        else:
            if dict_a_packagename < dict_b_packagename:
                return -1
            if dict_a_packagename > dict_b_packagename:
                return 1

    data = sorted(data, key=cmp_to_key(compare))
    return data


def markdown_row(length: int, data: list):
    string = ""
    for i in range(length):
        string += "| " + str(data[i]) + " "
    string += "|\n"
    return string


def markdown_header(translation: dict, locale: str):
    locale_translation = {}
    for i in range(len(translation)):
        if translation[i]["locale"] == locale:
            locale_translation = translation[i]["translation"]
    data = [
        locale_translation["package_name"],
        locale_translation["institution_name"],
        locale_translation["maintainer_type"],
        locale_translation["github_repository"],
        locale_translation["gitlab_repository"],
        locale_translation["gitee_repository"],
        locale_translation["ctan_package"],
        locale_translation["status"],
    ]
    return markdown_row(len(data), data)


def markdown_table(length: int):
    data = ["-", "-", "-", "-", "-", "-", "-", "-"]
    return markdown_row(length, data)


def markdown_entry(thesis_entry: dict):
    data = [
        thesis_entry["package_name"],
        thesis_entry["institution_name"],
        thesis_entry["maintainer_type"],
        thesis_entry["github_repository"],
        thesis_entry["gitlab_repository"],
        thesis_entry["gitee_repository"],
        thesis_entry["ctan_package"],
        thesis_entry["status"],
    ]
    return markdown_row(len(data), data)


def markdown_body(length,data,locale: str): 
    thesis_json = open("..\\data\\thesis.json", "r", encoding="utf-8")
    thesis_data = json.loads(thesis_json.read())["CUTI"]
    column_json = open("..\\data\\column.json", "r", encoding="utf-8")
    column_data = json.loads(column_json.read())
    string = ""
    if locale != "Default":
        string += markdown_header(column_data["i18n"], locale)
    else:
        string += markdown_header(column_data["i18n"], "zh-CN")
    string += markdown_table(
        column_data["len"],
    )
    # WRONG CODE: thesis_data.sort(key=lambda x: x["package_name"])
    thesis_data = x_sort(thesis_data)
    for i in range(len(thesis_data)):
        string += markdown_entry(thesis_data[i])
    return string


def markdown_gen(locale, text, token_begin, token_warn, token_end):
    readme_slice = text.split(token_begin)
    readme_slice.append(readme_slice[1].split(token_warn)[0])
    readme_slice.append(readme_slice[1].split(token_end)[1])
    table = markdown_body(locale)
    markdown = (
        readme_slice[0]
        + token_begin
        + "\n"
        + token_warn
        + "\n"
        + table
        + "\n"
        + token_end
        + readme_slice[3]
    )
    if table == "":
        return text
    else:
        return markdown


def readme_gen(readme_locale):
    if readme_locale != "":
        path = "..\\README" + "-" + readme_locale + ".md"
    else:
        readme_locale = "Default"
        path = "..\\README.md"
    readme_file = open(path, "r", encoding="utf-8")
    readme_text = readme_file.read()
    readme_file.close()
    readme_text = markdown_gen(
        readme_locale, readme_text, syntax_1, syntax_2, syntax_3
    )
    readme_file = open(path, "w", encoding="utf-8")
    readme_file.write(readme_text)
    readme_file.close()
    print(readme_locale, ": ", path.replace("..\\", "").replace("../", ""))


readme_gen("")
readme_gen("zh-CN")
readme_gen("en-US")


###### MAIN
if __name__ == '__main__':
    ARGUMENT_DICT = {"MODE": "NULL"}
    STATUS = "VALUE"
    for i in range(len(sys.argv)):
        if STATUS == "NAME":
            if (i != 0) and (i + 1 <= len(sys.argv) - 1):
                ARGUMENT_DICT.update({sys.argv[i].replace("--", "").upper(): sys.argv[i + 1].upper()})
            elif i != 0:
                ARGUMENT_DICT.update({sys.argv[i].replace("--", "").upper(): "NULL"})
            else:
                ARGUMENT_DICT.update({"path": sys.argv[i]})
            STATUS = "VALUE"
        else:
            STATUS = "NAME"
    print(ARGUMENT_DICT)
    # 三千参数，我只取MODE饮
    if ARGUMENT_DICT["MODE"] == "CLI":
        while True:
            print("==请输入您希望进入的模式==")
            GLOBAL_MODE = input()
            if eval(GLOBAL_MODE) == 1:
                TEMP_RETURN = MODE_CREATE()
            elif eval(GLOBAL_MODE) == 2:
                TEMP_RETURN = MODE_INPUT()
            elif eval(GLOBAL_MODE) == 3:
                TEMP_RETURN = MODE_MERGE()
            else:
                TEMP_RETURN = 0
                print("EXIT")
                break
    # elif ARGUMENT_DICT["mode"] == "GUI":
    else:
        GLOBAL_MODE = "GUI_0"
        TEMP_RETURN = 0

# 这段异常退出分析是对GUI和CLI共用的
if GLOBAL_MODE == 1 and TEMP_RETURN == "ERROR_NONEXIST_QUANTITY":
    print("退出原因：不存在的数量")
if GLOBAL_MODE == 2 and TEMP_RETURN == "ERROR_NONEXIST_QUANTITY":
    print("退出原因：不存在的数量")
if GLOBAL_MODE == 3 and TEMP_RETURN == "ERROR_NONEXIST_QUANTITY":
    print("退出原因：不存在的数量")
quit(0)