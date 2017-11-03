# random_planner
Telegram bot that gives you a random task from your tasklist

## Features
* Hierarchical lists support
* Time logging
* Postponing task
* Command line interface

## Todo
* Select tasks by tag
* Command keyboard
* List editor

## Usage
### Bot
1. `git clone https://github.com/mingghan/random_planner.git`
2. Create your bot on [Telegram bot page](https://core.telegram.org/bots#6-botfather) and get your token
3. Put your token into `config.py`
4. Start the bot with
    `python random_planner_bot.py`
5. Commands:
    * `/next` - gets new task
    * `/pause` - pauses task
    * `/done` - finishes task and removes it from the list
6. Your tasklist is in `lists/work.txt` file

### Shell
1. `git clone https://github.com/mingghan/random_planner.git`
2. Run `python planner.py lists/work.txt` and follow the instructions. Instead of `lists/work.txt` you can use any other file on your filesystem

# Methodology of fighting the procrastination by random planning (in Russian, translation in progress)
## Рандомное планирование как средство от прокрастинации

### Преамбула

Я люблю составлять TODO-списки. Они у меня огромные, иерархические, с кучей уровней, с приоритетами.

С планированием проблем нет. Проблема возникает тогда, когда нужно что-то уже сделать. Я смотрю на эти огромные списки, на кучу дел, которые нужно переделать, вздыхаю и ухожу читать ленту фейсбука. В конце дня возникает чувство вины и понимание, что можно работать уже не весь день, а всего несколько часов. После чего я, не заглядывая в список, беру то дело, о котором помню и которое больше всего меня беспокоит, и начинаю делать его.

### Решение

Я написал программу, которая говорит мне, что делать. Работает она так: на вход программе дается список дел со всеми приоритетами, а программа случайным образом выбирает из этого списка дело и показывает его мне. После чего я должен поработать над этой задачей в течение минимум 25 минут. Тут я применяю технику pomodoro - т.е. работаю над этой случайной задачей в течение одной помидорки.

Программа умеет работать с приоритетами и более важные задачи будет показывать чаще. Также она умеет работать с последовательными задачами - если одна задача зависит от другой, то будет показана только первая.

Еще я добавил несколько приятных мне дел, и, таким образом, у меня есть больше стимулов запускать программу - потому что есть небольшая вероятность делать что-то, что мне нравится. Психологи утверждают, что действие, дающее желаемый результат с небольшой вероятностью, является более аддиктивным, чем действие, которое дает тот же результат гарантированно. Игроки в рулетку меня поймут.
