#!/usr/bin/python

import json
import sys
import logging
import re
import types
import urllib
import urllib.request
import jinja2
import argparse
import site
import pathlib
from typing import Any, TypeVar
from unidiff import PatchSet
from enum import Enum

"""
This example module shows various types of documentation available for use
with pydoc.  To generate HTML documentation for this module issue the
command:

    pydoc -w NewAttribs

"""

logging.basicConfig(stream=sys.stderr, level=logging.WARNING)

def auto_str(cls):
    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )

    cls.__str__ = __str__
    return cls

class BoolType:
    pass

@auto_str
class NewAttribs:
    class Visibility(Enum):
        all = 'tag title'
        tag = 'tag'
        title = 'title'
        pass

    def __init__(self, parent):
        var = self.__update = True
        var = self.__append = False
        var = self.__noupdate = False
        var = self.nohighlight = BoolType
        var = self.__step = ''
        var = self.steps = []
        var = self.file = None
        var = self.context = None
        var = self.lang = None
        var = self.prefix = None
        var = self.suffix = None
        var = self.__visibility = self.Visibility.all
        var = self.parent_element = parent
        var = self.commits = []
        var = self.template = None
        var = self.tabs = BoolType
        var = self.t_old = None
        var = self.t_new = None
        # Pomocna premmena, ktora zabezpeci, ze v skupene spoloznych nastavení je mozne nastavit iba jedno
        var = self.oneonly_g1 = 0


    # @property
    # def t_new(self):
    #     return self.__t_new
    #
    # @t_new.setter
    # def t_new(self, value):
    #     self.__t_new = value if value is not None else None
    #
    # @property
    # def t_old(self):
    #     return self.__t_old
    #
    # @t_old.setter
    # def t_old(self, value):
    #     self.__t_old = value if value is not None else None
    #
    # @property
    # def tabs(self):
    #     return self.__tabs
    #
    # @tabs.setter
    # def tabs(self, value):
    #     self.__tabs = value if value is not None else False
    #
    # @property
    # def template(self):
    #     return self.__template
    #
    # @template.setter
    # def template(self, value):
    #     self.__template = value if value is not None else None
    #
    # @property
    # def lang(self):
    #     return self.__lang
    #
    # @lang.setter
    # def lang(self, value):
    #     self.__lang = value if value is not None else None
    #
    # @property
    # def prefix(self):
    #     return self.__prefix
    #
    # @prefix.setter
    # def prefix(self, value):
    #     self.__prefix = value if value is not None else None
    #
    # @property
    # def suffix(self):
    #     return self.__suffix
    #
    # @suffix.setter
    # def suffix(self, value):
    #     self.__suffix = value if value is not None else None

    @property
    def visibility(self):
        return self.__visibility

    @visibility.setter
    def visibility(self, value):
        try:
            self.__visibility = self.Visibility[value]
        except KeyError as err:
            a = [(str(v.name)) for v in self.Visibility]
            raise InputError('', ' \n\tWrong visibility parameter: ' + str(err) + ' Allowed parameters: '
                             + str(a))

    # @property
    # def context(self):
    #     return self.__context
    #
    # @context.setter
    # def context(self, value):
    #     self.__context = value if value is not None else None
    
    @property
    def update(self):
        return self.__update

    @update.setter
    def update(self, value):
        self.__update = value if value is not None else True
        self.oneonly_g1 += 1
        if self.oneonly_g1 > 1:
            raise InputError('', 'Only one variable can be set')

    # @property
    # def nohighlight(self):
    #     return self.__nohighlight
    #
    # @nohighlight.setter
    # def nohighlight(self, value):
    #     self.__nohighlight = value if value is not None else True

    @property
    def append(self):
        return self.__append

    @append.setter
    def append(self, value):
        self.__append = value if value is not None else True
        self.oneonly_g1 += 1
        if self.oneonly_g1 > 1:
            raise InputError('', 'Only one variable can be set')

    @property
    def noupdate(self):
        return self.__noupdate


    @noupdate.setter
    def noupdate(self, value):
        self.__noupdate = value if value is not None else True
        self.oneonly_g1 += 1
        if self.oneonly_g1 > 1:
            raise InputError('', 'Only one variable can be set')

    @property
    def step(self):
        return self.__step

    @step.setter
    def step(self, value):
        if value != 'all':
            if value.find('-') > 0:
                self.steps = value.split('-')
                try:
                    self.steps[0] = [int(_) for _ in self.steps[0].split(".")]
                    self.steps[1] = [int(_) for _ in self.steps[1].split(".")]
                except ValueError as err:
                    raise InputError('', str(
                        err) + ' \n\tCannot convert commit tag to list of integers: ' + self.step)
                self.__step = 'range'
            elif value.find(',') > 0:
                self.steps = value.split(',')
                self.__step = 'list'
            else:
                self.__step = value
        else:
            self.__step = value

    # @property
    # def file(self):
    #     return self.__file
    #
    # @file.setter
    # def file(self, value):
    #     self.__file = value if value is not None else True
        
    
    @staticmethod
    def instance(attribs, parent):
        new_attribs = NewAttribs(parent)
        for i, attribTuple in enumerate(attribs, start=1):
            attrib = [None] * 2
            attrib[0] = attribTuple[0]
            attrib[1] = attribTuple[2] + attribTuple[4]
            try:
                if attrib[1] == '' or attrib[1] is None:
                    if isinstance(getattr(new_attribs, attrib[0]), BoolType.__class__) or isinstance(getattr(new_attribs, attrib[0]), bool):
                        attrib[1] = True
                    else:
                        attrib[1] = getattr(new_attribs, attrib[0], None)

                elif attrib[1].lower() == 'false':
                    attrib[1] = False
                setattr(new_attribs, attrib[0], attrib[1])
            except AttributeError as err:
                raise InputError('', ' \n\t' + str(err))

        return new_attribs


    def isInRange(self, step):
        if step.lower() == 'ignore':
            # If commit is tagged as ignore that ignore it
            return False
        elif self.step == 'all':
            return True
        elif self.step == 'range':
            try:
                list_int = [int(_) for _ in step.split(".")]
            except ValueError as err:
                raise InputError('', str(err) + ' \n-------Cannot convert commit tag to list of integers: ' + step)
            return self.steps[0] <= list_int <= self.steps[1]
        elif self.step == 'list':
            for __step in self.steps:
                if __step == step:
                    return True
            return False
        else:
            return self.step == step


