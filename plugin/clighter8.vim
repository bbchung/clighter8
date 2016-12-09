if exists('g:loaded_clighter8')
    finish
endif

let s:script_folder_path = escape( expand( '<sfile>:p:h' ), '\'   )
execute('source '. s:script_folder_path . '/../syntax/clighter8.vim')
execute('source '. s:script_folder_path . '/../third_party/gtags.vim')

fun! s:on_gtags_finish()
    if exists('s:gtags_need_update') && s:gtags_need_update == 1
        call s:check_update_gtags()
    endif
endf

fun! s:update_gtags()
    let s:gtags_need_update = 0
    let l:cmd = 'global -u --single-update="' . expand('%') . '"'
    let s:gtags_job = job_start(l:cmd, {'stoponexit': '', 'in_io': 'null', 'out_io': 'null', 'err_io': 'null', 'exit_cb' : {job, status->s:on_gtags_finish()}})
endf

fun! s:check_update_gtags()
    if &diff
        return
    endif

    if exists('s:gtags_job') && job_status(s:gtags_job) ==# 'run'
        let s:gtags_need_update = 1
    else
        let s:gtags_need_update = 0

        if filereadable('GPATH') && filereadable('GRTAGS') && filereadable('GTAGS')
            if executable('global')
                call s:update_gtags()
            endif
        else
            if executable('gtags')
                let s:gtags_job = job_start('gtags', {'stoponexit': '', 'in_io': 'null', 'out_io': 'null', 'err_io': 'null', 'exit_cb' : {job, status->s:on_gtags_finish()}})
            endif
        endif
    endif
endf

fun! s:engine_init(channel, libclang_path, compile_args, cwd, hlt_whitelist, hlt_blacklist)
    let l:expr = {'cmd' : 'init', 'params' : {'libclang' : a:libclang_path, 'cwd' : a:cwd, 'global_compile_args' : a:compile_args, 'whitelist' : a:hlt_whitelist, 'blacklist' : a:hlt_blacklist}}
    return ch_evalexpr(a:channel, l:expr)
endf

fun! s:engine_get_hlt_async(channel, bufname, begin, end, row, col, word, callback)
    let l:expr = {'cmd' : 'get_hlt', 'params' : {'bufname' : a:bufname, 'begin_line' : a:begin, 'end_line' : a:end, 'row' : a:row, 'col': a:col, 'word' : a:word}}
    call ch_sendexpr(a:channel, l:expr, {'callback': a:callback})
endf

func s:engine_cursor_info(channel, bufname, row, col)
    let l:expr = {'cmd' : 'cursor_info', 'params' : {'bufname' : a:bufname, 'row' : a:row, 'col': a:col}}
    return ch_evalexpr(a:channel, l:expr)
endf

func s:engine_compile_info(channel, bufname)
    let l:expr = {'cmd' : 'compile_info', 'params' : {'bufname' : a:bufname}}
    return ch_evalexpr(a:channel, l:expr)
endf

func s:engine_req_parse_async(channel, bufname, callback)
    let l:expr = {'cmd' : 'req_parse', 'params' : {'bufname' : a:bufname}}
    call ch_sendexpr(a:channel, l:expr, {'callback': a:callback})
endf

func s:engine_req_get_hlt_async(channel, bufname, callback)
    let l:expr = {'cmd' : 'req_get_hlt', 'params' : {'bufname' : a:bufname}}
    call ch_sendexpr(a:channel, l:expr, {'callback': a:callback})
endf

func s:engine_parse_async(channel, bufname, content, callback)
    let l:expr = {'cmd' : 'parse', 'params' : {'bufname' : a:bufname, 'content' : a:content}}
    call ch_sendexpr(a:channel, l:expr, {'callback': a:callback})
endf

func s:engine_parse(channel, bufname, content)
    let l:expr = {'cmd' : 'parse', 'params' : {'bufname' : a:bufname, 'content' : a:content}}
    return ch_evalexpr(a:channel, l:expr, {'timeout' : 10000})
endf

fun! s:engine_delete_buffer(channel, bufname)
    let l:expr = {'cmd' : 'delete_buffer', 'params' : {'bufname' : a:bufname}}
    call ch_evalexpr(a:channel, l:expr)
endf

fun! s:engine_enable_log(channel, en)
    let l:expr = {'cmd' : 'enable_log', 'params' : {'enable' : a:en}}
    call ch_sendexpr(a:channel, l:expr)
endf

fun! s:engine_get_usr_info(channel, bufname, row, col, word)
    let l:expr = {'cmd' : 'get_usr_info', 'params' : {'bufname' : a:bufname, 'row' : a:row, 'col': a:col, 'word' : a:word}}
    return ch_evalexpr(a:channel, l:expr)
endf

fun! s:engine_rename(channel, bufname, usr)
    let l:expr = {'cmd' : 'rename', 'params' : {'bufname' : a:bufname, 'usr' : a:usr}}
    return ch_evalexpr(a:channel, l:expr, {'timeout' : 10000})
endf

fun! s:engine_get_cdb_files(channel)
    let l:expr = {'cmd' : 'get_cdb_files', 'params' : {}}
    return ch_evalexpr(a:channel, l:expr, {'timeout' : 10000})
endf

func HandleParse(channel, msg)
    if !empty(a:msg)
        call s:vim_clear_matches([g:clighter8_usage_priority])
        call s:engine_req_get_hlt_async(a:channel, a:msg['bufname'], 'HandleReqGetHlt')
    endif
endfunc

func HandleReqParse(channel, msg)
    if !empty(a:msg)
        let l:content = v:null
        if bufloaded(a:msg)
            let l:content = join(getbufline(a:msg, 1,'$'), "\n")
        endif

        call s:engine_parse_async(a:channel, a:msg, l:content, 'HandleParse')
    endif
endfunc

func HandleReqGetHlt(channel, msg)
    if !empty(a:msg)
        call s:engine_get_hlt_async(a:channel, a:msg, line('w0'), line('w$'), line('.'), col('.'), expand("<cword>"), 'HandleGetHlt')
    endif
endfunc

func HandleGetHlt(channel, msg)
    if empty(a:msg)
        return
    endif

    if a:msg['bufname'] != expand('%:p')
        return
    endif

    call s:vim_clear_matches([g:clighter8_syntax_priority, g:clighter8_usage_priority])
    call s:vim_highlight(a:msg['hlt'])
endfunc

func s:vim_highlight(matches)
    for [group, all_pos] in items(a:matches)
        let l:count = 0
        let l:match8 = []
        let l:priority = (group ==# 'clighter8Usage') ? g:clighter8_usage_priority : g:clighter8_syntax_priority 

        for pos in all_pos
            call add(l:match8, pos)
            let l:count += 1
            if l:count == 8
                call matchaddpos(group, l:match8, l:priority)

                let l:count = 0
                let l:match8 = []
            endif
        endfor

        call matchaddpos(group, l:match8, l:priority)
    endfor
endf

fun! s:vim_replace(usage, old, new, qflist)
    let l:pattern = ''
    for [row, column] in a:usage
        if (!empty(l:pattern))
            let l:pattern = l:pattern . '\|'
        endif

        let l:pattern = l:pattern . '\%' . row . 'l' . '\%>' . (column - 1) . 'c\%<' . (column + strlen(a:old)) . 'c' . a:old
        call add(a:qflist, {'filename':bufname(''), 'bufnr':bufnr(''), 'lnum':row, 'col':column, 'type' : 'I', 'text':"'".a:old."' was renamed to '".a:new."'"})
    endfor

    let l:cmd = '%s/' . l:pattern . '/' . a:new . '/gI'

    execute(l:cmd)
endf

fun! s:vim_clear_matches(priorities)
    for m in getmatches()
        if index(a:priorities, m['priority']) >= 0
            call matchdelete(m['id'])
        endif
    endfor
endf

fun! s:cl_load_cdb()
    let l:cdb_files = s:engine_get_cdb_files(s:channel)

    if empty(l:cdb_files)
        echohl WarningMsg | echo '[clighter8] no files to open' | echohl None
        return
    endif

    let l:all = len(l:cdb_files)
    let l:chk = 10
    let l:count = 0

    let l:new = ''
    echohl MoreMsg
    for bufname in l:cdb_files
        execute('silent! e! '. bufname)

        if index(['c', 'cpp', 'objc', 'objcpp'], &filetype) == -1
            continue
        endif

        let l:result = s:engine_parse(s:channel, bufname, join(getbufline(bufname, 1,'$'), "\n"))
        if empty(l:result)
            continue
        endif

        let l:new .= join(l:result['updates'], ' ')

        let l:count += 1
        let l:percent = 100.0 * l:count / l:all

        if l:percent >= l:chk
            redraw | echo '[clighter8] loading compilation database...' . float2nr(l:percent) . '%'
            let l:chk = l:percent + 10
        endif
    endfor
    echohl None

    if !empty(l:new)
        execute('n! ' . l:new)
    endif
endf

fun! s:cl_is_header(bufname)
    if empty(a:bufname)
        return ''
    endif

    let l:dot = -1
    let l:offset = 0
    let len = len(a:bufname)

    while l:offset < len
        if a:bufname[l:offset] ==# '.'
            let l:dot = l:offset
        endif

        let l:offset += 1
    endwhile

    if l:dot == -1 || l:dot == len(a:bufname) - 1
        return 0
    endif

    return a:bufname[l:dot + 1] ==? 'h'
endf


fun s:cl_rename(row, col)
    if !exists('s:channel')
        return
    endif

    let l:bufname = expand('%:p')
    if empty(s:engine_parse(s:channel, l:bufname, join(getbufline(l:bufname, 1,'$'), "\n")))
        echohl WarningMsg | echo '[clighter8] unable to rename' | echohl None
        return
    endif

    let l:usr_info = s:engine_get_usr_info(s:channel, l:bufname, a:row, a:col, expand("<cword>"))

    if empty(l:usr_info)
        echohl WarningMsg | echo '[clighter8] unable to rename' | echohl None
        return
    endif

    let [l:old, l:usr] = l:usr_info
    echohl Question | let l:new = input('Rename ' . l:old . ' to : ', l:old) | echohl None
    if (empty(l:new) || l:old ==# l:new)
        return
    endif

    let l:qflist = []
    let l:wnr = winnr()
    let l:bufnr = bufnr('%')
    let l:pos = getpos('.')

    let l:title = '[clighter8] rename "' . l:old . '" to "' . l:new. '"'
    let l:prompt = confirm(l:title . '?', "&Yes\n&All\n&No", 1)
    if (l:prompt == 3 || l:prompt == 0)
        return
    endif

    let l:start = reltime()

    let l:buffers = getbufinfo()
    let l:all = len(l:buffers)

    let l:count = 0
    let l:chk = 10
    echohl MoreMsg
    echo l:title. '... 0%'

    " to sort the buffers
    let l:sources = []
    let l:headers = []

    for info in l:buffers
        if s:cl_is_header(info.name) == 1
            call add(l:headers, info)
        else
            call add(l:sources, info)
        endif
    endfor

    for info in l:sources + l:headers
        execute('silent! buffer! '. info.bufnr)

        if index(['c', 'cpp', 'objc', 'objcpp'], &filetype) == -1
            continue
        endif

        if empty(s:engine_parse(s:channel, info.name, join(getbufline(info.name, 1,'$'), "\n")))
            continue
        endif

        let l:usage = s:engine_rename(s:channel, info.name, l:usr)

        if empty(l:usage) 
            continue
        endif

        if (l:prompt == 1)
            let l:yn = confirm("rename '". l:old ."' to '" .l:new. "' in " .info.name. '?', "&Yes\n&No", 1)
            if (l:yn == 2 || l:yn == 0)
                continue
            endif
        endif

        silent! call s:vim_replace(l:usage, l:old, l:new, l:qflist)

        call s:engine_parse(s:channel, info.name, join(getbufline(info.name, 1,'$'), "\n"))

        let l:count += 1
        let l:percent = 100.0 * l:count / l:all

        if l:percent >= l:chk
            redraw | echo l:title. ' ...' . float2nr(l:percent) . '%'
            let l:chk = l:percent + 10
        endif
    endfor

    call setqflist(l:qflist)
    exe 'buffer! '.l:bufnr
    call setpos('.', l:pos)
    copen
    exe l:wnr.'wincmd w'

    if l:prompt == 2
        let l:seconds = reltimefloat(reltime(l:start))
        echo printf('[clighter8] time usage: %f seconds', l:seconds)
    endif

    echohl None
endf

fun! OnTimer(bufname, timer)
    call s:engine_req_parse_async(s:channel, a:bufname, 'HandleReqParse')
endf

func! s:cl_textchanged(bufname)
    if exists('s:timer')
        call timer_stop(s:timer)
    endif

    let s:timer = timer_start(800, function('OnTimer', [a:bufname]))
endf

fun! s:cl_start()
    if exists('s:channel')
        return
    endif

    let s:channel = ch_open('localhost:8787')
    if ch_status(s:channel) ==# 'fail'
        let l:cmd = 'python '. s:script_folder_path.'/../python/engine.py '. g:clighter8_logfile
        let s:job = job_start(l:cmd, {'stoponexit': '', 'in_io': 'null', 'out_io': 'null', 'err_io': 'null'})
        let s:channel = ch_open('localhost:8787', {'waittime': 500})
        if ch_status(s:channel) ==# 'fail'
            echohl ErrorMsg | echo '[clighter8] failed start engine' | echohl None
            return
        endif
    endif

    let l:succ = s:engine_init(s:channel, g:clighter8_libclang_path, g:clighter8_global_compile_args, getcwd(), g:clighter8_highlight_whitelist, g:clighter8_highlight_blacklist)

    if l:succ == v:false
        echohl ErrorMsg | echo '[clighter8] failed to init client' | echohl None
        call ch_close(s:channel)
        unlet s:channel
        return
    endif

    call s:engine_req_parse_async(s:channel, expand('%:p'), 'HandleReqParse')

    if g:clighter8_auto_gtags == 1
        call s:check_update_gtags()
    endif

    augroup Clighter8
        autocmd!

        if g:clighter8_syntax_highlight == 1
            au BufEnter,TextChanged,TextChangedI * call s:cl_textchanged(expand('%:p'))
            au BufEnter * call s:vim_clear_matches([g:clighter8_usage_priority, g:clighter8_syntax_priority])
            au BufLeave * if exists('s:channel') | call s:engine_req_parse_async(s:channel, expand('%:p'), 'HandleReqParse') | endif
            au CursorMoved,CursorMovedI * call s:vim_clear_matches([g:clighter8_usage_priority]) | call s:engine_req_get_hlt_async(s:channel, expand('%:p'), 'HandleReqGetHlt')
            au BufDelete * call s:engine_delete_buffer(s:channel, expand('%:p'))
            au VimLeave * call s:cl_stop()
        endif

        if g:clighter8_auto_gtags == 1
            au BufWritePost,BufEnter * call s:check_update_gtags()
        endif

        if g:clighter8_format_on_save == 1
            au BufWritePre * call ClFormat()
        endif
    augroup END
endf

fun! s:cl_stop()
    augroup Clighter8
        autocmd!
    augroup END

    if exists('s:channel') && ch_status(s:channel) ==# 'open'
        call ch_close(s:channel)
        unlet s:channel
    endif

    let a:wnr = winnr()
    windo call s:vim_clear_matches([g:clighter8_usage_priority, g:clighter8_syntax_priority])
    exe a:wnr.'wincmd w'
endf

fun! ClFormat()
    if !executable('clang-format-3.9')
        return
    endif

    if v:count == 0
        let l:lines='all'
    else
        let l:lines=printf('%s:%s', v:lnum, v:lnum+v:count-1)
    endif

    execute('pyf '.s:script_folder_path.'/../third_party/clang-format.py')
endf

command! ClStart call s:cl_start()
command! ClStop call s:cl_stop()
command! ClRestart call s:cl_stop() | call s:cl_start()
command! ClShowCursorInfo if exists ('s:channel') | echo s:engine_cursor_info(s:channel, expand('%:p'), getpos('.')[1], getpos('.')[2]) | endif
command! ClShowCompileInfo if exists ('s:channel') | echo s:engine_compile_info(s:channel, expand('%:p')) | endif
command! ClEnableLog if exists ('s:channel') | call s:engine_enable_log(s:channel, v:true) | endif
command! ClDisableLog if exists ('s:channel') | call s:engine_enable_log(s:channel, v:false) | endif
command! ClLoadCdb call s:cl_start() | call s:cl_load_cdb()
command! ClRenameCursor call s:cl_rename(line('.'), col('.'))


let g:clighter8_autostart = get(g:, 'clighter8_autostart', 1)
let g:clighter8_libclang_path = get(g:, 'clighter8_libclang_path', '')
let g:clighter8_usage_priority = get(g:, 'clighter8_usage_priority', -1)
let g:clighter8_syntax_priority = get(g:, 'clighter8_syntax_priority', -2)
let g:clighter8_highlight_blacklist = get(g:, 'clighter8_highlight_blacklist', [])
let g:clighter8_highlight_whitelist = get(g:, 'clighter8_highlight_whitelist', [])
let g:clighter8_global_compile_args = get(g:, 'clighter8_global_compile_args', ['-x', 'c++', '-std=c++11'])
let g:clighter8_logfile = get(g:, 'clighter8_logfile', '/tmp/clighter8.log')
let g:clighter8_auto_gtags = get(g:, 'clighter8_auto_gtags', 1)
let g:clighter8_syntax_highlight = get(g:, 'clighter8_syntax_highlight', 1)
let g:clighter8_format_on_save = get(g:, 'clighter8_format_on_save', 0)
let g:clang_format_path = get(g:, 'clang_format_path', 'clang-format-3.9')


if g:clighter8_autostart
    au Filetype c,cpp call s:cl_start()
endif

let g:loaded_clighter8=1
