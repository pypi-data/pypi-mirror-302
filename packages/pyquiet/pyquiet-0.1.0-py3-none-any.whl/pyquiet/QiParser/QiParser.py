from typing import List
from pathlib import Path
from antlr4 import InputStream, CommonTokenStream
from pyquiet.antlr import QuietLexer, QuietParser
from pyquiet.QiVisitor.QuietVisitor import QuietVisitor
from pyquiet.qir.qi_prog import QiProgram
from pyquiet.qir.qinstructions import FuncCall
from pyquiet.qir.qfile import File, FileSection

#Process the file path and convert it to Path format
def ensure_path(fn) -> Path:
    assert isinstance(fn, (str, Path))
    if isinstance(fn, str):
        fn = Path(fn).resolve()
    return fn

class QiParser:
    def __init__(self) -> None:
        # There are several QiPrograms per parsing.
        # self.__programs = List[QiProgram]
        # self.__final_prog: QiProgram = None
        # self.__input_files: List[InputStream]
        # self.__visitor = QuietVisitor()
        pass

    def parse(self, filename):
        input = ""
        with open(filename, "r") as f:
            input = f.read()
        input2 = InputStream(input)
        lexer = QuietLexer(input2)
        tokens = CommonTokenStream(lexer)
        # get the CST.
        parser = QuietParser(tokens)
        quiet_cst = parser.prog()
        # convert the CST into QiProg
        visitor = QuietVisitor(qi_path=Path(filename).resolve().parent)
        prog = QiProgram(filename)
        # Before visiting the entire quiet_cst, we need to load the files included in the file section first.
        if quiet_cst.fileSection() is not None:
            qifile: FileSection = visitor.visitFileSection(quiet_cst.fileSection())
            for file in qifile.included_files:
                program_inc: QiProgram = self.parse(file.address)
                for module in program_inc.module_set.modules:
                    prog.module_set.import_module(module)
                for gate_cfg in program_inc.gate_section.dict.values():
                    prog.add_define_gate(gate_cfg)
                for func in program_inc.code_section.functions:
                    if func.name == "measure" or func.name == "reset":
                        continue
                    try:
                        prog.code_section.get_func(func.name)
                    except ValueError:
                        prog.add_define_function(func)
                    else:
                        raise ValueError(f"The function {func.name} has been defined yet.")
        # After loading the files, we can visit the quiet_cst.
        visitor.loadProg(prog)
        prog = visitor.visit(quiet_cst)
        # for func in prog.code_section.functions:
        #     for insn in func.body:
        #         if isinstance(insn, FuncCall):
        #             insn.bind_function(prog.code_section.get_func(insn.opname))
        return prog