# @auto_str
# class Attribs:
#
#     class Visibility(Enum):
#         all = 'tag title'
#         tag = 'tag'
#         title = 'title'
#         pass
#
#     def __init__(self, attribs, parent_element):
#         if not attribs:
#             raise InputError('', 'Missing basic attribute (tag or file)!')
#
#         var = self.update = True
#         var = self.append = False
#         var = self.noupdate = False
#         var = self.nohighlight = False
#         var = self.step = ''
#         var = self.steps = []
#         var = self.file = None
#         var = self.context = None
#         var = self.lang = ''
#         var = self.prefix = None
#         var = self.suffix = None
#         var = self.visibility = self.Visibility.all
#         var = self.parent_element = parent_element
#         var = self.commits = []
#         var = self.template = None
#         var = self.tabs = None
#         var = self.t_old = None
#         var = self.t_new = None
#         single_one = 0
#
#         for i, attribTuple in enumerate(attribs, start=1):
#             attrib = [None] * 2
#             attrib[0] = attribTuple[0]
#             attrib[1] = attribTuple[2] + attribTuple[4]
#             if i == 1:
#                 if attrib[0] == 'tag':
#                     self.step = attrib[1]
#                     if self.step != 'all':
#                         if self.step.find('-') > 0:
#                             self.steps = self.step.split('-')
#                             try:
#                                 self.steps[0] = [int(_) for _ in self.steps[0].split(".")]
#                                 self.steps[1] = [int(_) for _ in self.steps[1].split(".")]
#                             except ValueError as err:
#                                 raise InputError('', str(
#                                     err) + ' \n\tCannot convert commit tag to list of integers: ' + self.step)
#                             self.step = 'range'
#                         elif self.step.find(',') > 0:
#                             self.steps = self.step.split(',')
#                             self.step = 'list'
#                 elif attrib[0] == 'file':
#                     self.file = attrib[1]
#                 else:
#                     raise InputError('', 'Missing basic attribute (tag or file)!')
#             else:
#                 if attrib[0] == 'update':
#                     single_one += 1
#                     self.update = True
#                 elif attrib[0] == 'append':
#                     single_one += 1
#                     self.append = True
#                 elif attrib[0] == 'noupdate':
#                     single_one += 1
#                     self.noupdate = True
#                 elif attrib[0] == 'nohllines':
#                     self.nohighlight = True
#                 elif attrib[0] == 'prefix':
#                     self.prefix = attrib[1]
#                 elif attrib[0] == 'suffix':
#                     self.suffix = attrib[1]
#                 elif attrib[0] == 'lang':
#                     self.lang = attrib[1]
#                 elif attrib[0] == 't_old':
#                     self.lang = attrib[1]
#                 elif attrib[0] == 't_new':
#                     self.lang = attrib[1]
#                 elif attrib[0] == 'template':
#                     self.template = attrib[1]
#                 elif attrib[0] == 'visibility':
#                     try:
#                         self.visibility = self.Visibility[attrib[1]]
#                     except KeyError as err:
#                         a = [(str(v.name)) for v in self.Visibility]
#                         raise InputError('', ' \n\tWrong visibility parameter: ' + str(err) + ' Allowed parameters: '
#                                          + str(a))
#
#                 elif attrib[0] == 'context':
#                     self.context = attrib[1]
#                 else:
#                     raise InputError('', 'Wrong attribute: ' + attrib[0])
#
#         if single_one > 1:
#             raise InputError('', 'Ambiguous use of attributes update, append, noupdate')
#
#     def isInRange(self, step):
#         if step.lower() == 'ignore':
#             # If commit is tagged as ignore that ignore it
#             return False
#         elif self.step == 'all':
#             return True
#         elif self.step == 'range':
#             try:
#                 list_int = [int(_) for _ in step.split(".")]
#             except ValueError as err:
#                 raise InputError('', str(err) + ' \n-------Cannot convert commit tag to list of integers: ' + step)
#             return self.steps[0] <= list_int <= self.steps[1]
#         elif self.step == 'list':
#             for __step in self.steps:
#                 if __step == step:
#                     return True
#             return False
#         else:
#             return self.step == step


