import argparse
from prettytable import PrettyTable
from prettytable import from_html_one

from worker import Worker
from config import login, password, folder_path


def initialize_parser():
    """Initialize parser for CLI."""
    parser = argparse.ArgumentParser(
        usage='acm [command] [parameters]',
    )
    parser.set_defaults(func=lambda args: parser.print_help())
    subparsers = parser.add_subparsers(
        dest='command',
        title='Commands',
        metavar='<command>',
    )

    gen_cmd = subparsers.add_parser('gen', help='Generate new contests')
    gen_cmd.set_defaults(func=generate)

    submit_cmd = subparsers.add_parser('submit', help='Submit task')
    submit_cmd.add_argument('path', type=str, help='File to submit')    
    submit_cmd.set_defaults(func=submit)

    status_cmd = subparsers.add_parser('status', help='Get status of all problems in contest')
    status_cmd.set_defaults(func=status)
    
    submissions_cmd = subparsers.add_parser('submissions', help='Get status of all problems in contest')
    submissions_cmd.set_defaults(func=submissions)

    return parser


def get_worker():
    return Worker(login, password, folder_path)


def generate(args):
    w = get_worker()
    res = w.update_contests()
    print(res)


def submit(args):
    w = get_worker()
    res = w.submit_task(args.path)
    print(res)


def status(args):
    w = get_worker()
    res = w.get_summary()
    x = PrettyTable()
    x.field_names = ["Problem", "Verdict"]
    for i in res:
        x.add_row([i, res[i]])
    print(x)


def submissions(args):
    w = get_worker()
    table = w.get_last_submission()
    x = from_html_one(table)
    print(x[1:10])


def main():
    """Point of entry."""
    parser = initialize_parser()
    args = parser.parse_args()

    args.func(args)


if __name__ == '__main__':
    main()
