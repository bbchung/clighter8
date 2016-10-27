import logging
import json
import sys
import socket
import SocketServer as socketserver

from clang import cindex
import compilation_database
import clighter8_helper

CUSTOM_SYNTAX_GROUP = {
    cindex.CursorKind.INCLUSION_DIRECTIVE: 'clighter8InclusionDirective',
    cindex.CursorKind.MACRO_INSTANTIATION: 'clighter8MacroInstantiation',
    cindex.CursorKind.VAR_DECL: 'clighter8VarDecl',
    cindex.CursorKind.STRUCT_DECL: 'clighter8StructDecl',
    cindex.CursorKind.UNION_DECL: 'clighter8UnionDecl',
    cindex.CursorKind.CLASS_DECL: 'clighter8ClassDecl',
    cindex.CursorKind.ENUM_DECL: 'clighter8EnumDecl',
    cindex.CursorKind.PARM_DECL: 'clighter8ParmDecl',
    cindex.CursorKind.FUNCTION_DECL: 'clighter8FunctionDecl',
    cindex.CursorKind.FUNCTION_TEMPLATE: 'clighter8FunctionDecl',
    cindex.CursorKind.CXX_METHOD: 'clighter8FunctionDecl',
    cindex.CursorKind.CONSTRUCTOR: 'clighter8FunctionDecl',
    cindex.CursorKind.DESTRUCTOR: 'clighter8FunctionDecl',
    cindex.CursorKind.FIELD_DECL: 'clighter8FieldDecl',
    cindex.CursorKind.ENUM_CONSTANT_DECL: 'clighter8EnumConstantDecl',
    cindex.CursorKind.NAMESPACE: 'clighter8Namespace',
    cindex.CursorKind.CLASS_TEMPLATE: 'clighter8ClassDecl',
    cindex.CursorKind.TEMPLATE_TYPE_PARAMETER: 'clighter8TemplateTypeParameter',
    cindex.CursorKind.TEMPLATE_NON_TYPE_PARAMETER: 'clighter8TemplateNoneTypeParameter',
    cindex.CursorKind.TYPE_REF: 'clighter8TypeRef',  # class ref
    cindex.CursorKind.NAMESPACE_REF: 'clighter8NamespaceRef',  # namespace ref
    cindex.CursorKind.TEMPLATE_REF: 'clighter8TemplateRef',  # template class ref
    cindex.CursorKind.DECL_REF_EXPR:
    {
        cindex.TypeKind.FUNCTIONPROTO: 'clighter8DeclRefExprCall',  # function call
        cindex.TypeKind.ENUM: 'clighter8DeclRefExprEnum',  # enum ref
        cindex.TypeKind.TYPEDEF: 'clighter8TypeRef',  # ex: cout
    },
    # ex: designated initializer
    cindex.CursorKind.MEMBER_REF: 'clighter8DeclRefExprCall',
    cindex.CursorKind.MEMBER_REF_EXPR:
    {
        cindex.TypeKind.UNEXPOSED: 'clighter8MemberRefExprCall',  # member function call
    },
}


def _get_default_syn(cursor_kind):
    if cursor_kind.is_preprocessing():
        return 'clighter8Prepro'
    elif cursor_kind.is_declaration():
        return 'clighter8Decl'
    elif cursor_kind.is_reference():
        return 'clighter8Ref'
    else:
        return None


def _get_syntax_group(cursor, blacklist):
    group = _get_default_syn(cursor.kind)

    custom = CUSTOM_SYNTAX_GROUP.get(cursor.kind)
    if custom:
        if cursor.kind == cindex.CursorKind.DECL_REF_EXPR:
            custom = custom.get(cursor.type.kind)
            if custom:
                group = custom
        elif cursor.kind == cursor.kind == cindex.CursorKind.MEMBER_REF_EXPR:
            custom = custom.get(cursor.type.kind)
            if custom:
                group = custom
            else:
                group = 'clighter8MemberRefExprVar'
        else:
            group = custom

    if group in blacklist:
        return None

    return group


class ClientData:
    translation_units = {}
    unsaved = []
    cdb = None
    idx = None
    global_args = None


def ParseLineDelimited(data):
    result = []
    i = 0
    sz = len(data)
    start = 0
    while i < sz:
        if data[i] == '\n':
            result.append(data[start:i])
            start = i + 1

        i += 1

    return result, data[start:]