class Error(Exception):
    pass


class InputError(Error):

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


class Commit:
    tag: str
    msg: str
    hash: str
    diff: None
    remoteUrl: str
    fileList:str

    def __init__(self, commitTag: str, commitMsg: str, commitHash: str, commitDiff: str, remoteUrl: str, fileList: str) -> None:
        self.tag = commitTag
        self.msg = commitMsg
        self.hash = commitHash
        self.diff = commitDiff
        self.remoteUrl = remoteUrl
        self.fileList = fileList

    @staticmethod
    def from_dict(obj: Any) -> 'CommitElement':
        assert isinstance(obj, dict)
        commitTag = from_str(obj.get("commitTag"))
        commitMsg = from_str(obj.get("commitMsg"))
        commitHash = from_str(obj.get("commitHash"))
        commitDiff = from_str(obj.get("commitDiff"))
        remoteUrl = from_str(obj.get("remoteUrl"))
        fileList = from_str(obj.get("fileList"))
        return Commit(commitTag, commitMsg, commitHash, commitDiff, remoteUrl, fileList)


class ContextResource:
    class DefaultValues:
        def __init__(self):
            # Set default values for all contexts
            self.context = None
            self.lang = None
            self.tabs = False
            self.t_old = 'Old'
            self.t_new = 'New'
            self.prefix = None
            self.suffix = None
            self.nohighlight = False

        def dump_values(self, attribs: NewAttribs):
            for item in vars(self).items():
                value = getattr(attribs, str(item[0]), None)
                if value is not None and not isinstance(value, BoolType.__class__) :
                    setattr(self, str(item[0]), value)

        def load_values(self, attribs: NewAttribs):
            for item in vars(self).items():
                value = getattr(self, str(item[0]), None)
                valueAttib = getattr(attribs, str(item[0]), None)
                # Copy context value only if attrib is not set
                if valueAttib is None or isinstance(valueAttib, BoolType.__class__) :
                    setattr(attribs, str(item[0]), value)

    pass

    url = ''
    encoding = 'UTF-8'
    commits = None
    template = ''
    default_values = DefaultValues()

    def __init__(self, url=None, encoding='UTF-8', template=None):
        self.url = url
        self.encoding = encoding
        self.template = template
        self.inputDiff = ''
        assert url is not None
        if re.match(r"\s?(http|https):\/\/.*", url, re.M):
            # assert not "Zatial tato funkcianlita nie je prerobena na json"
            http_diff = urllib.request.urlopen(url)
            regex = r"charset *= *([^; ]+)"
            reg_str = http_diff.headers['Content-Type']
            self.encoding = re.findall(regex, reg_str, re.MULTILINE)[0]
            self.inputDiff = http_diff.read()
            # self.commits = PatchSet(http_diff, encoding=self.encoding)

        else:
            try:
                file = open(url, "r", encoding=self.encoding)
                self.inputDiff = file.read()
                file.close()
            except FileNotFoundError as e:
                raise InputError('', "File Not found")
        self.commits = json.loads(self.inputDiff, encoding=self.encoding, object_hook=lambda a: Commit.from_dict(a))
        for index, commit in enumerate(self.commits):
            try:
                self.commits[index].diff = PatchSet.from_string(commit.diff.encode(), encoding=encoding)

            except Exception as e:
                pass
                raise InputError("", "Wrong patch format!")

    pass


