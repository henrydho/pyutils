"""Command Line Input module"""
from typing import Union, Literal, NamedTuple

from utilities.utils import TextFormatter, Validator


class PromptMenu(NamedTuple):
    """PromptMenu `namedtuple` class

    :param cmd: a `str` command entered from STDIN
    :param message: a `str` prompt message
    """
    cmd: str
    message: str


class PromptInput(NamedTuple):
    """PromptInput `namedtuple` calss

    :param message: a `str` prompt message
    :param datatype: input data types
    :param description: a `str`input description
    :param input_type: a `str` input type, default='info'
    :param valid_values: a list of valid values used with 'input' datatype
    """
    message: str
    datatype: Literal['int', 'ip', 'ipv4', 'ipv6', 'input']
    valid_values: list=[]
    description: str=''
    input_type: Literal['info', 'warning']='info'


class InteractiveCli:
    """Interactive CLI to get the user's input via STDIN

    :param title: a `str` menu title
    :param menu: a `list` of menu items with data type of
        `namedtuple` PromptMenu class
    :param prompt_message: a `str` menu's prompt message
    """

    def __init__(self, title: str, menu: list, prompt_message: str):
        self.title = title
        self.menu = menu
        self.prompt_message = prompt_message

    def prompt_menu(self):
        """Display a list of menu and prompt user to enter a menu command

        - Validate the entered command and display error if it is invalid
        - Return the valid command entered by the user
        """
        # TODO: Add navigation commands below:
        # - r: return to previous menu
        # - q: quit the application

        # Print out the menu until a valid command is entered
        while True:
            # Print menu title
            print(f"\n{'':2}{TextFormatter.format(self.title, 'green')}\n")

            # Print out the menu's commands
            for item in self.menu:
                if item.cmd == 'q':
                    print(f"\n{'':2}{TextFormatter.format('Exit', 'green')}\n")
                print(f"{'':6}{item.cmd:4}{item.message}")

            command = input(f"\n{TextFormatter.format(self.prompt_message + ': ', 'bold')}")

            try:
                return self.validate_command(command)
            except ValueError as err:
                print(TextFormatter.format(str(err), 'red'))

    def prompt_inputs(
            self,
            prompts: list,
            exit_cmd: str='r'
            ) -> Union[list, None]:
        """Display and prompt user to provide inputs from the command line

        :param prompts: a `list` of `namedtuple` PromptInput class containing
            prompt message and data type

            :Example: [
                PromptMenu('message'='Prompt Message', 'datatype'='int'},
                PromptMenu('message'='Prompt message', 'datatype'='ipv6'},
            ]

        :param description: a `str` description of input
        :param exit_cmd: exit command used to return to previous menu
        :return:
            `list` of inputs entered from the cli
            `str` value of the exit prompt command
        rtype: `list`, `None`
        """

        inputs = []
        for prompt in prompts:
            _input = ''
            while _input != exit_cmd:
                # Print out the input's description
                if prompt.description is not None:
                    match prompt.input_type:
                        case 'info':
                            print(f"\n{TextFormatter.format(prompt.description, 'green')}")
                        case 'warning':
                            warn_msg = f"\n{prompt.input_type.upper()} - {prompt.description}"
                            print(f"{TextFormatter.format(warn_msg, 'red')}\n")

                prompt_message = f"{prompt.message} ({exit_cmd} to return previous menu)"
                _input = input(
                        f"{TextFormatter.format(prompt_message + ': ', 'bold')}"
                        ).strip()
                if _input == exit_cmd:
                    break

                try:
                    if prompt.datatype == 'input':
                        inputs.append(Validator.validate(
                            data=_input,
                            datatype=prompt.datatype,
                            valid_values=prompt.valid_values
                            ))
                    else:
                        inputs.append(Validator.validate(_input, prompt.datatype))
                    break
                except ValueError as err:
                    print(TextFormatter.format(str(err), 'red'))

            if _input == exit_cmd:
                return None
        return inputs

    def validate_command(self, command: str) -> str:
        """Validate the command entered from the prompt menu

        :param command: a `str` command value entered from the user
        :raise ValueError: if command entered is not valid
        :return: `command` entered from the command line
        :rtype: `str`
        """
        valid_commands = [menu_item.cmd for menu_item in self.menu]
        if command.strip() in valid_commands:
            return command
        raise ValueError(
                f"{'':2}The command '{command}' entered is not valid!\n"
                f"{'':2}Valid commands are {valid_commands}."
                )
