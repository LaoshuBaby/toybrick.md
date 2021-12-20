import json
import os.path
import sys
from functools import cmp_to_key
from pprint import pprint

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


def markdown_entry(row_entry: dict):
    data = [
        row_entry["package_name"],
        row_entry["institution_name"],
        row_entry["maintainer_type"],
        row_entry["github_repository"],
        row_entry["gitlab_repository"],
        row_entry["gitee_repository"],
        row_entry["ctan_package"],
        row_entry["status"],
    ]
    return markdown_row(len(data), data)


def markdown_body(length, data, locale: str):
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


def page_gen(readme_locale):
    # 确定文件名
    if readme_locale != "":
        path = "..\\README" + "-" + readme_locale + ".md"
    else:
        readme_locale = "Default"
        path = "..\\README.md"
    # 读取原始文件
    readme_file = open(path, "r", encoding="utf-8")
    readme_text = readme_file.read()
    readme_file.close()
    # 把原始文件发送给生成函数（可能未来逐步分生成会在这里累积多层）
    readme_text = markdown_gen(
        readme_locale, readme_text, syntax_1, syntax_2, syntax_3
    )
    # 写回文件
    readme_file = open(path, "w", encoding="utf-8")
    readme_file.write(readme_text)
    readme_file.close()
    print(readme_locale, ": ", path.replace("..\\", "").replace("../", ""))


def build():
    # 未来build或许可以根据参数或者配置文件来队列生成
    page_gen("")
    page_gen("zh-CN")
    page_gen("en-US")
    return 0


def gen_id(content_type="table", content_name=""):
    if content_name == "":
        content_name = input("请输入数据名称：")
    data_file = open(
        os.path.join(
            __file__.replace("main.py", ""),
            "..",
            "data",
            content_type,
            content_name,
            "data.json",
        ),
        "r",
        encoding="utf-8",
    )
    column_file = open(
        os.path.join(
            __file__.replace("main.py", ""),
            "..",
            "data",
            content_type,
            content_name,
            "column.json",
        ),
        "r",
        encoding="utf-8",
    )
    data_json=json.loads(data_file.read())
    column_json=json.loads(column_file.read())
    # pprint(data_json)
    schema_id=column_json["schema_id"]
    # print(data_json[schema_id][0]["entry_id"])
    def random_id(x:int):
        # 生成6位随机字符串
        import uuid
        return str(uuid.uuid4()).replace("-", "").upper()[:x]
    for i in range(len(data_json[schema_id])):
        data_json[schema_id][i]["entry_id"]=schema_id+"-"+random_id(6)
    data_file.close()
    data_file = open(
        os.path.join(
            __file__.replace("main.py", ""),
            "..",
            "data",
            content_type,
            content_name,
            "data.json",
        ),
        "w",
        encoding="utf-8",
    )
    # data_file.write(json.dumps(data_json, ensure_ascii=False, indent=4))
    data_file.write(json.dumps(data_json, ensure_ascii=False, indent=4))
    data_file.close()
    return 0


###### MAIN
if __name__ == "__main__":
    argument_dict = {"MODE": "NULL"}
    status = "VALUE"
    for i in range(len(sys.argv)):
        if status == "NAME":
            if (i != 0) and (i + 1 <= len(sys.argv) - 1):
                argument_dict.update(
                    {
                        sys.argv[i]
                        .replace("--", "")
                        .upper(): sys.argv[i + 1]
                        .upper()
                    }
                )
            elif i != 0:
                argument_dict.update(
                    {sys.argv[i].replace("--", "").upper(): "NULL"}
                )
            else:
                argument_dict.update({"path": sys.argv[i]})
            status = "VALUE"
        else:
            status = "NAME"
    print(argument_dict)
    # MODE
    if argument_dict["MODE"] == "FULL_BUILD":
        temp_return = build()
    elif argument_dict["MODE"] == "SINGLE_LANGUAGE":
        temp_return = 1
    elif argument_dict["MODE"] == "DATA_GEN_ID":
        temp_return = gen_id()
    else:
        temp_return = 0

# 这段异常退出分析是对GUI和CLI共用的
if temp_return == "ERROR_NONEXIST_LOCALE":
    print("退出原因：不存在的语言")
exit(0)
