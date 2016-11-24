from clang import cindex

KindToGroup = {
    cindex.CursorKind.STRUCT_DECL: 'clighter8StructDecl',
    cindex.CursorKind.UNION_DECL: 'clighter8UnionDecl',
    cindex.CursorKind.CLASS_DECL: 'clighter8ClassDecl',
    cindex.CursorKind.ENUM_DECL: 'clighter8EnumDecl',
    cindex.CursorKind.FIELD_DECL: 'clighter8FieldDecl',
    cindex.CursorKind.ENUM_CONSTANT_DECL: 'clighter8EnumConstantDecl',
    cindex.CursorKind.FUNCTION_DECL: 'clighter8FunctionDecl',
    cindex.CursorKind.VAR_DECL: 'clighter8VarDecl',
    cindex.CursorKind.PARM_DECL: 'clighter8ParmDecl',
    cindex.CursorKind.TYPEDEF_DECL: 'clighter8TypedefDecl',
    cindex.CursorKind.CXX_METHOD: 'clighter8CxxMethod',
    cindex.CursorKind.NAMESPACE: 'clighter8Namespace',
    cindex.CursorKind.CONSTRUCTOR: 'clighter8Constructor',
    cindex.CursorKind.DESTRUCTOR: 'clighter8Destructor',
    cindex.CursorKind.TEMPLATE_TYPE_PARAMETER: 'clighter8TemplateTypeParameter',
    cindex.CursorKind.TEMPLATE_NON_TYPE_PARAMETER: 'clighter8TemplateNoneTypeParameter',
    cindex.CursorKind.FUNCTION_TEMPLATE: 'clighter8FunctionTemplate',
    cindex.CursorKind.CLASS_TEMPLATE: 'clighter8ClassTemplate',
    cindex.CursorKind.TYPE_REF: 'clighter8TypeRef',
    cindex.CursorKind.TEMPLATE_REF: 'clighter8TemplateRef',  # template class ref
    cindex.CursorKind.NAMESPACE_REF: 'clighter8NamespaceRef',  # namespace ref
    cindex.CursorKind.MEMBER_REF: 'clighter8MemberRef',
    cindex.CursorKind.VARIABLE_REF: 'clighter8variableRef',
    cindex.CursorKind.DECL_REF_EXPR: 'clighter8DeclRefExpr',
    cindex.CursorKind.MEMBER_REF_EXPR: 'clighter8MemberRefExpr',
    cindex.CursorKind.CALL_EXPR: 'clighter8CallExpr',
    cindex.CursorKind.MACRO_INSTANTIATION: 'clighter8MacroInstantiation',
    cindex.CursorKind.INCLUSION_DIRECTIVE: 'clighter8InclusionDirective',
}


def get_hlt_group(cursor, whitelist, blacklist):
    group = KindToGroup.get(cursor.kind)

    if not group:
        if cursor.kind.is_declaration():
            group = 'clighter8Decl'
        elif cursor.kind.is_reference():
            group = 'clighter8Ref'
        elif cursor.kind.is_expression():
            group = 'clighter8Expr'
        elif cursor.kind.is_statement():
            group = 'clighter8Stat'
        elif cursor.kind.is_preprocessing():
            group = 'clighter8Prepro'

    if whitelist:
        if group not in whitelist:
            return None

        return group

    if blacklist:
        if group in blacklist:
            return None

    return group


def parse_line_delimited(data, on_parse):
    i = 0
    sz = len(data)
    start = 0
    while i < sz:
        if data[i] == '\n':
            on_parse(data[start:i])
            start = i + 1

        i += 1

    return data[start:]


def parse_concatenated(data):
    result = []
    quatos = 0
    i = 0
    sz = len(data)
    depth = 0
    start = 0
    used = -1
    while i < sz:
        if i > 0 and data[i - 1] == "\\":
            i += 1
            continue

        if data[i] == '"':
            quatos += 1
        elif data[i] == '[' and quatos % 2 == 0:
            depth += 1
        elif data[i] == ']' and quatos % 2 == 0:
            depth -= 1
            if depth == 0:
                used = i
                result.append(data[start:i + 1])
                start = i + 1

        i += 1

    return result, data[used + 1:]


def get_cursor(tu, bufname, row, col):
    if not tu:
        return None

    return cindex.Cursor.from_location(
        tu,
        cindex.SourceLocation.from_position(tu,
                                            tu.get_file(bufname),
                                            row,
                                            col))


def get_semantic_symbol_from_location(tu, bufname, row, col):
    cursor = get_cursor(tu, bufname, row, col)
    if not cursor:
        return None

    symbol = get_semantic_symbol(cursor)

    if not symbol:
        return None

    if cursor.location.line != row or col < cursor.location.column or col >= cursor.location.column + \
            len(symbol.spelling):
        return None

    return symbol


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

        if not symbol or symbol.get_usr() != usr or token.spelling != symbol.spelling:
            continue

        result.append((token.location.line, token.location.column))


def get_compile_args_from_cdb(cdb, bufname):
    if not cdb:
        return[]

    cmds = cdb.getCompileCommands(bufname)
    if cmds is None:
        return []

    result = list(cmds[0].arguments)
    result.pop()
    result.pop(0)

    return result
