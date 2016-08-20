# Clighter8: Vim8 plugin to highlight C-family code

## Intro

Clighter8 is a vim plugin to support C-family code powered by libclang.
Currently it can highlight and rename-refactor code semantically. Clighter8's
engine takes the advantage of vim8's new async architecture, and it is highly
optimized, so it runs very fast, user will not feel any laggy.

## Requirements

clighter8 requires the following:

* Vim8
* libclang, http://llvm.org/apt/

## Installation

use vim plugin manager, for example

* Vundle Install:
```vim
Bundle 'bbchung/clighter8'
```

## Usage

Clighter8 provides these commands and functions.

### StartClighter8

Start Clighter8 immediatly.

### StopClighter8

Stop Clighter8 and cleanup highlight.

### ShowInfo

Show clighter8 runtime informations.

### Rename()

* An experimental function to do rename-refactor.
* The scope is opened vim buffers.
* There is no one-step undo/redo method.
* Strongly recommend that backing up all files before calling this function.
* For convenience, you can add key mapping in your vimrc:
```vim
nmap <silent> <Leader>r :call Rename()<CR>
```

## Options

:help clighter8-options

## Compilation Database

Clighter8 automatically load and parse the compilation database
"compile_commands.json" if it exists in current working directory, then the
compile options will be passed to libclang. For more information about
compilation database, please reference [Compilation Database][cdb].

## FAQ

### Clighter8 doesn't work?
Check the Requirements and Installation.

### Why rename-refactor function is an experimental function?
Due to the character of c-family language, it's hard to do rename-refactor.
Clighter8 only search the current opened buffer to do rename-refactor and it
can't guarantee the correctness.

### How to set compile args?
Clighter8 set the compile args for each file with (g:clighter8_compile_args +
"compilation database"). Compile args will affect the correctness of highlight
and rename-refactor.

## LICENSE

This software is licensed under the [GPL v3 license][gpl].

Note: This license does not cover the files that come from the LLVM project.


[gpl]: http://www.gnu.org/copyleft/gpl.html
[ycm]: https://github.com/Valloric/YouCompleteMe
[cdb]: http://clang.llvm.org/docs/JSONCompilationDatabase.html
