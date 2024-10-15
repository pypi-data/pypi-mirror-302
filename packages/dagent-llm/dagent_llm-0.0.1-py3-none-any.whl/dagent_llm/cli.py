#!/usr/bin/env python3
# coding=utf-8
# @Time    : 2024-10-15
# @Author  : zhaosheng@nuaa.edu.cn
# @Describe: Command Line Interface for LLM package

import argparse
import logging
from dagent_llm import LLM

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Command Line Interface for LLM operations.")
    
    # Define subcommands
    subparsers = parser.add_subparsers(dest='command', help="Sub-commands for various operations")
    
    # 'chat' subcommand
    chat_parser = subparsers.add_parser('chat', help='Send a message to the LLM and get a response.')
    chat_parser.add_argument('--message', required=True, help='The message to send to the LLM.')
    chat_parser.add_argument('--llm_server', default='deepseek', help="Specify the LLM server to use.")
    chat_parser.add_argument('--role', default='human', choices=['human', 'ai', 'system'], help="Specify the role of the message sender.")
    
    # 'choose' subcommand
    choose_parser = subparsers.add_parser('choose', help='Present options to the LLM and get a choice.')
    choose_parser.add_argument('--options', nargs='+', required=True, help='List of options to choose from.')
    choose_parser.add_argument('--prompt', required=True, help='The prompt presented to the LLM for making a choice.')
    choose_parser.add_argument('--need-reason', action='store_true', help='Ask the LLM to provide reasons for the choice.')
    choose_parser.add_argument('--multiple', action='store_true', help='Allow the LLM to select multiple options.')

    # 'choose_with_args' subcommand
    choose_args_parser = subparsers.add_parser('choose_with_args', help='Choose an option and provide arguments.')
    choose_args_parser.add_argument('--options', nargs='+', required=True, help='List of options to choose from.')
    choose_args_parser.add_argument('--prompt', required=True, help='The prompt for choosing.')
    choose_args_parser.add_argument('--option-type', required=True, help='The type of options being chosen.')
    choose_args_parser.add_argument('--need-reason', action='store_true', help='Provide reasons for the choice.')
    choose_args_parser.add_argument('--multiple', action='store_true', help='Allow multiple selections.')

    # Parse arguments
    args = parser.parse_args()

    # Initialize the LLM object
    llm = LLM(llm_server=args.llm_server)

    if args.command == 'chat':
        # Chat command
        response = llm.chat(args.message, role=args.role)
        print(f"LLM response: {response.content}")

    elif args.command == 'choose':
        # Choose command
        result = llm.choose(
            options=args.options,
            prompt=args.prompt,
            need_reason=args.need_reason,
            multiple=args.multiple
        )
        print(f"LLM choice: {result}")

    elif args.command == 'choose_with_args':
        # Choose with arguments command
        choice, args = llm.choose_with_args(
            options=args.options,
            prompt=args.prompt,
            option_type=args.option_type,
            need_reason=args.need_reason,
            multiple=args.multiple
        )
        print(f"LLM choice: {choice}")
        print(f"LLM arguments: {args}")

    else:
        print("Invalid command. Use --help for more details.")

if __name__ == '__main__':
    main()
