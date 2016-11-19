from clang import cindex

def get_cursor(tu, filepath, row, col):
    if not tu:
        return None

    return cindex.Cursor.from_location(
        tu,
        cindex.SourceLocation.from_position(tu,
                                            tu.get_file(filepath),
                                            row,
                                            col))

def get_semantic_symbol_from_location(tu, filepath, row, col):
    cursor = get_cursor(tu, filepath, row, col);
    if not cursor:
        return None

    if cursor.location.line != row or col < cursor.location.column or col >= cursor.location.column + \
            len(cursor.spelling):
        return None

    return get_semantic_symbol(cursor)


def get_semantic_symbol(cursor):
    if cursor.kind == cindex.CursorKind.MACRO_DEFINITION:
        return cursor

    symbol = cursor.get_definition()
    if not symbol:
        symbol = cursor.referenced

    if not symbol:
        return None

    if symbol.kind == cindex.CursorKind.CONSTRUCTOR or symbol.kind == cindex.CursorKind.DESTRUCTOR:
        symbol = symbol.semantic_parent

    return symbol


def search_by_usr(tu, usr, result):
    if not tu:
        return None

    tokens = tu.cursor.get_tokens()
    for token in tokens:
        cursor = token.cursor
        cursor._tu = tu

        symbol = get_semantic_symbol(cursor)
        if symbol and symbol.get_usr() == usr:
            result.append((token.location.line, token.location.column))

def get_compile_args_from_cdb(cdb, bufname):
    if not cdb:
        return[]

    cmds = cdb.getCompileCommands(bufname) 
    if cmds == None:
        return []

    result = list(cmds[0].arguments)
    result.pop()
    result.pop(0)

    return result
