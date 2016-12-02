# Clighter8: Vim plugin for c/c++ developers and Vim lovers

# Intro

Clighter8 is a server-client architecture Vim plugin, implemented with Vim
channel api. Clighter8 integrates with [clang][clang], [GNU Global][GNU Global] and provides following features currently:

* On-the-fly, highly customized syntax highlight
* Rename-refactor
* Auto update gtags in background
* Intelligent compilation database supporting
* Integrate with clang-format.py
* A color scheme for Clighter8

# Requirements
Clighter8 requires the following things:

* Vim with +job and +channel features
* [libclang][libclang], (3.9 is recommended)
* clang-format-3.9
* [GNU Global][GNU Global]

# Installation

Use a plugin manager, for example

* Vundle Install:
```vim
Bundle 'bbchung/clighter8'
```

# Usage

Clighter8 provides following commands.

## ClStart

Start Clighter8, highlight the code.

## ClStop

Stop Clighter8.

## ClRestart

Restart Clighter8.

## ClShowCursorInfo

Show cursor informations from libclang. It's useful when debugging.

## ClShowCompileInfo

Show compiler args of current buffer.

## ClEnableLog

Enable log, the path of log file is '/tmp/clighter8.log'.

## ClDisableLog

Disable log.

## ClLoadCdb (Experimental)

It will start clighter8 and open source files described in compilation
database and all reference header files under current working folder of Vim.
Notice that it will take much time if the compilation database is big.

## ClRenameCursor (Experimental)

Refactor-rename the current cursor of the buffer. Notice that the search scope
is Vim opened buffers and it's will take much time if there are many opened
buffers. For convenience, you can add the key mapping in your vimrc:

```vim
nmap <silent> <Leader>r :ClRenameCursor<CR>
```

## Compilation Database

Clighter8 supports compilation database, and it loads the compilation database
under the current working directory automatically. Compilation database can
give Clighter8 the compile args for each source file precisely, so it's
strongly recommended to provide a compilation database for Clighter8 to get
the better result of highlight and refactor-rename. For more information about
compilation database, please reference [Compilation Database][cdb].

## FAQ

## Highlight feature doesn't work?
Check the [Requirements](#requirements) and [Installation](#installation)
, and check if a valid libclang path is
given. Also, you can check /tmp/clighter8.log.

## Gtags feature doesn't work?
Check if both 'gtags' and 'global' are installed and the execute path is under
system PATH.

## ClRenameCursor is experimental?
Due to the many restrictions, it's hard to do rename-refactor of c++ code.
Clighter8 only searches opened buffers in Vim to do renaming and it can't
guarantee the correctness.

## How to set compile args?
Clighter8 sets the compile args for each file with
(g:clighter8_global_compile_args + "compilation database"). Compile args will
affect the correctness of highlight and rename-refactor.

# LICENSE

This software is licensed under the [GPL v3 license][gpl].

Note: This license does not cover the files that come from the LLVM and GNU
Global or other third party libraries.


[libclang]: http://llvm.org/apt/
[gpl]: http://www.gnu.org/copyleft/gpl.html
[ycm]: https://github.com/Valloric/YouCompleteMe
[cdb]: http://clang.llvm.org/docs/JSONCompilationDatabase.html
[clang]: http://clang.llvm.org/
[GNU Global]: https://www.gnu.org/software/global/download.html
