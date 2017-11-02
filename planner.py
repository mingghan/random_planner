#!/usr/bin/python
#-*- coding: utf-8 -*-

from tree import Tree
from stack import Stack
import re
import random
import sys
import datetime as dt
from node import Node

(_ROOT, _DEPTH, _BREADTH) = range(3)
ARCHIVE_FILE = "_archive.txt"
ROOT = 'root'
INBOX = 'INBOX'
EVALUATION_ADVISOR_RATE = 0.3
MORNING_PLANNING_HOUR = 8
EVENING_PLANNING_HOUR = 22

WEEK_PLANNING_DAY = 6

DEFAULT_EVALUATION_UNIT = 'h'
DECOMPOSITION_THRESHOLD = '1h'
DECOMPOSITION_ADVISOR_RATE = 0.3

class bgcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def deduplicate(filename):
    root = "."
    parents = Stack()
    parents.push(root)
    prev_indent = 0
    parent = root
    dic = {}
    i = 100000
    
    f = open(filename, "r+")
    lines = f.readlines()
    f.seek(0)
    
    for line in lines:
        i += 1
        indent = len(re.match('^\t*', line).group(0))
        if indent > prev_indent:
            parent = current
            parents.push(parent)
            prev_indent = indent
        elif indent < prev_indent:
            for i in xrange(0,prev_indent-indent+1):
                parent = parents.pop()
            parents.push(parent)

        node = line.strip()    
        
        prev_indent = indent
        current = node
        #tree.add_node(current, parent)
        if current in dic:
            line = line[:-1]
            if current + parent in dic:
                new_line = "{0} ({1} #{2})\n".format(line, parent, i)
            else:
                new_line = "{0} ({1})\n".format(line, parent)
                dic[current + parent] = 1
        else:
            new_line = line
            dic[current] = 1
    
        f.write(new_line)
        
    f.truncate()
    f.close()    

def read_file_to_tree(in_file):
    tree = Tree()

    tree.add_node(ROOT)  # root node
    parents = Stack()
    parents.push(ROOT)
    prev_indent = 0
    parent = ROOT
    
    for line in in_file:
        indent = len(re.match('^\t*', line).group(0))
        if indent > prev_indent:
            parent = current
            parents.push(parent)
            prev_indent = indent
        elif indent < prev_indent:
            for i in xrange(0,prev_indent-indent+1):
                parent = parents.pop()
            parents.push(parent)

        node = line.strip()    
        prev_indent = indent
        current = node
        tree.add_node(current, parent)
    
    return tree

def prioritize(in_list):
    new_list = []
    low_priority_list = []
    for item in in_list:
        if item.startswith('_'):
                low_priority_list.append(item)
                continue
        priority = len(re.match('^!*', item).group(0))
        for i in range(-1,priority):
            new_list.append(item)
    return new_list, low_priority_list
    
def pick_random_task(list):
    leaves_list, low_priority = prioritize(list)

    size = len(leaves_list)
    if len(low_priority)>0:
        size += 1
    randnum = random.randint(0,size-1)
    if randnum == size-1 and len(low_priority)>0:
        randnum = random.randint(0, len(low_priority)-1)
        next_task = low_priority[randnum]
        print 'low priority item:\n\t%s' % next_task
        return next_task
    next_task = leaves_list[randnum]
    print next_task
    print '[#%d out of %d]' % (randnum+1, size)
    return next_task
    
def get_next_task(tree):
    leaves = []
    leaves_list = list(tree.get_branch(ROOT, leaves))    
    next_task = pick_random_task(leaves_list)
    return next_task

def remove_item_from_file(item, filename):
    f = open(filename, "r+")
    lines = f.readlines()
    f.seek(0)
    for line in lines:
        if item not in line:
            f.write(line)
    f.truncate()
    f.close()
    
def append_item_to_file(item, filename):
    with open(filename, "a") as myfile:
        myfile.write(item)

def pretty_time_delta(seconds):
    sign_string = '-' if seconds < 0 else ''
    seconds = abs(int(seconds))
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    return '%02d:%02d:%02d' % (hours, minutes, seconds)
    
def get_task_time(start_time):
    now = dt.datetime.now()
    task_time = now - start_time
    return task_time
    
def print_time_delta(start_time):
    task_time = get_task_time(start_time)
    print pretty_time_delta(task_time.seconds)

def prepare_log_str(item, start_time, status=""):
    task_time = get_task_time(start_time)
    if status:
        status = "[" + status + "]"
    log_str = "%s -- %s [%s]%s\n" % (dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), item, pretty_time_delta(task_time.seconds), status)
    return log_str

