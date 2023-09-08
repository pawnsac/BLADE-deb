import sys
import clang.cindex
from clang.cindex import CursorKind
from pprint import pprint
from trimmer import remove_lines, restore_lines
from process import run_test_case
from writer import write
import time

#to-do: refine statement_tree builder

global_token_storage = {}
container_declarations = [
    CursorKind.FUNCTION_DECL,
    CursorKind.IF_STMT,
    CursorKind.WHILE_STMT,
    CursorKind.FOR_STMT,
    CursorKind.STRUCT_DECL,
    CursorKind.UNION_DECL,
]
comment = clang.cindex.TokenKind.COMMENT

labels = []


def get_addr_str(cursor):
    addr = [
        cursor.extent.start.line,
        cursor.extent.start.column,
        cursor.extent.end.line,
        cursor.extent.end.column,
    ]
    addr = [str(i) for i in addr]
    return ",".join(addr)


def find_entry_cont(entry, cont):
    result = False
    try:
        result = cont[entry]
    except:
        pass
    return result


def get_loc_str(token):
    addr = [token.location.file, token.location.line, token.location.column]
    addr = [str(i) for i in addr]
    return ",".join(addr)


def parse_struct_union(root, used_statements):
    global global_token_storage
    cont_id, statement_id = 0, 0
    addr = get_addr_str(root)
    global_token_storage[addr] = True
    maps = {}
    maps["addr"] = addr
    start_statement = True
    statement, addr_statement = [], []
    for idx, elem in enumerate(root.get_tokens()):
        if idx < 2:
            continue
        if (
            not find_entry_cont(get_loc_str(elem), used_statements)
            and elem.kind != comment
            and elem.spelling not in ["{", "}"]
        ):
            statement.append(elem.spelling)
            if start_statement:
                addr_statement.append(elem.location.line)
                addr_statement.append(elem.location.column)
                start_statement = False
            if statement[-1] == ";":
                addr_statement.append(elem.location.line)
                addr_statement.append(elem.location.column)
                if not (
                    addr_statement[0] - addr_statement[2] == 0
                    and addr_statement[1] - addr_statement[3] == 0
                ):
                    addr_statement = [str(i) for i in addr_statement]
                    addr_statement = ",".join(addr_statement)
                    if not find_entry_cont(addr_statement, global_token_storage):
                        global_token_storage[addr_statement] = True
                        maps[f"st_{statement_id}"] = [
                            " ".join(statement),
                            addr_statement,
                        ]
                statement = []
                statement_id += 1
                start_statement = True
                addr_statement = []
            used_statements[get_loc_str(elem)] = True
    return maps


def get_bounds(root):
    bounds = []
    global global_token_storage
    start = True
    addr = get_addr_str(root)
    end = None
    if root.kind == CursorKind.IF_STMT:
        els = False
        for idx, elem in enumerate(root.get_tokens()):
            if elem.spelling == "{" and start:
                st = get_loc_str(elem)
                st = st.split(",")[1:]
                st = [int(el) for el in st]
                st = [st[0], st[1] + 1]
                st = [str(el) for el in st]
                st = addr.split(",")[:2] + st
                st = ",".join(st)
                bounds.append(st)
                start = False
            if elem.spelling == "}":
                st = get_loc_str(elem)
                st = st.split(",")[1:]
                st = [int(el) for el in st]
                en = [st[0], st[1] + 1]
                st = [st[0], max(st[1] - 1, 1)] + en
                st = [str(el) for el in st]
                st = ",".join(st)
                end = st
            if elem.spelling == "else":
                st = get_loc_str(elem)
                st = st.split(",")[1:]
                st = [int(el) for el in st]
                en = [st[0], st[1] + 6]
                st += en
                st = [str(el) for el in st]
                st = ",".join(st)
                if not find_entry_cont(st, global_token_storage):
                    els = True
                    bounds.append(st)
                    global_token_storage[st] = True
                    break
        bounds.append(end)
        if els:
            st = addr.split(",")[2:]
            st = [int(el) for el in st]
            en = [st[0], max(st[1] - 2, 1)]
            st = en + st
            st = [str(el) for el in st]
            st = ",".join(st)
            bounds.append(st)
    if root.kind == CursorKind.WHILE_STMT:
        for idx, elem in enumerate(root.get_tokens()):
            if elem.spelling == "{" and start:
                st = get_loc_str(elem)
                st = st.split(",")[1:]
                st = [int(el) for el in st]
                st = [st[0], st[1] + 1]
                st = [str(el) for el in st]
                st = addr.split(",")[:2] + st
                st = ",".join(st)
                bounds.append(st)
                start = False
                break

        st = addr.split(",")[2:]
        st = [int(el) for el in st]
        en = [st[0], st[1] - 1]
        st = en + st
        st = [str(el) for el in st]
        st = ",".join(st)
        bounds.append(st)
    return bounds


def parse_container(root, used_containers={}, used_statements={}):
    global global_token_storage
    global itr_load
    cont_id, statement_id = 0, 0
    start_statement = True
    addr = get_addr_str(root)
    global_token_storage[addr] = True
    maps = {}
    maps["addr"] = addr
    container_cond = False if root.kind in container_declarations else True
    statement = []
    addr_statement = []
    for idx, elem in enumerate(root.get_tokens()):
        if elem.cursor == root:
            if elem.spelling == "(":
                container_cond = False
            elif elem.spelling == ")":
                container_cond = True
            continue
        if elem.cursor.kind in container_declarations:
            container_cond = False
            if elem.spelling == "(":
                container_cond = False
            elif elem.spelling in [")", "}", ";"]:
                container_cond = True
            if not find_entry_cont(get_addr_str(elem.cursor), used_containers):
                if elem.cursor.kind in [CursorKind.STRUCT_DECL, CursorKind.UNION_DECL]:
                    maps[f"cont_{cont_id}"] = parse_struct_union(
                        elem.cursor, used_statements
                    )
                else:
                    maps[f"cont_{cont_id}"] = parse_container(
                        elem.cursor, used_containers, used_statements
                    )
                cont_id += 1
                addr_cont = get_addr_str(elem.cursor)
                used_containers[addr_cont] = True
        else:
            if (
                not find_entry_cont(get_loc_str(elem), used_statements)
                and elem.kind != comment
                and elem.spelling not in ["{", "}"]
                and container_cond
            ):
                statement.append(elem.spelling)
                if start_statement:
                    addr_statement.append(elem.location.line)
                    addr_statement.append(elem.location.column)
                    start_statement = False
                if statement[-1] in [";", ">"] or (
                    elem.cursor.kind == CursorKind.LABEL_STMT and elem.spelling == ":"
                ):
                    addr_statement.append(elem.location.line)
                    addr_statement.append(elem.location.column)
                    if not (
                        addr_statement[0] - addr_statement[2] == 0
                        and addr_statement[1] - addr_statement[3] == 0
                    ):
                        addr_statement = [str(i) for i in addr_statement]
                        addr_statement = ",".join(addr_statement)
                        if not find_entry_cont(addr_statement, global_token_storage):
                            global_token_storage[addr_statement] = True
                            maps[f"st_{statement_id}"] = [
                                " ".join(statement),
                                addr_statement,
                            ]
                    statement = []
                    statement_id += 1
                    start_statement = True
                    addr_statement = []
                used_statements[get_loc_str(elem)] = True
    if root.kind in [CursorKind.IF_STMT, CursorKind.WHILE_STMT]:
        maps["bounds"] = get_bounds(root)
    return maps


def reset_global_storage():
    global global_token_storage
    global_token_storage = {}


def get_global_storage():
    global global_token_storage
    return global_token_storage
