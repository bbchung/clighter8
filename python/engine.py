import logging
import json
import SocketServer as socketserver
import threading

from clang import cindex
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


class BufferData:
    def __init__(self):
        self.tu = None
        self.compile_args = None
        self.parse_busy = False
        self.hlt_busy = False


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


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def __init__(self, request, client_addres, server):
        self.buffer_data = {}
        self.unsaved = []
        self.cdb = None
        self.idx = None
        self.global_compile_args = None

        socketserver.BaseRequestHandler.__init__(self, request, client_addres, server)
    

    def handle(self):
        remain = ''
        server.add_client(self.request)
        logging.info('socket accepted')
        while True:
            try:
                data = self.request.recv(8192)
            except:
                logging.warn('socket error')
                break

            #print("received: {0}{1}".format(data, len(data)))
            if data == '':
                break

            if remain != '':
                data = remain + data

            remain = parse_line_delimited(data, self.handle_json)

        self.request.close()

        server.remove_client(self.request)

    def handle_json(self, json_str):
        try:
            decoded = json.loads(json_str)
        except ValueError:
            logging.warn('json decoding failed')

        if decoded[0] >= 0:
            self.handle_msg(decoded[0], decoded[1])

    def safe_sendall(self, msg):
        try:
            self.request.sendall(msg)
        except:
            pass

    def handle_msg(self, sn, msg):
        if msg['cmd'] == 'init':
            libclang = msg["params"]["libclang"]
            cwd = msg["params"]["cwd"]
            global_compile_args = msg["params"]["global_compile_args"]
            blacklist = msg["params"]["blacklist"]

            try:
                cindex.Config.set_library_file(libclang)
                logging.info('config libclang path')
            except:
                logging.warn('cannot config library path')

            succ = self.init(cwd, global_compile_args, blacklist)
            self.safe_sendall(json.dumps([sn, succ]))

        elif msg['cmd'] == 'parse':
            bufname = msg['params']['bufname'].encode("utf-8")
            content = msg['params']['content'].encode("utf-8")

            logging.info("parse %s" % bufname)
            if not bufname:
                self.safe_sendall(json.dumps([sn, '']))
                return

            self.update_unsaved(bufname, content)
            self.parse(bufname)

            self.safe_sendall(json.dumps([sn, bufname]))

        elif msg['cmd'] == 'req_parse':
            bufname = msg['params']['bufname'].encode("utf-8")
            if self.is_parse_busy(bufname):
                self.safe_sendall(json.dumps([sn, ""]))
                return

            self.set_parse_busy(bufname)
            self.safe_sendall(json.dumps([sn, bufname]))

        elif msg['cmd'] == 'req_get_hlt':
            bufname = msg['params']['bufname'].encode("utf-8")

            if self.is_hlt_busy(bufname):
                self.safe_sendall(json.dumps([sn, ""]))
                return

            self.set_hlt_busy(bufname)
            self.safe_sendall(json.dumps([sn, bufname]))

        elif msg['cmd'] == 'get_hlt':
            bufname = msg['params']['bufname'].encode("utf-8")
            begin_line = msg['params']['begin_line']
            end_line = msg['params']['end_line']
            row = msg['params']['row']
            col = msg['params']['col']

            self.unset_hlt_busy(bufname)
            hlt = self.get_hlt(
                bufname, begin_line, end_line, row, col)

            result = {'bufname': bufname, 'hlt': hlt}
            self.safe_sendall(json.dumps(
                [sn, result]))


        elif msg['cmd'] == 'delete_buffer':
            bufname = msg['params']['bufname'].encode("utf-8")
            self.delete_buffer_data(bufname)

        elif msg['cmd'] == 'get_usr_info':
            bufname = msg['params']['bufname'].encode("utf-8")
            row = msg['params']['row']
            col = msg['params']['col']

            ctx = self.get_buffer_data(bufname)
            if not ctx or not ctx.tu:
                self.safe_sendall(json.dumps([sn, '']))
                return

            symbol = clighter8_helper.get_semantic_symbol_from_location(
                ctx.tu, bufname, row, col)

            if not symbol:
                self.safe_sendall(json.dumps([sn, '']))
                return

            self.safe_sendall(json.dumps(
                [sn, [symbol.spelling, symbol.get_usr()]]))

        elif msg['cmd'] == 'rename':
            bufname = msg['params']['bufname'].encode("utf-8")
            usr = msg['params']['usr']

            buffer_data = self.get_buffer_data(bufname)
            if not buffer_data:
                return

            refs = []
            clighter8_helper.search_by_usr(self.get_buffer_data(
                bufname).tu, usr, refs)

            self.safe_sendall(json.dumps([sn, refs]))

        elif msg['cmd'] == 'cursor_info':
            bufname = msg['params']['bufname'].encode("utf-8")
            row = msg['params']['row']
            col = msg['params']['col']

            tu = self.get_buffer_data(bufname).tu
            cursor = clighter8_helper.get_cursor(tu, bufname, row, col)

            if not cursor:
                self.safe_sendall(json.dumps([sn, None]))
                return

            result = {
                'cursor': str(cursor), 'cursor.kind': str(
                    cursor.kind), 'cursor.type.kind': str(
                    cursor.type.kind), 'cursor.spelling': cursor.spelling, 'location': [
                    cursor.location.line, cursor.location.column]}
            self.safe_sendall(json.dumps([sn, result]))

        elif msg['cmd'] == 'compile_info':
            bufname = msg['params']['bufname'].encode("utf-8")

            result = self.get_buffer_data(
                bufname).compile_args + self.get_global_compile_args()
            self.safe_sendall(json.dumps([sn, result]))

        elif msg['cmd'] == 'enable_log':
            enable = msg['params']['enable']
            if enable:
                logging.disable(logging.NOTSET)
                logging.info("enable logger")
            else:
                logging.disable(logging.CRITICAL)
                logging.info("disable logger")

            self.safe_sendall(json.dumps([sn, True]))

    def get_buffer_data(self, bufname):
        if bufname in self.buffer_data:
            return self.buffer_data[bufname]

        return None

    def delete_buffer_data(self, bufname):
        if bufname in self.buffer_data:
            del self.buffer_data[bufname]

    def set_parse_busy(self, bufname):
        if bufname in self.buffer_data:
            self.buffer_data[bufname].parse_busy = True

    def is_parse_busy(self, bufname):
        if bufname in self.buffer_data:
            return self.buffer_data[bufname].parse_busy

        return False

    def set_hlt_busy(self, bufname):
        if bufname in self.buffer_data:
            self.buffer_data[bufname].hlt_busy = True

    def unset_hlt_busy(self, bufname):
        if bufname in self.buffer_data:
            self.buffer_data[bufname].hlt_busy = False

    def is_hlt_busy(self, bufname):
        if bufname in self.buffer_data:
            return self.buffer_data[bufname].hlt_busy

        return False

    def init(self, cwd, global_compile_args, blacklist):
        try:
            self.idx = cindex.Index.create()
            self.cdb = cindex.CompilationDatabase.fromDirectory(cwd)
        except cindex.CompilationDatabaseError:
            logging.warn('compilation data not found')
        except:
            return False

        self.global_compile_args = global_compile_args
        self.blacklist = blacklist

        return True

    def update_unsaved(self, bufname, content):
        for item in self.unsaved:
            if item[0] == bufname:
                self.unsaved.remove(item)

        self.unsaved.append((bufname, content))

    def parse(self, bufname):
        if bufname not in self.buffer_data:
            self.buffer_data[bufname] = BufferData()
            self.buffer_data[bufname].compile_args = clighter8_helper.get_compile_args_from_cdb(
                self.cdb, bufname)

        compile_args = self.buffer_data[
            bufname].compile_args + self.global_compile_args

        self.buffer_data[bufname].parse_busy = False

        try:
            if self.buffer_data[bufname].tu:
                self.buffer_data[bufname].tu.reparse(
                    self.unsaved,
                    cindex.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD)
            else:
                self.buffer_data[bufname].tu = self.idx.parse(
                    bufname,
                    compile_args if compile_args else None,
                    self.unsaved,
                    options=cindex.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD)
        except:
            del self.buffer_data[bufname]
            logging.warn('libclang failed to parse')
            return

        for i in self.buffer_data[bufname].tu.get_includes():
            if i.is_input_file:
                continue

            if i.include not in self.buffer_data:
                self.buffer_data[
                    i.include.name] = BufferData()

            self.buffer_data[i.include.name].compile_args = self.buffer_data[bufname].compile_args

    def get_hlt(self, bufname, begin_line, end_line, row, col):
        if bufname not in self.buffer_data:
            return {}

        tu = self.buffer_data[bufname].tu
        if not tu:
            return {}

        symbol = clighter8_helper.get_semantic_symbol_from_location(
            tu, bufname, row, col)
        
        tu_file = tu.get_file(bufname)

        if not tu_file:
            return {}

        begin = cindex.SourceLocation.from_position(
            tu, tu_file, line=begin_line, column=1)
        end = cindex.SourceLocation.from_position(
            tu, tu_file, line=end_line + 1, column=1)
        tokens = tu.get_tokens(
            extent=cindex.SourceRange.from_locations(begin, end))

        result = {}

        if symbol:
            result['clighter8Refs'] = []

        for token in tokens:
            if token.kind.value != 2:  # no keyword, comment
                continue

            cursor = token.cursor
            cursor._tu = tu

            pos = [
                token.location.line, token.location.column, len(
                    token.spelling)]
            group = _get_syntax_group(
                cursor, self.blacklist)  # blacklist

            if group:
                if group not in result:
                    result[group] = []

                result[group].append(pos)

            t_symbol = None
            t_symbol = clighter8_helper.get_semantic_symbol(cursor)

            if symbol and t_symbol and symbol == t_symbol and t_symbol.spelling == token.spelling:
                result['clighter8Refs'].append(pos)

        return result




class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):

    def __init__(self, addr, handler):
        self.__clients = set()
        self.__lock = threading.Lock()

        socketserver.TCPServer.__init__(self, addr, handler)

    def add_client(self, cli):
        with self.__lock:
            self.__clients.add(cli)

    def remove_client(self, cli):
        with self.__lock:
            self.__clients.remove(cli)
            num_client = len(self.__clients)
            logging.info("socket closed(%d clients remains)" % num_client)
            if num_client == 0:
                logging.info('server shutdown')
                print('server shutdown')
                server.shutdown()
                server.server_close()


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
    logging.info("server start at %s:%d" % (ip, port))
    server.serve_forever()