def find_patch(attribs, commits):
    for commit in commits:
        if attribs.isInRange(commit.tag):
            attribs.commits.append(commit)
    return


def log_error(message, tag_, data_in):
    count = len(data_in[0:tag_.start()].split('\n'))
    logging.error("Error occurred at line {start}: {match} \n-->Error message: {msg} ".format(start=count
                                                                                              , match=tag_.group()
                                                                                              , msg=message))


def log_warring(message, tag_, data_in):
    count = len(data_in[0:tag_.start()].split('\n'))
    logging.warning("Warring at line {start}: {match} \n-->Error message: {msg} ".format(start=count
                                                                                         , match=tag_.group()
                                                                                         , msg=message))
def main():

    cliParser = argparse.ArgumentParser(description='Generate code snippets from diff file')
    cliParser.add_argument('infile', metavar='infile', type=str, nargs=1, help='Input file  to process')
    cliParser.add_argument('outfile', metavar='outfile', type=str, nargs='?', help='Output file')
    cliParser.add_argument('-d', '--diff_file', metavar='diff_file', type=str, nargs='?', help='Git diff file/url')
    cliParser.add_argument('-e', '--encoding', metavar='encoding', type=str, nargs='?', help='Encodning', default='UTF-8')
    cliParser.add_argument('-t', '--template', metavar='template', type=str, nargs='?', help='Template file', default='mkdocs.jinja')
    args = cliParser.parse_args()
    
    # TEMPLATE_DIR = str(pathlib.Path.home().joinpath('.local/TutGen/templates/'))
    site.getuserbase();
    TEMPLATE_DIR = str(site.USER_BASE + '/TutGen/templates/')
    print(TEMPLATE_DIR)
    TEMPLATE_FILE = 'mkdocs.jinja'
    MAIN_CONTEXT = 'MAIN_CONTEXT'
    # DIFF_CONTEXT = \
    #     {MAIN_CONTEXT: ContextResource('/home/martin/AndroidStudioProjects/ActivityTutorial//tutorial.multi.patch')}

    if args.diff_file is not None:
        DIFF_CONTEXT = {MAIN_CONTEXT: ContextResource(args.diff_file, args.encoding, args.template)}
    else:
        DIFF_CONTEXT = {MAIN_CONTEXT: None}

    INPUT_FILE = args.infile[0]
    if args.outfile is None:
        OUTPUT_FILE = INPUT_FILE
    else:
        OUTPUT_FILE = args.outfile



    # Set up jinja templates. Look for templates in the TEMPLATE_DIR
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR))

    # http = urllib.request
    # diff = http.urlopen('https://github.com/matiasb/python-unidiff/pull/3.diff')
    # regex = re.compile(r"charset *= *([^; ]+)", re.MULTILINE)
    # regex = r"charset *= *([^; ]+)"
    # reg_str = diff.headers['Content-Type']
    # encoding = re.findall(regex, reg_str, re.MULTILINE)[0]
    # patch = PatchSet(diff, encoding=encoding)

    # diff_file = PatchSet.from_filename('/home/martin/AndroidStudioProjects/ActivityTutorial//tutorial.multi.patch', encoding='utf-8')

    # print(patch[0])

    try:
        with open(INPUT_FILE, "r") as file:
            data_in = file.read()
            data_out = data_in
            file.close()
    except FileNotFoundError:
        logging.error("Can't open input file. File not found: " + INPUT_FILE)
        sys.exit(1)

    regExprTags = re.compile(r"<!--tgen.(.*?)-->", re.DOTALL)
    # regExprAttrib = re.compile(r'(\w+)=?(.*?)(?= \w+=?|$)', re.S)
    regExprAttrib = re.compile(r"(\w+)=?('|\")?(?(2)(.*?)('|\")|(\S*))(?= \w+=?|$)", re.S)
    # tags = regExpr.findall(data)

    # Iba na Testovanie chyb regexu
    # data = "1\n2\n3\n4\n<!--tgen file=\\home\\martin.diff context=tut1/2 noupdate -->\n6\n7\n8\n9\n" \
    #        "<!--tgen -->"
    var = attribList = []
    interElements = regExprTags.finditer(data_in)

    for matchNum, elementGroups in enumerate(interElements, start=1):

        logging.debug("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum=matchNum, start=elementGroups.start(),
                                                                           end=elementGroups.end(), match=elementGroups.group()))

        element = elementGroups.group(1)

        # if attrib is None:
        #     raise Exception('No attribute found', 'Not found')
        element = " ".join(element.split())  # get rid of all the duplicate whitespaces and newline characters
        element = element.replace(" =", "=")
        element = element.replace("= ", "=")

        attribs_str = regExprAttrib.findall(element)
        # attribs = re.findall(r'(\w+)=?(.*?)(?= \w+=?|$)', attrib, re.S)

        # Process founded attribute string
        try:
            # attribs = Attribs(attribs_str, elementGroups)
            attribs = NewAttribs.instance(attribs_str, elementGroups)
        except InputError as e:
            log_error(e.message, elementGroups, data_in)
            sys.exit(1)

        # Load file
        if attribs.file is not None:
            # Process element with file attribute
            if attribs.context is None:
                try:
                    DIFF_CONTEXT[MAIN_CONTEXT] = ContextResource(attribs.file, template=attribs.template)
                    DIFF_CONTEXT[MAIN_CONTEXT].default_values.dump_values(attribs)
                except InputError as e:
                    log_error(e.message, elementGroups, data_in)
                    sys.exit(1)
            else:
                if attribs.context in DIFF_CONTEXT:
                    log_warring("Context: {context} have already opened file: {file}".format(context=attribs.context,file=DIFF_CONTEXT[attribs.context].url), elementGroups,data_in)
                try:
                    DIFF_CONTEXT[attribs.context] = ContextResource(attribs.file, template=attribs.template)
                    DIFF_CONTEXT[attribs.context].default_values.dump_values(attribs)
                except Exception as e:
                    log_error("File {file} is not found: \n{exc}".format(file=attribs.file, exc=str(e)), elementGroups, data_in)
                    sys.exit(1)
        else:
            # Continue to process parsed attribs:
            if attribs.context is None:
                # context was not specified use MAIN_CONTEXT
                try:
                    commit = DIFF_CONTEXT[MAIN_CONTEXT].commits
                    TEMPLATE_FILE = DIFF_CONTEXT[MAIN_CONTEXT].template
                    DIFF_CONTEXT[MAIN_CONTEXT].default_values.load_values(attribs)
                except Exception:
                    log_error("For main context there is no diff file defined: \n".format(file=attribs.file), elementGroups, data_in)
                    sys.exit(1)
            else:
                # context was specified use it
                try:
                    commit = DIFF_CONTEXT[attribs.context].commits
                    TEMPLATE_FILE = DIFF_CONTEXT[attribs.context].template
                    DIFF_CONTEXT[attribs.context].default_values.load_values(attribs)
                except Exception as e:
                    log_error("Context: {context} has no open file: \n{exc}".format(context=attribs.context, exc=str(e)), elementGroups, data_in)
                    sys.exit(1)

            # Process the attributes
            try:
                # Connect attribute step with patch content
                find_patch(attribs, commit)
            except InputError as err:
                logging.warning(err.message)
                pass
            # logging.debug(attribCurr.__dict__)
            # Get the template and render it to a string. Pass table in as a var called table.

            if TEMPLATE_FILE is None:
                if attribs.template is not None:
                        TEMPLATE_FILE = attribs.template
                else:
                        TEMPLATE_FILE = args.template

            gen_text = env.get_template(TEMPLATE_FILE).render(element=attribs)
            logging.debug(gen_text)
            sub_reg = r"(" + attribs.parent_element.group() + r"\s?)(.*?)(<!--end-->)"

            if attribs.template == "gen_tags.jinja":
                subst = "\\1" + "\\3\n" + gen_text
            else:
                # Nahradenie casti za vygenerovane kody
                if attribs.append:
                    subst = "\\1" + gen_text + "\\2\\3"
                elif attribs.update:
                    subst = "\\1" + gen_text + "\n\\3"

            if not attribs.noupdate:
                data_out = re.sub(sub_reg, subst, data_out, 0, re.MULTILINE | re.DOTALL)

    with open(OUTPUT_FILE, "w") as file:
        file.write(data_out)
        file.close()


if __name__ == "__main__":
    main()


