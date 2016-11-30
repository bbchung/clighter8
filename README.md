# Clighter8: Vim plugin to use libclang to do syntax highlight, code format, refactor

## Intro

Clighter8 is a Vim plugin using libclang to help c-family programming.
Currently it can highlight code semantically and do rename-refactor.
Clighter8 is designed for the new async io mechanism of Vim, it's cool and
.

## Requirements

Clighter8 requires the following things:

* Vim with +job and +channel features
* [libclang][libclang], (3.9 is recommended)

## Installation

Use a plugin manager, for example

* Vundle Install:
```vim
Bundle 'bbchung/clighter8'
```

## Usage

Clighter8 provides following commands and functions:

#### ClStart

Start Clighter8 immediatly. Clighter8 will highlight the code after it starts,
and the refactor-rename function will be enabled.

#### ClStop

Stop Clighter8 and cleanup highlight, refactor-rename function will be
disabled.

#### ClRestart

Restart clighter8.

#### ClShowCursorInfo

Show cursor informations.

#### ClShowCompileInfo

Show compiler args of current buffer.

#### ClEnableLog

Enable clighter8 log, the log file is put under /tmp/clighter8.log.

#### ClDisableLog

Disable clighter8 log.

#### ClLoadCdb

Open source files described in compilation database and all reference header
files under current working folder of Vim. It will take a lot of time if the
compilation database is big.

#### ClRenameCursor

* It's the experimental function to do rename-refactor.
* The search scope is the list of Vim buffers.
* There is no one-step undo function.

For convenience, you can add the key mapping in your vimrc:
```vim
nmap <silent> <Leader>r :ClRenameCursor<CR>
```

## Options

:help clighter8-options

## Compilation Database

Clighter8 supports compilation database if the compilation database exists in
current directory. It's strongly recommended to provide a compilation database
in your project to get the better result of highlight and refactor-rename. For
more information about compilation database, please reference [Compilation
Database][cdb].

## FAQ

#### Clighter8 doesn't work?
Check the Requirements and Installation, and check if a valid libclang path is
given.

#### ClRenameCursor is experimental?
Due to the many restrictions, it's hard to do rename-refactor. Clighter8 only
searches opened buffers in Vim to do renaming and it can't guarantee the
correctness.

#### How to set compile args?
Clighter8 sets the compile args for each file with
(g:clighter8_global_compile_args + "compilation database"). Compile args will
affect the correctness of highlight and rename-refactor.

## LICENSE

This software is licensed under the [GPL v3 license][gpl].

Note: This license does not cover the files that come from the LLVM project.


[libclang]: http://llvm.org/apt/
[gpl]: http://www.gnu.org/copyleft/gpl.html
[ycm]: https://github.com/Valloric/YouCompleteMe
[cdb]: http://clang.llvm.org/docs/JSONCompilationDatabase.html
