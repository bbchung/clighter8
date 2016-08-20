if exists('g:loaded_clighter8')
    finish
endif

let s:script_folder_path = escape( expand( '<sfile>:p:h' ), '\'   )
execute('source '. s:script_folder_path . '/../syntax/clighter8.vim')

func HandleParse(channel, msg)
    if a:msg == v:true
        call s:notify_highlight()
    endif
endfunc

func HandleChange(channel, msg)
    if a:msg != ""
        call s:notify_parse(a:msg)
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
        let s:count = 0
        let s:match8 = []

        for l:pos in l:all_pos
            call add(s:match8, l:pos)
            let s:count = s:count + 1
            if s:count == 8
                call matchaddpos(l:group, s:match8, a:priority)

                let s:count = 0
                let s:match8 = []
            endif
        endfor

        call matchaddpos(l:group, s:match8, a:priority)
    endfor
endf

fun Rename()
    let l:wnr = winnr()
    "let l:bufnr = bufnr('')
    let s:pos = getpos('.')
    let l:bufname = expand('%:p')
    bufdo! call s:req_parse(expand('%:p'))
    bn!

    let str = json_encode({"cmd" : "rename", "params" : {"bufname" : l:bufname, "row" : s:pos[1], "col": s:pos[2]}})
    let s:result = ch_evalexpr(s:channel, str)

    if empty(s:result) || empty(s:result['renames'])
        return
    endif

    let s:old = s:result['old']
    echohl WildMenu
    let s:new = input('Rename ' . s:old . ' : ', s:old)
    echohl None
    if (empty(s:new) || s:old == s:new)
        return
    endif

    let l:qflist = []
    bufdo! call s:do_replace(s:result['renames'], s:old, s:new, l:qflist)
    bn!
    bufdo! call s:req_parse(expand('%:p'))
    bn!
    call setqflist(l:qflist)
    "copen
    "exe l:wnr.'wincmd w'
    "exe 'buffer! '.l:bufnr
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


fun! s:notify_delete_buffer()
    let str = json_encode({"cmd" : "delete_buffer", "params" : {"bufname" : expand('%:p')}})
    call ch_sendexpr(s:channel, str)
endf

fun! s:notify_highlight()
    if index(['c', 'cpp', 'objc', 'objcpp'], &filetype) == -1
        return
    endif

    let s:pos = getpos('.')
    let str = json_encode({"cmd" : "highlight", "params" : {"bufname" : expand('%:p'), "begin_line" : line('w0'), "end_line" : line('w$'), "row" : s:pos[1], "col": s:pos[2]}})
    call ch_sendexpr(s:channel, str, {'callback': "HandleHighlight"})
endf

func s:req_info()
    if index(['c', 'cpp', 'objc', 'objcpp'], &filetype) == -1
        return
    endif

    let s:pos = getpos('.')
    let str = json_encode({"cmd" : "info", "params" : {"bufname" : expand('%:p'), "begin_line" : line('w0'), "end_line" : line('w$'), "row" : s:pos[1], "col": s:pos[2]}})
    let l:result = ch_evalexpr(s:channel, str)
    echo l:result
endf

func s:notify_change()
    if index(['c', 'cpp', 'objc', 'objcpp'], &filetype) == -1
        return
    endif

    let str = json_encode({"cmd" : "change", "params" : {"bufname" : expand('%:p')}})
    call ch_sendexpr(s:channel, str, {'callback': "HandleChange"})
endf

func s:notify_parse(bufname)
    if index(['c', 'cpp', 'objc', 'objcpp'], &filetype) == -1
        return
    endif

    let str = json_encode({"cmd" : "parse", "params" : {"bufname" : a:bufname, "content" : getline(1,'$')}})
    call ch_sendexpr(s:channel, str, {'callback': "HandleParse"})
endf

func s:req_parse(bufname)
    if index(['c', 'cpp', 'objc', 'objcpp'], &filetype) == -1
        return
    endif

    let str = json_encode({"cmd" : "parse", "params" : {"bufname" : a:bufname, "content" : getline(1,'$')}})
    call ch_evalexpr(s:channel, str)
endf

fun! s:start_clighter8()
    let s:channel = ch_open('localhost:8787')
    if ch_status(s:channel) == "fail"
        let l:cmd = 'python '. s:script_folder_path.'/../python/engine.py'
        let s:job = job_start(l:cmd, {"stoponexit": ""})
        let s:channel = ch_open('localhost:8787', {"waittime": 1000})
    endif

    let str = json_encode({"cmd" : "init", "params" : {"libclang" : g:clighter8_libclang_path, "cwd" : getcwd(), "hcargs" : g:clighter8_heuristic_compile_args, "gcargs" : g:clighter8_compile_args, "blacklist" : g:clighter8_highlight_blacklist}})
    let l:succ = ch_evalexpr(s:channel, str)

    if l:succ == v:false
        echo 'failed to init libclang'
        call ch_close(s:channel)
        unlet s:channel
        return
    endif

    call s:notify_change()

    augroup Clighter8
        autocmd!
        au TextChanged,TextChangedI,WinEnter,BufWinEnter * call s:notify_change()
        au CursorMoved,CursorMovedI * call s:notify_highlight()
        au BufDelete * call s:notify_delete_buffer()
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

command! StartClighter8 call s:start_clighter8()
command! StopClighter8 call s:stop_clighter8()
command! ShowInfo call s:req_info()

let g:clighter8_autostart = get(g:, 'clighter8_autostart', 1)
let g:clighter8_libclang_path = get(g:, 'clighter8_libclang_path', '')
let g:clighter8_occurrence_priority = get(g:, 'clighter8_occurrence_priority', -1)
let g:clighter8_syntax_priority = get(g:, 'clighter8_syntax_priority', -2)
let g:clighter8_highlight_blacklist = get(g:, 'clighter8_highlight_blacklist', ['clighter8InclusionDirective'])
let g:clighter8_heuristic_compile_args = get(g:, 'clighter8_heuristic_compile_args', 1)
let g:clighter8_compile_args = get(g:, 'clighter8_compile_args', [])

if g:clighter8_autostart
    au VimEnter *.c,*.cpp,*.h,*.hpp call s:start_clighter8()
endif

let g:loaded_clighter8=1
