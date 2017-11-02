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
1.
    git clone https://github.com/mingghan/random_planner.git
2. Create your bot on [Telegram bot page](https://core.telegram.org/bots#6-botfather) and get your token
3. Put your token into config.py
4. Start the bot with
    python random_planner_bot.py
5. Commands:
    /next - gets new task
    /pause - pauses task
    /done - finishes task and removes it from the list
