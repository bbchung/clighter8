# Clamp: NeoVim plugin to highlight C-family code

## Intro

Clamp is a neovim plugin to support C-family code powered by libclang.
Currently it can highlight and rename-refactor code semantically. Clamp takes
the advantage of new plugin architecture of neovim and it runs very smooth.

## Requirements

Clamp requires the following:

* NeoVim
* libclang, http://llvm.org/apt/
* python-client of msg-pack, https://github.com/neovim/python-client

## Installation

use vim plugin manager, for example

* Vundle Install:
```vim
Bundle 'bbchung/Clamp'
```

## Options

### g:clamp_autostart

Start Clamp automatically.

Default: `1`
```vim
let g:clamp_autostart = 0
```

### g:clamp_libclang_path

Config the libclang path if libclang is not in default path or Clamp can't
find it.

Default: `''`
```vim
let g:clamp_libclang_file = '/usr/lib/libclang.so'
```

### g:clamp_highlight_blacklist

Define the group of syntax NOT to be highlighted.

Default: `['clampInclusionDirective']`

The recommend setting to not be dazzled:
```vim
let g:clamp_highlight_blacklist = ['clampNamespaceRef', 'clampFunctionDecl', 'clampFieldDecl', 'clampDeclRefExprCall', 'clampMemberRefExprCall', 'clampMemberRefExprVar', 'clampNamespace', 'clampNamespaceRef', 'cligherInclusionDirective', 'clampVarDecl']
```

### g:clamp_heuristic_compile_args

Clamp search the compilation database to compile, but the compilation
database the CMake generated doesn't include the header files. Clamp can
heuristic search the compilation database to guess the most possible compile
args if set this option.

Default: `1`
```vim
let g:clamp_heuristic_compile_args = 1
```

### g:clamp_compile_args

The global compile args of Clamp.

Default: `[]`
```vim
let g:clamp_compile_args = []
```

### g:clamp_highlight_mode

Set it to 1 only if you DON'T use autocomplete plugin like
[YouCompleteMe][ycm].

Default: `0`
```vim
let g:clamp_highlight_mode = 1
```

## Commands and Functions

Clamp provides these commands and functions.

### ClampStart

### ClampShutdown

### ClampRename()

* An experimental function to do rename-refactor.
* The scope is opened vim buffers.
* There is no one-step undo/redo method.
* Strongly recommend that backing up all files before calling this function.
* For convenience, you can add key mapping in your vimrc:
```vim
nmap <silent> <Leader>r :call ClampRename()<CR>
```

## Compilation Database

Clamp automatically load and parse the compilation database
"compile_commands.json" if it exists in current working directory, then the
compile options will be passed to libclang. For more information about
compilation database, please reference [Compilation Database][cdb].

## Highlight Group

Clamp defines these highlight groups corresponded to libclang.

```vim
hi default link clampPrepro PreProc
hi default link clampDecl Identifier
hi default link clampRef Type
hi default link clampInclusionDirective cIncluded
hi default link clampMacroInstantiation Constant
hi default link clampVarDecl Identifier
hi default link clampStructDecl Identifier
hi default link clampUnionDecl Identifier
hi default link clampClassDecl Identifier
hi default link clampEnumDecl Identifier
hi default link clampParmDecl Identifier
hi default link clampFunctionDecl Identifier
hi default link clampFieldDecl Identifier
hi default link clampEnumConstantDecl Constant
hi default link clampDeclRefExprEnum Constant
hi default link clampDeclRefExprCall Type
hi default link clampMemberRefExprCall Type
hi default link clampMemberRefExprVar Type
hi default link clampTypeRef Type
hi default link clampNamespace Identifier
hi default link clampNamespaceRef Type
hi default link clampTemplateTypeParameter Identifier
hi default link clampTemplateNoneTypeParameter Identifier
hi default link clampTemplateRef Type
hi default link clampOccurrences IncSearch
```

You can customize these colors in your colorscheme, for example:
```vim
hi clampTypeRef term=NONE cterm=NONE ctermbg=232 ctermfg=255 gui=NONE
```
## FAQ

### The Clamp plugin doesn't work?
Check the Requirements and Installation.

### Why rename-refactor function is an experimental function?
Due to the character of c-family language, it's hard to do rename-refactor.
Clamp only search the current opened buffer to do rename-refactor and it can't
guarantee the correctness.

### Crash?
Clamp may crashes in some cases. Call ClampStart again if it happens.

### Highlighting always are messed up as typing, can fix?
No, Clamp use matchaddpos() api currently. Once NeoVim provides more powerful
api, I will use it.

### How to set compile args?
Clamp set the compile args for each file with (g:clamp_compile_args +
"compilation database"). Compile args will affect the correctness of highlight
and rename-refactor.

## LICENSE

This software is licensed under the [GPL v3 license][gpl].

Note: This license does not cover the files that come from the LLVM project.


[gpl]: http://www.gnu.org/copyleft/gpl.html
[ycm]: https://github.com/Valloric/YouCompleteMe
[cdb]: http://clang.llvm.org/docs/JSONCompilationDatabase.html