def complete_task(item, filename, start_time, tree):
    if item == ROOT:
        return
    log_str = prepare_log_str(item, start_time)
    print log_str
    append_item_to_file(log_str, ARCHIVE_FILE)
    parent = tree[item].parent
    children_count = len(tree[parent].children)
    tree.remove_node(item)
    tree.dump_to_file(filename)
    #TODO: uncomment this
    #if children_count == 1 and parent != ROOT:
    #    prompt_str = bgcolors.OKBLUE + 'Do you want to close also parent task "' + bgcolors.WARNING +\
    #                parent + bgcolors.OKBLUE + '"? ' + bgcolors.ENDC
    #    input = raw_input(prompt_str)
    #    if input in ['y', 'yes']:
    #        complete_task(parent, filename, dt.datetime.now(), tree)
    #remove_item_from_file(item, filename)
    print bgcolors.OKGREEN + "Excellent work!" + bgcolors.ENDC   
    return log_str

def postpone_task(item, filename, start_time):
    log_str = prepare_log_str(item, start_time, status="WIP")
    print log_str
    append_item_to_file(log_str, ARCHIVE_FILE)
    return log_str
    
def get_project_list(tree):
    projects = []
    for item in tree[ROOT].children:
        projects.append(item)
    return projects

def print_list(list):
    i = 0
    for item in list:
        i += 1
        print "%d. %s" % (i, item)
        
def get_next_task_from_project(tree, item):
    list = []
    list = tree.get_branch(item, list)

    next_task = pick_random_task(list)
    return next_task
        
def pick_project(tree):
    projects = get_project_list(tree)
    print_list(projects)
    prompt_str = bgcolors.OKBLUE + "pick project number: " + bgcolors.ENDC
    input = ''
    while not input.isdigit():
        input = raw_input(prompt_str)
        if not input.isdigit():
            print bgcolors.WARNING + "Please enter a number" + bgcolors.ENDC
        elif int(input) > len(projects):
            print bgcolors.WARNING + "Number entered is bigger than number of projects" + bgcolors.ENDC
        else:
            return get_next_task_from_project(tree, projects[int(input)-1])

def pick_tagged_task(tree):
    prompt_str = bgcolors.OKBLUE + "enter a tag: " + bgcolors.ENDC
    input = ''
    list = []
    while len(list)==0:
        input = raw_input(prompt_str)
        list = tree.get_tagged_leaves(ROOT, list, input)
        if len(list) == 0:
            print bgcolors.WARNING + "No items with such tags found" + bgcolors.ENDC
    next_task = pick_random_task(list)
    return next_task

def add_task(child, parent, tree, filename):
    if tree[parent] is None:
        tree.add_node(parent, ROOT)
    tree.add_node(child, parent)
    tree.dump_to_file(filename)

def add_task_to_inbox(tree, filename):
    prompt_str = bgcolors.OKBLUE + "enter task: " + bgcolors.ENDC
    input = raw_input(prompt_str)
    add_task(input, INBOX, tree, filename)
    print bgcolors.OKGREEN + "Task added to your Inbox" + bgcolors.ENDC
    
def evaluate_task(task, tree, filename):
    if "[" in task or task == ROOT:
        return
    if random.random() > EVALUATION_ADVISOR_RATE:
        return
    prompt_str = bgcolors.OKBLUE + 'How much time will' + bgcolors.OKGREEN +\
                 ' "{0}" '.format(task) + bgcolors.OKBLUE + 'task take: '  + bgcolors.ENDC
    input = raw_input(prompt_str)
    if input == 'done':
        complete_task(task, filename, dt.datetime.now())
        return
    if input == 'skip' or input == '':
        print bgcolors.OKGREEN + 'skipped'  + bgcolors.ENDC
        return
    new_task = '{0} [{1}]'.format(task, input)
    new_tree = tree
    new_tree.replace_node(task, new_task) #[task] = new_task #Node(new_task)
    
    print bgcolors.WARNING + new_task + bgcolors.ENDC
    tree.dump_to_file(filename)
    print bgcolors.OKGREEN + "Task evaluated" + bgcolors.ENDC

def check_inbox(tree):
    current_hour = dt.datetime.now().hour
    if tree[INBOX] is None:
        return False
    leaves = tree.get_branch(INBOX, [])
    if len(leaves) > 0 and leaves[0] != INBOX \
        and (current_hour < MORNING_PLANNING_HOUR or current_hour >= EVENING_PLANNING_HOUR):
            print bgcolors.WARNING + 'You have tasks in your INBOX, please empty it' + bgcolors.ENDC
            return True
    return False
    