def ParseConcatenated(data):
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


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        remain = '' 
        server.clients[self.request] = ClientData()
        logging.info('socket accepted')
        while True:
            try:
                data = self.request.recv(8192).decode('utf-8')
            except:
                logging.warn('socket error')
                break

            #print("received: {0}{1}".format(data, len(data)))
            if data == '':
                break

            if remain != '': 
                data = remain + data;

            result, remain = ParseLineDelimited(data)

            for next in result:
                try:
                    decoded = json.loads(next)
                except ValueError:
                    logging.warn('json decoding failed')
                    continue

                if decoded[0] >= 0:
                    self.handle_msg(decoded[0], json.loads(decoded[1]))

        del server.clients[self.request]
        self.request = None

        num_client = len(server.clients)
        logging.info("socket closed(%d clients remains)" % num_client)
        if num_client == 0:
            logging.info('server shutdown')
            server.shutdown()
            server.server_close()

    def handle_msg(self, sn, msg):
        if msg['cmd'] == 'init_client':
            libclang = msg["params"]["libclang"]
            cwd = msg["params"]["cwd"]
            hcargs = msg["params"]["hcargs"]
            gcargs = msg["params"]["gcargs"]
            blacklist = msg["params"]["blacklist"]

            try:
                cindex.Config.set_library_file(libclang)
                logging.info('config libclang path')
            except:
                logging.warn('cannot config library path')

            succ = server.init_client(
                self.request, cwd, hcargs, gcargs, blacklist)
            self.request.sendall(json.dumps([sn, succ]).encode('utf-8'))

        elif msg['cmd'] == 'parse':
            bufname = msg['params']['bufname']
            content = str("\n".join(msg['params']['content']))

            logging.info("parse %s" % bufname)
            if not bufname:
                self.request.sendall(json.dumps([sn, False]).encode('utf-8'))
                return

            self.server.update_unsaved(self.request, bufname, content)
            self.server.parse_or_reparse(self.request, bufname)

            self.request.sendall(json.dumps([sn, True]).encode('utf-8'))

        elif msg['cmd'] == 'change':
            bufname = msg['params']['bufname']
            if server.is_dirty(self.request, bufname):
                self.request.sendall(json.dumps([sn, ""]).encode('utf-8'))
                return

            server.set_dirty(self.request, bufname)
            self.request.sendall(json.dumps([sn, bufname]).encode('utf-8'))

        elif msg['cmd'] == 'highlight':
            bufname = msg['params']['bufname']
            begin_line = msg['params']['begin_line']
            end_line = msg['params']['end_line']
            row = msg['params']['row']
            col = msg['params']['col']

            result = self.server.highlight(
                self.request, bufname, begin_line, end_line, row, col)
            self.request.sendall(json.dumps(
                [sn, [bufname, result]]).encode('utf-8'))

        elif msg['cmd'] == 'delete_buffer':
            bufname = msg['params']['bufname']
            self.server.delete_tu(self.request, bufname)

        elif msg['cmd'] == 'rename':
            bufname = msg['params']['bufname']
            row = msg['params']['row']
            col = msg['params']['col']

            #self.server.parse_or_reparse(self.request, bufname)

            if bufname not in self.server.get_all_tu(self.request):
                self.request.sendall(json.dumps([sn, {}]).encode('utf-8'))
                return

            tu = self.server.get_all_tu(self.request)[bufname][0]
            symbol = clighter8_helper.get_semantic_symbol_from_location(
                tu, bufname, row, col)

            if not symbol:
                logging.info("not symbol at %s:[%d, %d]" % (bufname, row, col))
                self.request.sendall(json.dumps([sn, {}]).encode('utf-8'))
                return

            usr = symbol.get_usr()
            if not usr:
                self.request.sendall(json.dumps([sn, {}]).encode('utf-8'))
                return

            result = {'old': symbol.spelling, 'renames': {}}

            for next_bufname, next_tu in self.server.get_all_tu(
                    self.request).iteritems():
                locations = []
                clighter8_helper.search_referenced_tokens_by_usr(
                    next_tu[0], usr, locations, symbol.spelling)

                if locations:
                    result['renames'][next_bufname] = locations

            self.request.sendall(json.dumps([sn, result]).encode('utf-8'))

        elif msg['cmd'] == 'info':
            bufname = msg['params']['bufname']
            row = msg['params']['row']
            col = msg['params']['col']

            tu = self.server.get_all_tu(self.request)[bufname][0]
            cursor = clighter8_helper.get_cursor(tu, bufname, row, col)

            if not cursor:
                self.request.sendall(json.dumps([sn, None]).encode('utf-8'))
                return


            result = {
                'cursor': str(cursor), 'cursor.kind': str(
                    cursor.kind), 'cursor.type.kind': str(
                    cursor.type.kind), 'cursor.spelling': cursor.spelling}
            self.request.sendall(json.dumps([sn, result]).encode('utf-8'))

        elif msg['cmd'] == 'en_log':
            enable = msg['params']['enable']
            if enable:
                logging.disable(logging.NOTSET)
                logging.info("enable logger")
            else:
                logging.disable(logging.CRITICAL)
                logging.info("disable logger")

            self.request.sendall(json.dumps([sn, True]).encode('utf-8'))


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    clients = {}

    def get_all_tu(self, cli):
        return self.clients[cli].translation_units

    def delete_tu(self, cli, bufname):
        try:
            del self.clients[cli].translation_units[bufname]
        except:
            pass

    def set_dirty(self, cli, bufname):
        if bufname in self.clients[cli].translation_units:
            self.clients[cli].translation_units[bufname][1] = True

    def is_dirty(self, cli, bufname):
        if bufname in self.clients[cli].translation_units:
            return self.clients[cli].translation_units[bufname][1]

        return False

    def init_client(self, cli, cwd, hcargs, gcargs, blacklist):
        try:
            self.clients[cli].idx = cindex.Index.create()
        except:
            return False

        self.clients[cli].cdb = compilation_database.CompilationDatabase.from_dir(
            cwd, hcargs)
        self.clients[cli].global_args = gcargs
        self.clients[cli].blacklist = blacklist

        return True

    def update_unsaved(self, cli, bufname, content):
        for item in self.clients[cli].unsaved:
            if item[0] == bufname:
                self.clients[cli].unsaved.remove(item)

        self.clients[cli].unsaved.append((bufname, content))

    def parse_or_reparse(self, cli, bufname):
        self.clients[cli].translation_units[
            bufname] = [self.parse(cli, bufname), False]
        return
        # if bufname not in self.clients[cli].translation_units:
        # self.clients[cli].translation_units[bufname] = [self.parse(cli, bufname), False]
        # else:
        # self.clients[cli].translation_units[bufname][0].reparse(
        # self.clients[cli].unsaved,
        # options=cindex.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD)
        # self.clients[cli].translation_units[bufname][1] = False

    def parse(self, cli, bufname):
        args = None
        if self.clients[cli].cdb:
            args = self.clients[cli].cdb.get_useful_args(
                bufname) + self.clients[cli].global_args

        try:
            return self.clients[cli].idx.parse(
                bufname,
                args,
                self.clients[cli].unsaved,
                options=cindex.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD)
        except:
            logging.warn('libclang failed to parse')
            return None

    def highlight(self, cli, bufname, begin_line, end_line, row, col):
        if bufname not in self.clients[cli].translation_units.keys():
            return [{}, {}]

        tu = self.clients[cli].translation_units[bufname][0]
        if not tu:
            return [{}, {}]

        symbol = clighter8_helper.get_semantic_symbol_from_location(
            tu, bufname, row, col)
        file = tu.get_file(bufname)

        if not file:
            return [{}, {}]

        begin = cindex.SourceLocation.from_position(
            tu, file, line=begin_line, column=1)
        end = cindex.SourceLocation.from_position(
            tu, file, line=end_line + 1, column=1)
        tokens = tu.get_tokens(
            extent=cindex.SourceRange.from_locations(begin, end))

        syntax = {}
        occurrence = {'clighter8Occurrences': []}

        for token in tokens:
            if token.kind.value != 2:  # no keyword, comment
                continue

            cursor = token.cursor
            cursor._tu = tu

            pos = [
                token.location.line, token.location.column, len(
                    token.spelling)]
            group = _get_syntax_group(
                cursor, self.clients[cli].blacklist)  # blacklist

            if group:
                if group not in syntax:
                    syntax[group] = []

                syntax[group].append(pos)

            t_symbol = None
            t_symbol = clighter8_helper.get_semantic_symbol(cursor)

            if symbol and t_symbol and symbol == t_symbol and t_symbol.spelling == token.spelling:
                occurrence['clighter8Occurrences'].append(pos)

        return [syntax, occurrence]


if __name__ == "__main__":
    logging.basicConfig(
        filename='/tmp/clighter8.log',
        filemode='w',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s')
    logging.disable(logging.CRITICAL)
    HOST, PORT = "localhost", 8787
    try:
        server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    except:
        logging.error("failed to start TCP server")
        exit()

    ip, port = server.server_address
    logging.info("server start looping")
    server.serve_forever()
