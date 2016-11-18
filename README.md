# Clighter8: VIM8 plugin to highlight C-family code

## Intro

Clighter8 is a VIM plugin to support C-family code powered by libclang.
Currently it can highlight code semantically and do rename-refactor.
Clighter8's engine is highly optimized for VIM's new async io mechanism, that
means Clighter8 will run in background totally, and it won't slow down the
performance of VIM.

## Requirements

Clighter8 requires the following things:

* VIM8
* [libclang 3.9][libclang] (Note: If you are using a different version of clang, you have to replace the Python clang bindings in python/clang with the appropriate version.)

## Installation

Use a VIM plugin manager, for example

* Vundle Install:
```vim
CCㄠBundle 'bbchung/clighter8'
```

## Usage

Clighter8 provides following commands and functions:

#### ClStart

Start Clighter8 immediatly. Clighter8 will highlight the code after it starts,
and the refactor-rename function will be enabled.

#### ClStop

Stop Clighter8 and cleanup highlight, refactor-rename function will be
disabled.

#### ClShowCursorInfo

Show some Clighter8 runtime informations.

#### ClEnableLog

Enable clighter8 log, the log file is put under /tmp/clighter8.log.

#### ClDisableLog

Disable clighter8 log.

#### ClRename()

* An experimental function to do rename-refactor.
* Only do renaming in opened buffers.
* There is no one-step undo method.

For convenience, you can add a key mapping in your vimrc:
```vim
nmap <silent> <Leader>r :call Rename()<CR>
```

## Options

:help clighter8-options

## Compilation Database

Clighter8 automatically loads and parses the compilation database
"compile_commands.json" if it exists in current working directory, then passes
the compile options to libclang. For more information about compilation
database, please reference [Compilation Database][cdb].

## FAQ

#### Clighter8 doesn't work?
Check the Requirements and Installation, and check if libclang path is given.

#### Rename() function is an experimental function?
Due to the limitation of c-family language, it's hard to do rename-refactor.
Clighter8 will only search all opened buffers to do renaming and it can't
guarantee the correctness.

#### How to set compile args?
Clighter8 set the compile args for each file by (g:clighter8_compile_args +
"compilation database"). Compile args will affect the correctness of highlight
and rename-refactor.

## LICENSE

This software is licensed under the [GPL v3 license][gpl].

Note: This license does not cover the files that come from the LLVM project.


[libclang]: http://llvm.org/apt/
[gpl]: http://www.gnu.org/copyleft/gpl.html
[ycm]: https://github.com/Valloric/YouCompleteMe
[cdb]: http://clang.llvm.org/docs/JSONCompilationDatabase.html