def advise_backlog_grooming():
    current_weekday = dt.datetime.now().weekday()
    current_hour = dt.datetime.now().hour
    if current_weekday == WEEK_PLANNING_DAY \
        and (current_hour < MORNING_PLANNING_HOUR or current_hour >= EVENING_PLANNING_HOUR):
            print bgcolors.WARNING + "It's week planning time. Please groom your backlog" + bgcolors.ENDC
            return True
    return False
    
def parse_duration(duration):
    seconds = 0
    minutes = 0
    hours = 0
    days = 0
    weeks = 0
    months = 0
    years = 0
    parsed = re.match("(\d+) *(\w*)", duration)
    if parsed is None:
        print "Couldn't parse duration:", duration
        return
    
    number = int(parsed.group(1))
    units = parsed.group(2)
    if units is "":
        units = DEFAULT_EVALUATION_UNIT
        
    if units == 's' or 'sec' in units:
        seconds = number
    elif units == 'm' or 'min' in units:
        minutes = number
    elif units == 'h' or 'hour' in units:
        hours = number
    elif units == 'd' or 'day' in units:
        days = number
    elif units == 'w' or 'week' in units:
        weeks = number
    else:
        print "Couldn't parse units:", units
        return
        
    delta = dt.timedelta(seconds = seconds, minutes = minutes, hours = hours, days = days, weeks = weeks)
    return delta    
    
def advise_task_decomposition(task, tree, filename):
    if not "[" in task:
        return
    if random.random() > DECOMPOSITION_ADVISOR_RATE:
        return
    duration_re = re.match(".*?\[(.+?)\]", task).group(1)
    duration = parse_duration(duration_re)
    if duration is None:
        return
    threshold = parse_duration(DECOMPOSITION_THRESHOLD)
    if duration < threshold:
        return
    prompt_str = bgcolors.WARNING + "Decompose this task: " + \
        bgcolors.OKGREEN + task + bgcolors.WARNING + "? " + bgcolors.ENDC
    input = raw_input(prompt_str)
    while input in ['y', 'yes', 'да', 'д']:
        prompt_str = bgcolors.OKBLUE + "Enter subtask: " + bgcolors.ENDC
        input = raw_input(prompt_str)
        add_task(input, task, tree, filename)
        print bgcolors.OKGREEN + "Subtask added" + bgcolors.ENDC
        prompt_str = bgcolors.OKBLUE + "Add another subtask? " + bgcolors.ENDC
        input = raw_input(prompt_str)
    print ''
    
def prompt_loop(filename):
    input = ''
    task = "#*(#*#(*#UJ" #random string
    start_time = dt.datetime.now()
    while (input != "exit"):
        prompt_str = bgcolors.OKBLUE + "enter command: " + bgcolors.ENDC
        input = raw_input(prompt_str)
        
        deduplicate(filename)
        tree = read_file_to_tree(open(filename))

        if input == 'done' or input == '+':
            complete_task(task, filename, start_time, tree)
        elif input in ['start', 'reset']:
            start_time = dt.datetime.now()
            print bgcolors.WARNING + "Timer has been resetted" + bgcolors.ENDC
        elif input == 'next' or input == 'n':
            if check_inbox(tree):
                continue
            if advise_backlog_grooming():
                continue
            task = get_next_task(tree)
            evaluate_task(task, tree, filename)
            advise_task_decomposition(task, tree, filename)
            start_time = dt.datetime.now()
        elif input == 'postpone' or input == 'pause':
            postpone_task(task, filename, start_time)
        elif input == 'time' or input == 'current_time':
            print_time_delta(start_time)
        elif input == 'projects' or input == 'p':
            task = pick_project(tree)
            start_time = dt.datetime.now()
        elif input == 'tag':
            task = pick_tagged_task(tree)
            start_time = dt.datetime.now()
        elif input == 'add':
            add_task_to_inbox(tree, filename)
        elif input == 'context' or input == 'parent':
            print tree[task].parent
        elif input == 'tree' or input == 'display':
            tree.display(ROOT)
    
    print bgcolors.OKGREEN + "See you again!" + bgcolors.ENDC

def main():
    filename = sys.argv[1]
    prompt_loop(filename)
        
    #for item in leaves_list:
    #    print item

if __name__ == "__main__":
    main()
