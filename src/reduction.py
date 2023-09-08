from trimmer import remove_lines, restore_lines
from process import run_test_case
from writer import write
from multiprocessing import Pool
import os
from tqdm import tqdm
import numpy as np


class Reduction:
    def __init__(self, last_fit, oracle_cmd, file_name, n_max=5, back_max=5):
        self.last_fit = last_fit
        self.oracle_cmd = oracle_cmd
        self.progress_bar = None
        self.last_updated_addr = len(last_fit)
        self.n_max = int(n_max)
        self.stored_addr = []
        self.prev_remmed = 0
        self.file_name = file_name
        self.back_max = int(back_max)
        self.current_back = 0

    def __getstate__(self):
        """This is called before pickling."""
        state = self.__dict__.copy()
        del state["progress_bar"]
        return state

    def __setstate__(self, state):
        """This is called while unpickling."""
        self.__dict__.update(state)

    def clear_screen(self):
        os.system("cls" if os.name in ("nt", "dos") else "clear")

    def start_progress(self, lines):
        self.last_updated_addr
        try:
            self.progress_bar.close()
        except:
            pass
        self.progress_bar = tqdm(total=lines)
        self.last_updated_addr = lines

    def reduce(self, inp):
        addr, idx, bounds_check = inp
        to_write = None
        if not bounds_check:
            addr_new = addr.split(",")
            addr_new = [int(i) for i in addr_new]
            to_write = remove_lines(self.last_fit, addr_new)
        else:
            to_write = self.last_fit.copy()
            for add in addr:
                addr_new = add.split(",")
                addr_new = [int(i) for i in addr_new]
                to_write = remove_lines(to_write, addr_new)
        write(to_write, f"processing/{idx}/{self.file_name}")
        if run_test_case(f"./{self.oracle_cmd}", f"processing/{idx}/") == 0:
            return True
        else:
            return False

    def batch_maker(self, queue):
        if len(queue) == 0:
            return []
        end_addr = queue[0][0].split(",")[2:]
        out = []
        for adr, idx in queue:
            addr = adr.split(",")[:2] + end_addr
            addr = addr = ",".join(addr)
            out.append(addr)
        return out

    def reduction(self, maps):
        red_whole = self.reduce((maps["addr"], 1, False))
        nodes = list(maps.keys())
        if red_whole:
            addr = maps["addr"]
            addr_new = addr.split(",")
            addr_new = [int(i) for i in addr_new]
            self.clear_screen()
            self.last_fit = remove_lines(self.last_fit, addr_new)
            self.progress_bar.update(self.last_updated_addr - int(addr.split(",")[0]))
            self.last_updated_addr = int(addr.split(",")[0])
            print(f"[block with location:{addr} removed]\n")
            print(
                f"prev_removed:{self.prev_remmed}",
                f"Down_traversal_activated: {self.back_max==self.current_back}",
            )
            return
        elif len(maps) == 3 and nodes[1].startswith("st") and nodes[2] == "bounds":
            if self.reduce((maps["bounds"], "1", True)):
                to_change = self.last_fit.copy()
                for add in maps["bounds"]:
                    addr_new = add.split(",")
                    addr_new = [int(i) for i in addr_new]
                    to_change = remove_lines(to_change, addr_new)
                self.last_fit = to_change
                print("bounds removed: ", maps["bounds"])
            self.stored_addr.append((maps[nodes[1]][1], 1))
            return

        if (len(self.last_fit) - int(maps["addr"].split(",")[2])) >= 0.10 * len(
            self.last_fit
        ):
            try:
                curr_list = self.stored_addr[: self.back_max]
                if int(curr_list[-1][0].split(",")[0]) - int(
                    maps["addr"].split(",")[2]
                ) >= 0.05 * len(self.last_fit):
                    self.current_back = self.back_max
                else:
                    self.current_back = 0
            except:
                self.current_back = 0
        else:
            self.current_back = 0
        nodes.reverse()
        loop_itr = 0
        bounds_done = False
        while True:
            if nodes[loop_itr].startswith("cont"):
                self.reduction(maps[nodes[loop_itr]])
                loop_itr += 1
                if loop_itr >= len(maps):
                    if self.reduce((maps["bounds"], "1", True)):
                        to_change = self.last_fit.copy()
                        for add in maps["bounds"]:
                            addr_new = add.split(",")
                            addr_new = [int(i) for i in addr_new]
                            to_change = remove_lines(to_change, addr_new)
                        self.last_fit = to_change
                        print("bounds removed: ", maps["bounds"])
                    break
            queue = []
            while not (len(queue) == self.n_max or loop_itr == len(nodes)):
                if not nodes[loop_itr] in ["addr", "bounds"]:
                    node = maps[nodes[loop_itr]]
                    addr = None
                    if type(node) == dict:  # signifying a block
                        addr = node["addr"]
                    else:  # signifying a statement
                        addr = node[1]
                    queue.append((addr, loop_itr))
                loop_itr += 1
            if len(queue) == 0:
                if nodes[0] == "bounds":
                    if self.reduce((maps["bounds"], "1", True)):
                        to_change = self.last_fit.copy()
                        for add in maps["bounds"]:
                            addr_new = add.split(",")
                            addr_new = [int(i) for i in addr_new]
                            to_change = remove_lines(to_change, addr_new)
                        self.last_fit = to_change
                        print("bounds removed: ", maps["bounds"])
                break
            queue_prev = self.stored_addr[: self.current_back]
            batch = self.batch_maker(queue)
            batch_prev = self.batch_maker(queue_prev)
            batch_processing = batch_prev + batch
            working_indx = -1
            pool = Pool(processes=len(batch_processing))
            pool_inputs_prev = [
                (addr, f"_{idx+1}", False) for idx, addr in enumerate(batch_prev)
            ]
            pool_inputs_next = [
                (addr, idx + 1, False) for idx, addr in enumerate(batch)
            ]
            pool_inputs = pool_inputs_prev + pool_inputs_next
            reduce_results = pool.map(self.reduce, pool_inputs)
            pool.close()
            results_next = reduce_results[len(batch_prev) :]
            results_prev = reduce_results[: len(batch_prev)]
            indx_results = np.where(results_next)[0]
            if len(indx_results) != 0:
                working_indx = indx_results[-1]
                addr = batch[working_indx]
                addr_new = addr.split(",")
                addr_new = [int(i) for i in addr_new]
                self.last_fit = remove_lines(self.last_fit, addr_new)
                self.clear_screen()
                self.progress_bar.update(
                    self.last_updated_addr - int(addr.split(",")[0])
                )
                self.last_updated_addr = int(addr.split(",")[0])
                print(
                    f'[concat of {working_indx+1} {"statement" if (working_indx+1)==1 else "statements"} removed, location:{addr}]\n'
                )
                print(
                    f"prev_removed:{self.prev_remmed}",
                    f"Down_traversal_activated: {self.back_max==self.current_back}",
                )
                for i in range(working_indx + 1):
                    try:
                        self.stored_addr.remove(queue[i])
                    except:
                        pass
            else:
                self.stored_addr = self.stored_addr + queue[:1]
            indx_results_prev = np.where(results_prev)[0]
            if len(indx_results_prev) != 0:
                index = indx_results_prev[-1]
                addr = batch_prev[index]
                addr_new = addr.split(",")
                addr_new = [int(i) for i in addr_new]
                self.last_fit = remove_lines(self.last_fit, addr_new)
                print(f"[prev {index+1} statements removed]")
                self.prev_remmed += index + 1
                for i in range(index + 1):
                    try:
                        self.stored_addr.remove(queue_prev[i])
                    except:
                        pass
            elif len(queue_prev) != 0 and self.current_back != 0:
                self.stored_addr = self.stored_addr[1:]
            if working_indx != -1:
                loop_itr = queue[working_indx][1] + 1
            else:
                loop_itr = queue[0][1] + 1
                if nodes[loop_itr - 1].startswith("cont"):
                    loop_itr -= 1
            if loop_itr == len(maps):
                if nodes[0] == "bounds":
                    if self.reduce((maps["bounds"], "1", True)):
                        to_change = self.last_fit.copy()
                        for add in maps["bounds"]:
                            addr_new = add.split(",")
                            addr_new = [int(i) for i in addr_new]
                            to_change = remove_lines(to_change, addr_new)
                        self.last_fit = to_change
                        print("bounds removed: ", maps["bounds"])
                break
