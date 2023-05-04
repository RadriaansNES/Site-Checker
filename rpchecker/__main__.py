import sys
from rpchecker.cli import read_user_cli_args
import pathlib
from rpchecker.checker import site_is_online
from rpchecker.cli import display_check_result, read_user_cli_args


## Function to run checker
def main():
    user_args = read_user_cli_args()
    urls = _get_websites_urls(user_args)
    if not urls:
        print("Error: no URLs to check", file=sys.stderr)
        sys.exit(1)
    _synchronous_check(urls)

## Store the list of URLS at CL into list, return it (if any provided)
def _get_websites_urls(user_args):
    urls = user_args.urls
    if user_args.input_file:
        urls += _read_urls_from_file(user_args.input_file)
    return urls

## Turn file into pathlib object (if any provided)
def _read_urls_from_file(file):
    file_path = pathlib.Path(file)
    if file_path.is_file():
        with file_path.open() as urls_file:
            urls = [url.strip() for url in urls_file]
            if urls:
                return urls
            print(f"Error: empty input file, {file}", file=sys.stderr)
    else:
        print("Error: input file not found", file=sys.stderr)
    return []

## Function to cycle through and display connectivity of multiple websites
def _synchronous_check(urls):
    for url in urls:
        error = ""
        try:
            result = site_is_online(url)
        except Exception as e:
            result = False
            error = str(e)
        display_check_result(result, url, error)

## Script trigger
if __name__ == "__main__":
    main()