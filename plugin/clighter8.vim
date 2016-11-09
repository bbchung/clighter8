if exists('g:loaded_clighter8')
    finish
endif

let s:script_folder_path = escape( expand( '<sfile>:p:h' ), '\'   )
execute('source '. s:script_folder_path . '/../syntax/clighter8.vim')

fun! ClFormat()
    let l:lines=printf('%s:%s', v:lnum, v:lnum+v:count-1)
    execute('pyf '.s:script_folder_path.'/../python/clang-format.py')
endf

func HandleParse(channel, msg)
    if a:msg == v:true
        call s:engine_notify_highlight()
    endif
endfunc

func HandleNotifyParse(channel, msg)
    if a:msg != ""
        call s:engine_parse_async(a:msg)
    endif
endfunc

func HandleNotifyHighlight(channel, msg)
    if a:msg != ""
        call s:engine_highlight_async()
    endif
endfunc


func HandleHighlight(channel, msg)
    if a:msg[0] != expand('%:p')
        return
    endif

    for l:m in getmatches()
        if g:clighter8_syntax_priority == l:m['priority'] || g:clighter8_occurrence_priority == l:m['priority']
            call matchdelete(l:m['id'])
        endif
    endfor

    call s:do_highlight(a:msg[1][0], g:clighter8_syntax_priority)
    call s:do_highlight(a:msg[1][1], g:clighter8_occurrence_priority)
endfunc

func s:do_highlight(matches, priority)
    for [l:group, l:all_pos] in items(a:matches)
        let l:count = 0
        let l:match8 = []

        for l:pos in l:all_pos
            call add(l:match8, l:pos)
            let l:count = l:count + 1
            if l:count == 8
                call matchaddpos(l:group, l:match8, a:priority)

                let l:count = 0
                let l:match8 = []
            endif
        endfor

        call matchaddpos(l:group, l:match8, a:priority)
    endfor
endf

fun Rename()
    if !exists('s:channel')
        return
    endif
    let l:wnr = winnr()
    let l:bufnr = bufnr('%')
    let l:pos = getpos('.')
    let l:bufname = expand('%:p')
    set ei=BufWinEnter,WinEnter
    echo '[cighter8] processing...'
    silent bufdo! call s:engine_parse(expand('%:p'))
    set ei=""
    exe 'buffer! '.l:bufnr

    let expr = {"cmd" : "rename", "params" : {"bufname" : l:bufname, "row" : l:pos[1], "col": l:pos[2]}}
    let l:result = ch_evalexpr(s:channel, expr, {"timeout":10000})

    if empty(l:result) || empty(l:result['renames'])
        echo "[clighter8] can\'t rename this"
        return
    endif

    let l:old = l:result['old']
    echohl WildMenu
    let l:new = input('Rename ' . l:old . ' : ', l:old)
    echohl None
    if (empty(l:new) || l:old == l:new)
        return
    endif

    let l:qflist = []
    set ei=BufWinEnter,WinEnter
    bufdo! call s:do_replace(l:result['renames'], l:old, l:new, l:qflist)
    echo '[clighter8] processing...'
    silent bufdo! call s:engine_parse(expand('%:p'))
    set ei=""
    call setqflist(l:qflist)
    "copen
    "exe l:wnr.'wincmd w'
    exe 'buffer! '.l:bufnr
    call setpos('.', l:pos)
endf

fun! s:do_replace(renames, old, new, qflist)
    let l:bufname = expand('%:p')
    if (!has_key(a:renames, l:bufname) || empty(a:renames[l:bufname]))
        return
    endif
    let l:locations = a:renames[l:bufname]

    let l:choice = confirm("rename '". a:old ."' to '" .a:new. "' in " .l:bufname. "?", "&Yes\n&No", 1)
    if (l:choice == 2)
        return
    endif

    let l:pattern = ''
    for [l:row, l:col] in l:locations
        if (!empty(l:pattern))
            let l:pattern = l:pattern . '\|'
        endif

        let l:pattern = l:pattern . '\%' . l:row . 'l' . '\%>' . (l:col - 1) . 'c\%<' . (l:col + strlen(a:old)) . 'c' . a:old
        call add(a:qflist, {'filename':bufname(''), 'bufnr':bufnr(''), 'lnum':l:row, 'text':"'".a:old."' was renamed to '".a:new."'"})
    endfor

    let l:cmd = '%s/' . l:pattern . '/' . a:new . '/gI'

    execute(l:cmd)
endf


fun! s:engine_delete_buffer()
    let expr = {"cmd" : "delete_buffer", "params" : {"bufname" : expand('%:p')}}
    call ch_sendexpr(s:channel, expr)
endf

fun! s:engine_highlight_async()
    if index(['c', 'cpp', 'objc', 'objcpp'], &filetype) == -1
        return
    endif

    let l:pos = getpos('.')
    let expr = {"cmd" : "highlight", "params" : {"bufname" : expand('%:p'), "begin_line" : line('w0'), "end_line" : line('w$'), "row" : l:pos[1], "col": l:pos[2]}}
    call ch_sendexpr(s:channel, expr, {'callback': "HandleHighlight"})
endf

func s:engine_info()
    if index(['c', 'cpp', 'objc', 'objcpp'], &filetype) == -1
        return
    endif

    let l:pos = getpos('.')
    let expr = {"cmd" : "info", "params" : {"bufname" : expand('%:p'), "begin_line" : line('w0'), "end_line" : line('w$'), "row" : l:pos[1], "col": l:pos[2]}}
    let l:result = ch_evalexpr(s:channel, expr)
    echo l:result
endf

func s:engine_notify_parse_async()
    if index(['c', 'cpp', 'objc', 'objcpp'], &filetype) == -1
        return
    endif

    let expr = {"cmd" : "notify_parse", "params" : {"bufname" : expand('%:p')}}
    call ch_sendexpr(s:channel, expr, {'callback': "HandleNotifyParse"})
endf

func s:engine_notify_highlight()
    if index(['c', 'cpp', 'objc', 'objcpp'], &filetype) == -1
        return
    endif

    let expr = {"cmd" : "notify_highlight", "params" : {"bufname" : expand('%:p')}}
    call ch_sendexpr(s:channel, expr, {'callback': "HandleNotifyHighlight"})
endf


func s:engine_parse_async(bufname)
    if index(['c', 'cpp', 'objc', 'objcpp'], &filetype) == -1
        return
    endif

    let expr = {"cmd" : "parse", "params" : {"bufname" : a:bufname, "content" : join(getline(1,'$'), "\n")}}
    call ch_sendexpr(s:channel, expr, {'callback': "HandleParse"})
endf

func s:engine_parse(bufname)
    if index(['c', 'cpp', 'objc', 'objcpp'], &filetype) == -1
        return
    endif

    let expr = {"cmd" : "parse", "params" : {"bufname" : a:bufname, "content" : join(getline(1,'$'), "\n")}}
    call ch_evalexpr(s:channel, expr)
endf

fun! s:start_clighter8()
    let s:channel = ch_open('localhost:8787')
    if ch_status(s:channel) == "fail"
        let l:cmd = 'python '. s:script_folder_path.'/../python/engine.py'
        let s:job = job_start(l:cmd, {"stoponexit": ""})
        let s:channel = ch_open('localhost:8787', {"waittime": 5000})
        if ch_status(s:channel) == "fail"
            echo '[clighter8] failed start engine'
            return
        endif
    endif

    let expr = {"cmd" : "init_client", "params" : {"libclang" : g:clighter8_libclang_path, "cwd" : getcwd(), "hcargs" : g:clighter8_heuristic_compile_args, "gcargs" : g:clighter8_compile_args, "blacklist" : g:clighter8_highlight_blacklist}}
    let l:succ = ch_evalexpr(s:channel, expr)

    if l:succ == v:false
        echo '[clighter8] failed to init client'
        call ch_close(s:channel)
        unlet s:channel
        return
    endif

    call s:engine_notify_parse_async()

    augroup Clighter8
        autocmd!
        au BufEnter * call s:clear_match_by_priorities([g:clighter8_occurrence_priority, g:clighter8_syntax_priority]) | call s:engine_notify_parse_async()
        
        if g:clighter8_parse_mode == 0
            au CursorHold,CursorHoldI,BufEnter * call s:engine_notify_parse_async()
        else
            au TextChanged,TextChangedI,BufEnter * call s:engine_notify_parse_async()
        endif
        au CursorMoved,CursorMovedI * call s:engine_notify_highlight()
        au BufDelete * call s:engine_delete_buffer()
        au VimLeave * call s:stop_clighter8()
    augroup END
endf

fun! s:stop_clighter8()
    augroup Clighter8
        autocmd!
    augroup END

    if exists('s:channel')
        call ch_close(s:channel)
        unlet s:channel
    endif
    
    let a:wnr = winnr()
    windo call s:clear_match_by_priorities([g:clighter8_occurrence_priority, g:clighter8_syntax_priority])
    exe a:wnr.'wincmd w'
endf

fun! s:clear_match_by_priorities(priorities)
    for l:m in getmatches()
        if index(a:priorities, l:m['priority']) >= 0
            call matchdelete(l:m['id'])
        endif
    endfor
endf

fun! s:enable_log(en)
    let expr = {"cmd" : "en_log", "params" : {"enable" : a:en}}
    call ch_sendexpr(s:channel, expr)
endf


command! ClStart call s:stop_clighter8() | call s:start_clighter8()
command! ClStop call s:stop_clighter8()
command! ClShowCursorInfo if exists ('s:channel') | call s:engine_info() | endif
command! ClEnableLog if exists ('s:channel') | call s:enable_log(v:true) | endif
command! ClDisableLog if exists ('s:channel') | call s:enable_log(v:false) | endif

let g:clighter8_autostart = get(g:, 'clighter8_autostart', 1)
let g:clighter8_libclang_path = get(g:, 'clighter8_libclang_path', '')
let g:clighter8_occurrence_priority = get(g:, 'clighter8_occurrence_priority', -1)
let g:clighter8_syntax_priority = get(g:, 'clighter8_syntax_priority', -2)
let g:clighter8_highlight_blacklist = get(g:, 'clighter8_highlight_blacklist', ['clighter8InclusionDirective'])
let g:clighter8_heuristic_compile_args = get(g:, 'clighter8_heuristic_compile_args', 1)
let g:clighter8_compile_args = get(g:, 'clighter8_compile_args', [])
let g:clighter8_parse_mode = get(g:, 'clighter8_parse_mode', 0)

if g:clighter8_autostart
    au VimEnter * if index(['c', 'cpp', 'objc', 'objcpp'], &filetype) >= 0 | call s:start_clighter8() | endif
    
endif

let g:loaded_clighter8=1
