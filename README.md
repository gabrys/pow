# Pow

Pow is a CLI tool to run useful commands easily configurable via Pow files.

# Pow for you

* Pow can replace a collection of useful command aliases and BASH scripts that almost everyone ends up keeping in their ~/bin/
* Pow can help you make sure you never run `docker run` without `--rm`
* Pow can help you with tasks you do from time to time but not often enough to remember the exact command line to use (and it's easier to share/version your pow files than your .bash_history for those relying on Ctrl-R)
* Pow can be used to create wrappers for your workflow (you can wrap commands involving `aws`, `docker`, `git` or anything else)
* Pow can be the way you share your scripts with others

## Example

Put the following in your `~/.pow_file.py`:

```python

def pow_avg(args):
    """Calculate average of given integers"""
    total = sum(map(int, args))
    print(total / len(args))
```

Then you execute like this:

```
$ pow avg 1 2 3 4
2.5
```

You can list all available commands:

```
$ pow

Usage: pow [options] <command> [command parameters]

  pow --help        Print pow's usage and available commands
  pow -h            Alias for --help
  pow avg           Calculate average of given integers
  pow inspect-pow   Inspect loaded pow files

```

# Pow for your project

* Pow aims to replace `npm run command`, `composer run-script command`, `./manage.py command` and the like -- in a framework independent fashion -- also sharing the entry point for parts done in different languages
* Pow can be used to provide one interface for building, running, maintaining, and debugging your application
* Pow offers a unified way to share scripts between developers

## Example

```
$ pow

Usage: pow [options] <command> [command parameters]

  pow --help                 Print pow's usage and available commands
  pow -h                     Alias for --help
  pow extract-translations   Extract strings to translate from application files
  pow generate-fake-data     Populate the database with randomly generated data
  pow githook-precommit      Run checks before git commit
  pow inspect-pow            Inspect loaded pow files
  pow install-githooks       Install git hooks
  pow lint                   Auto-format all Python and JavaScript files in this project
  pow run-backend            Build and start backend in docker
  pow run-frontend           Build and start frontend using node

```

In this example we see Pow used as a common way of discovering and running various commands for the project: extracting translations, linting the code, installing git hooks to help the team mates follow a process. The git hooks themselves are also executed through pow. The code for the commands might be split into multiple files like this:

```
pow_files/
├── pow_backend.py
├── pow_frontend.py
├── pow_githooks.py
└── pow_translations.py
```

Pow will load any file in `pow_files/` named `pow_*.py` so you can put together as many (or as few) commands in one Python file as you're comfortable with.

# Dependencies and installation

Pow is one Python 3 file with no further dependencies. In order to make it independent of system's installation of Python I created `pow-runner` which is an executable that embeds Python 3.8.7 and is used to run `pow.py`. It's precompiled for Linux, macOS and Windows (on Windows it's a bunch of files actually).

## Easy installation via yarn on Windows and Linux (x86_64 only)

You can install it via `sudo yarn global add https://github.com/gabrys/pow.git` (no sudo on Windows). When running `pow` installed via `npm`, it launches via a JavaScript script, so there is some additional overhead when starting.

## Easy installation via yarn on Macs (Intel and M1)

You can install it via `sudo yarn global add https://github.com/gabrys/pow-macos.git` (note, another GitHub repo!). When running `pow` installed via `npm`, it launches via a BASH script, and the overhead when starting is minimal.

## Any other platform with Python 3.8+

Put `pow.py` into your PATH, rename to `pow` (if that's what you desire) and make executable. 

# Comparison to other tools

Pow was inspired by the following tools and patterns:

* Using a Makefile to store commands useful for building, running, maintaining, and debugging your application
  * Pow file is easier to write than a Makefile
  * Pow commands are available anywhere in the project, not only in the directory with the Makefile
* Project scripts running through `yarn run`, `composer run-script`  (PHP), `./manage.py` (Django), etc
  * Pow can be used if you don't have `yarn` or `composer`. Example: use Pow to *install* yarn or run yarn via Docker
* Storing a ton of aliases in one's `.bashrc` or `.bash_aliases`
  * Pow commands *can* be as simple as aliases, but they also *can* also have some logic
  * You can have multiple Pow files and they will be automatically loaded if you put them to `pow_files` directory
  * You can use whatever shell you want and your pow commands will work the same
* A collection of useful short shell/Perl/Python/Ruby scripts in `~/bin`
  * Multiple (as many or as few as desired) Pow commands can be put in the same file
  * Common parts of your commands may be extracted to Pow plugins and reused
