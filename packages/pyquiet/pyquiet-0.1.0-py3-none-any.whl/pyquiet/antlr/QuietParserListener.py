# Generated from QuietParser.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .QuietParser import QuietParser
else:
    from QuietParser import QuietParser

# This class defines a complete listener for a parse tree produced by QuietParser.
class QuietParserListener(ParseTreeListener):

    # Enter a parse tree produced by QuietParser#prog.
    def enterProg(self, ctx:QuietParser.ProgContext):
        pass

    # Exit a parse tree produced by QuietParser#prog.
    def exitProg(self, ctx:QuietParser.ProgContext):
        pass


    # Enter a parse tree produced by QuietParser#usingModule.
    def enterUsingModule(self, ctx:QuietParser.UsingModuleContext):
        pass

    # Exit a parse tree produced by QuietParser#usingModule.
    def exitUsingModule(self, ctx:QuietParser.UsingModuleContext):
        pass


    # Enter a parse tree produced by QuietParser#fileSection.
    def enterFileSection(self, ctx:QuietParser.FileSectionContext):
        pass

    # Exit a parse tree produced by QuietParser#fileSection.
    def exitFileSection(self, ctx:QuietParser.FileSectionContext):
        pass


    # Enter a parse tree produced by QuietParser#fileSecDecl.
    def enterFileSecDecl(self, ctx:QuietParser.FileSecDeclContext):
        pass

    # Exit a parse tree produced by QuietParser#fileSecDecl.
    def exitFileSecDecl(self, ctx:QuietParser.FileSecDeclContext):
        pass


    # Enter a parse tree produced by QuietParser#fileSecContent.
    def enterFileSecContent(self, ctx:QuietParser.FileSecContentContext):
        pass

    # Exit a parse tree produced by QuietParser#fileSecContent.
    def exitFileSecContent(self, ctx:QuietParser.FileSecContentContext):
        pass


    # Enter a parse tree produced by QuietParser#includeContent.
    def enterIncludeContent(self, ctx:QuietParser.IncludeContentContext):
        pass

    # Exit a parse tree produced by QuietParser#includeContent.
    def exitIncludeContent(self, ctx:QuietParser.IncludeContentContext):
        pass


    # Enter a parse tree produced by QuietParser#gateSection.
    def enterGateSection(self, ctx:QuietParser.GateSectionContext):
        pass

    # Exit a parse tree produced by QuietParser#gateSection.
    def exitGateSection(self, ctx:QuietParser.GateSectionContext):
        pass


    # Enter a parse tree produced by QuietParser#gateSecDecl.
    def enterGateSecDecl(self, ctx:QuietParser.GateSecDeclContext):
        pass

    # Exit a parse tree produced by QuietParser#gateSecDecl.
    def exitGateSecDecl(self, ctx:QuietParser.GateSecDeclContext):
        pass


    # Enter a parse tree produced by QuietParser#gateSecContent.
    def enterGateSecContent(self, ctx:QuietParser.GateSecContentContext):
        pass

    # Exit a parse tree produced by QuietParser#gateSecContent.
    def exitGateSecContent(self, ctx:QuietParser.GateSecContentContext):
        pass


    # Enter a parse tree produced by QuietParser#gateDefinition.
    def enterGateDefinition(self, ctx:QuietParser.GateDefinitionContext):
        pass

    # Exit a parse tree produced by QuietParser#gateDefinition.
    def exitGateDefinition(self, ctx:QuietParser.GateDefinitionContext):
        pass


    # Enter a parse tree produced by QuietParser#numberArray.
    def enterNumberArray(self, ctx:QuietParser.NumberArrayContext):
        pass

    # Exit a parse tree produced by QuietParser#numberArray.
    def exitNumberArray(self, ctx:QuietParser.NumberArrayContext):
        pass


    # Enter a parse tree produced by QuietParser#numberList.
    def enterNumberList(self, ctx:QuietParser.NumberListContext):
        pass

    # Exit a parse tree produced by QuietParser#numberList.
    def exitNumberList(self, ctx:QuietParser.NumberListContext):
        pass


    # Enter a parse tree produced by QuietParser#pulseSection.
    def enterPulseSection(self, ctx:QuietParser.PulseSectionContext):
        pass

    # Exit a parse tree produced by QuietParser#pulseSection.
    def exitPulseSection(self, ctx:QuietParser.PulseSectionContext):
        pass


    # Enter a parse tree produced by QuietParser#pulseSecDecl.
    def enterPulseSecDecl(self, ctx:QuietParser.PulseSecDeclContext):
        pass

    # Exit a parse tree produced by QuietParser#pulseSecDecl.
    def exitPulseSecDecl(self, ctx:QuietParser.PulseSecDeclContext):
        pass


    # Enter a parse tree produced by QuietParser#pulseSecContent.
    def enterPulseSecContent(self, ctx:QuietParser.PulseSecContentContext):
        pass

    # Exit a parse tree produced by QuietParser#pulseSecContent.
    def exitPulseSecContent(self, ctx:QuietParser.PulseSecContentContext):
        pass


    # Enter a parse tree produced by QuietParser#customWave.
    def enterCustomWave(self, ctx:QuietParser.CustomWaveContext):
        pass

    # Exit a parse tree produced by QuietParser#customWave.
    def exitCustomWave(self, ctx:QuietParser.CustomWaveContext):
        pass


    # Enter a parse tree produced by QuietParser#waveFunction.
    def enterWaveFunction(self, ctx:QuietParser.WaveFunctionContext):
        pass

    # Exit a parse tree produced by QuietParser#waveFunction.
    def exitWaveFunction(self, ctx:QuietParser.WaveFunctionContext):
        pass


    # Enter a parse tree produced by QuietParser#waveFuncHeader.
    def enterWaveFuncHeader(self, ctx:QuietParser.WaveFuncHeaderContext):
        pass

    # Exit a parse tree produced by QuietParser#waveFuncHeader.
    def exitWaveFuncHeader(self, ctx:QuietParser.WaveFuncHeaderContext):
        pass


    # Enter a parse tree produced by QuietParser#waveFuncBody.
    def enterWaveFuncBody(self, ctx:QuietParser.WaveFuncBodyContext):
        pass

    # Exit a parse tree produced by QuietParser#waveFuncBody.
    def exitWaveFuncBody(self, ctx:QuietParser.WaveFuncBodyContext):
        pass


    # Enter a parse tree produced by QuietParser#waveInsn.
    def enterWaveInsn(self, ctx:QuietParser.WaveInsnContext):
        pass

    # Exit a parse tree produced by QuietParser#waveInsn.
    def exitWaveInsn(self, ctx:QuietParser.WaveInsnContext):
        pass


    # Enter a parse tree produced by QuietParser#codeSection.
    def enterCodeSection(self, ctx:QuietParser.CodeSectionContext):
        pass

    # Exit a parse tree produced by QuietParser#codeSection.
    def exitCodeSection(self, ctx:QuietParser.CodeSectionContext):
        pass


    # Enter a parse tree produced by QuietParser#codeSecDecl.
    def enterCodeSecDecl(self, ctx:QuietParser.CodeSecDeclContext):
        pass

    # Exit a parse tree produced by QuietParser#codeSecDecl.
    def exitCodeSecDecl(self, ctx:QuietParser.CodeSecDeclContext):
        pass


    # Enter a parse tree produced by QuietParser#codeSecContent.
    def enterCodeSecContent(self, ctx:QuietParser.CodeSecContentContext):
        pass

    # Exit a parse tree produced by QuietParser#codeSecContent.
    def exitCodeSecContent(self, ctx:QuietParser.CodeSecContentContext):
        pass


    # Enter a parse tree produced by QuietParser#entrySection.
    def enterEntrySection(self, ctx:QuietParser.EntrySectionContext):
        pass

    # Exit a parse tree produced by QuietParser#entrySection.
    def exitEntrySection(self, ctx:QuietParser.EntrySectionContext):
        pass


    # Enter a parse tree produced by QuietParser#entrySecDecl.
    def enterEntrySecDecl(self, ctx:QuietParser.EntrySecDeclContext):
        pass

    # Exit a parse tree produced by QuietParser#entrySecDecl.
    def exitEntrySecDecl(self, ctx:QuietParser.EntrySecDeclContext):
        pass


    # Enter a parse tree produced by QuietParser#entrySecContent.
    def enterEntrySecContent(self, ctx:QuietParser.EntrySecContentContext):
        pass

    # Exit a parse tree produced by QuietParser#entrySecContent.
    def exitEntrySecContent(self, ctx:QuietParser.EntrySecContentContext):
        pass


    # Enter a parse tree produced by QuietParser#layoutSection.
    def enterLayoutSection(self, ctx:QuietParser.LayoutSectionContext):
        pass

    # Exit a parse tree produced by QuietParser#layoutSection.
    def exitLayoutSection(self, ctx:QuietParser.LayoutSectionContext):
        pass


    # Enter a parse tree produced by QuietParser#layoutSecDecl.
    def enterLayoutSecDecl(self, ctx:QuietParser.LayoutSecDeclContext):
        pass

    # Exit a parse tree produced by QuietParser#layoutSecDecl.
    def exitLayoutSecDecl(self, ctx:QuietParser.LayoutSecDeclContext):
        pass


    # Enter a parse tree produced by QuietParser#layoutSecContent.
    def enterLayoutSecContent(self, ctx:QuietParser.LayoutSecContentContext):
        pass

    # Exit a parse tree produced by QuietParser#layoutSecContent.
    def exitLayoutSecContent(self, ctx:QuietParser.LayoutSecContentContext):
        pass


    # Enter a parse tree produced by QuietParser#portDecl.
    def enterPortDecl(self, ctx:QuietParser.PortDeclContext):
        pass

    # Exit a parse tree produced by QuietParser#portDecl.
    def exitPortDecl(self, ctx:QuietParser.PortDeclContext):
        pass


    # Enter a parse tree produced by QuietParser#subPortList.
    def enterSubPortList(self, ctx:QuietParser.SubPortListContext):
        pass

    # Exit a parse tree produced by QuietParser#subPortList.
    def exitSubPortList(self, ctx:QuietParser.SubPortListContext):
        pass


    # Enter a parse tree produced by QuietParser#subPort.
    def enterSubPort(self, ctx:QuietParser.SubPortContext):
        pass

    # Exit a parse tree produced by QuietParser#subPort.
    def exitSubPort(self, ctx:QuietParser.SubPortContext):
        pass


    # Enter a parse tree produced by QuietParser#phySubPort.
    def enterPhySubPort(self, ctx:QuietParser.PhySubPortContext):
        pass

    # Exit a parse tree produced by QuietParser#phySubPort.
    def exitPhySubPort(self, ctx:QuietParser.PhySubPortContext):
        pass


    # Enter a parse tree produced by QuietParser#lgcSubPort.
    def enterLgcSubPort(self, ctx:QuietParser.LgcSubPortContext):
        pass

    # Exit a parse tree produced by QuietParser#lgcSubPort.
    def exitLgcSubPort(self, ctx:QuietParser.LgcSubPortContext):
        pass


    # Enter a parse tree produced by QuietParser#portAlias.
    def enterPortAlias(self, ctx:QuietParser.PortAliasContext):
        pass

    # Exit a parse tree produced by QuietParser#portAlias.
    def exitPortAlias(self, ctx:QuietParser.PortAliasContext):
        pass


    # Enter a parse tree produced by QuietParser#bindPort.
    def enterBindPort(self, ctx:QuietParser.BindPortContext):
        pass

    # Exit a parse tree produced by QuietParser#bindPort.
    def exitBindPort(self, ctx:QuietParser.BindPortContext):
        pass


    # Enter a parse tree produced by QuietParser#function.
    def enterFunction(self, ctx:QuietParser.FunctionContext):
        pass

    # Exit a parse tree produced by QuietParser#function.
    def exitFunction(self, ctx:QuietParser.FunctionContext):
        pass


    # Enter a parse tree produced by QuietParser#funcHeader.
    def enterFuncHeader(self, ctx:QuietParser.FuncHeaderContext):
        pass

    # Exit a parse tree produced by QuietParser#funcHeader.
    def exitFuncHeader(self, ctx:QuietParser.FuncHeaderContext):
        pass


    # Enter a parse tree produced by QuietParser#inputArgs.
    def enterInputArgs(self, ctx:QuietParser.InputArgsContext):
        pass

    # Exit a parse tree produced by QuietParser#inputArgs.
    def exitInputArgs(self, ctx:QuietParser.InputArgsContext):
        pass


    # Enter a parse tree produced by QuietParser#outputArgs.
    def enterOutputArgs(self, ctx:QuietParser.OutputArgsContext):
        pass

    # Exit a parse tree produced by QuietParser#outputArgs.
    def exitOutputArgs(self, ctx:QuietParser.OutputArgsContext):
        pass


    # Enter a parse tree produced by QuietParser#formalVariable.
    def enterFormalVariable(self, ctx:QuietParser.FormalVariableContext):
        pass

    # Exit a parse tree produced by QuietParser#formalVariable.
    def exitFormalVariable(self, ctx:QuietParser.FormalVariableContext):
        pass


    # Enter a parse tree produced by QuietParser#funcBody.
    def enterFuncBody(self, ctx:QuietParser.FuncBodyContext):
        pass

    # Exit a parse tree produced by QuietParser#funcBody.
    def exitFuncBody(self, ctx:QuietParser.FuncBodyContext):
        pass


    # Enter a parse tree produced by QuietParser#insnWithLabel.
    def enterInsnWithLabel(self, ctx:QuietParser.InsnWithLabelContext):
        pass

    # Exit a parse tree produced by QuietParser#insnWithLabel.
    def exitInsnWithLabel(self, ctx:QuietParser.InsnWithLabelContext):
        pass


    # Enter a parse tree produced by QuietParser#label.
    def enterLabel(self, ctx:QuietParser.LabelContext):
        pass

    # Exit a parse tree produced by QuietParser#label.
    def exitLabel(self, ctx:QuietParser.LabelContext):
        pass


    # Enter a parse tree produced by QuietParser#instruction.
    def enterInstruction(self, ctx:QuietParser.InstructionContext):
        pass

    # Exit a parse tree produced by QuietParser#instruction.
    def exitInstruction(self, ctx:QuietParser.InstructionContext):
        pass


    # Enter a parse tree produced by QuietParser#variableDecl.
    def enterVariableDecl(self, ctx:QuietParser.VariableDeclContext):
        pass

    # Exit a parse tree produced by QuietParser#variableDecl.
    def exitVariableDecl(self, ctx:QuietParser.VariableDeclContext):
        pass


    # Enter a parse tree produced by QuietParser#callFunc.
    def enterCallFunc(self, ctx:QuietParser.CallFuncContext):
        pass

    # Exit a parse tree produced by QuietParser#callFunc.
    def exitCallFunc(self, ctx:QuietParser.CallFuncContext):
        pass


    # Enter a parse tree produced by QuietParser#actualPara.
    def enterActualPara(self, ctx:QuietParser.ActualParaContext):
        pass

    # Exit a parse tree produced by QuietParser#actualPara.
    def exitActualPara(self, ctx:QuietParser.ActualParaContext):
        pass


    # Enter a parse tree produced by QuietParser#actualParaList.
    def enterActualParaList(self, ctx:QuietParser.ActualParaListContext):
        pass

    # Exit a parse tree produced by QuietParser#actualParaList.
    def exitActualParaList(self, ctx:QuietParser.ActualParaListContext):
        pass


    # Enter a parse tree produced by QuietParser#actualVariableList.
    def enterActualVariableList(self, ctx:QuietParser.ActualVariableListContext):
        pass

    # Exit a parse tree produced by QuietParser#actualVariableList.
    def exitActualVariableList(self, ctx:QuietParser.ActualVariableListContext):
        pass


    # Enter a parse tree produced by QuietParser#controlQubit.
    def enterControlQubit(self, ctx:QuietParser.ControlQubitContext):
        pass

    # Exit a parse tree produced by QuietParser#controlQubit.
    def exitControlQubit(self, ctx:QuietParser.ControlQubitContext):
        pass


    # Enter a parse tree produced by QuietParser#quantumOpIns.
    def enterQuantumOpIns(self, ctx:QuietParser.QuantumOpInsContext):
        pass

    # Exit a parse tree produced by QuietParser#quantumOpIns.
    def exitQuantumOpIns(self, ctx:QuietParser.QuantumOpInsContext):
        pass


    # Enter a parse tree produced by QuietParser#moduleCtIns.
    def enterModuleCtIns(self, ctx:QuietParser.ModuleCtInsContext):
        pass

    # Exit a parse tree produced by QuietParser#moduleCtIns.
    def exitModuleCtIns(self, ctx:QuietParser.ModuleCtInsContext):
        pass


    # Enter a parse tree produced by QuietParser#moduleFmIns.
    def enterModuleFmIns(self, ctx:QuietParser.ModuleFmInsContext):
        pass

    # Exit a parse tree produced by QuietParser#moduleFmIns.
    def exitModuleFmIns(self, ctx:QuietParser.ModuleFmInsContext):
        pass


    # Enter a parse tree produced by QuietParser#dataTransFmIns.
    def enterDataTransFmIns(self, ctx:QuietParser.DataTransFmInsContext):
        pass

    # Exit a parse tree produced by QuietParser#dataTransFmIns.
    def exitDataTransFmIns(self, ctx:QuietParser.DataTransFmInsContext):
        pass


    # Enter a parse tree produced by QuietParser#mathOpFmIns.
    def enterMathOpFmIns(self, ctx:QuietParser.MathOpFmInsContext):
        pass

    # Exit a parse tree produced by QuietParser#mathOpFmIns.
    def exitMathOpFmIns(self, ctx:QuietParser.MathOpFmInsContext):
        pass


    # Enter a parse tree produced by QuietParser#typeConvFmIns.
    def enterTypeConvFmIns(self, ctx:QuietParser.TypeConvFmInsContext):
        pass

    # Exit a parse tree produced by QuietParser#typeConvFmIns.
    def exitTypeConvFmIns(self, ctx:QuietParser.TypeConvFmInsContext):
        pass


    # Enter a parse tree produced by QuietParser#moduleImIns.
    def enterModuleImIns(self, ctx:QuietParser.ModuleImInsContext):
        pass

    # Exit a parse tree produced by QuietParser#moduleImIns.
    def exitModuleImIns(self, ctx:QuietParser.ModuleImInsContext):
        pass


    # Enter a parse tree produced by QuietParser#dataTransImIns.
    def enterDataTransImIns(self, ctx:QuietParser.DataTransImInsContext):
        pass

    # Exit a parse tree produced by QuietParser#dataTransImIns.
    def exitDataTransImIns(self, ctx:QuietParser.DataTransImInsContext):
        pass


    # Enter a parse tree produced by QuietParser#logicOpImIns.
    def enterLogicOpImIns(self, ctx:QuietParser.LogicOpImInsContext):
        pass

    # Exit a parse tree produced by QuietParser#logicOpImIns.
    def exitLogicOpImIns(self, ctx:QuietParser.LogicOpImInsContext):
        pass


    # Enter a parse tree produced by QuietParser#mathOpImIns.
    def enterMathOpImIns(self, ctx:QuietParser.MathOpImInsContext):
        pass

    # Exit a parse tree produced by QuietParser#mathOpImIns.
    def exitMathOpImIns(self, ctx:QuietParser.MathOpImInsContext):
        pass


    # Enter a parse tree produced by QuietParser#moduleStdIns.
    def enterModuleStdIns(self, ctx:QuietParser.ModuleStdInsContext):
        pass

    # Exit a parse tree produced by QuietParser#moduleStdIns.
    def exitModuleStdIns(self, ctx:QuietParser.ModuleStdInsContext):
        pass


    # Enter a parse tree produced by QuietParser#noParaOpIns.
    def enterNoParaOpIns(self, ctx:QuietParser.NoParaOpInsContext):
        pass

    # Exit a parse tree produced by QuietParser#noParaOpIns.
    def exitNoParaOpIns(self, ctx:QuietParser.NoParaOpInsContext):
        pass


    # Enter a parse tree produced by QuietParser#paraOpIns.
    def enterParaOpIns(self, ctx:QuietParser.ParaOpInsContext):
        pass

    # Exit a parse tree produced by QuietParser#paraOpIns.
    def exitParaOpIns(self, ctx:QuietParser.ParaOpInsContext):
        pass


    # Enter a parse tree produced by QuietParser#theta.
    def enterTheta(self, ctx:QuietParser.ThetaContext):
        pass

    # Exit a parse tree produced by QuietParser#theta.
    def exitTheta(self, ctx:QuietParser.ThetaContext):
        pass


    # Enter a parse tree produced by QuietParser#modulePmIns.
    def enterModulePmIns(self, ctx:QuietParser.ModulePmInsContext):
        pass

    # Exit a parse tree produced by QuietParser#modulePmIns.
    def exitModulePmIns(self, ctx:QuietParser.ModulePmInsContext):
        pass


    # Enter a parse tree produced by QuietParser#waveFormIns.
    def enterWaveFormIns(self, ctx:QuietParser.WaveFormInsContext):
        pass

    # Exit a parse tree produced by QuietParser#waveFormIns.
    def exitWaveFormIns(self, ctx:QuietParser.WaveFormInsContext):
        pass


    # Enter a parse tree produced by QuietParser#customWaveFormIns.
    def enterCustomWaveFormIns(self, ctx:QuietParser.CustomWaveFormInsContext):
        pass

    # Exit a parse tree produced by QuietParser#customWaveFormIns.
    def exitCustomWaveFormIns(self, ctx:QuietParser.CustomWaveFormInsContext):
        pass


    # Enter a parse tree produced by QuietParser#defWaveFormIns.
    def enterDefWaveFormIns(self, ctx:QuietParser.DefWaveFormInsContext):
        pass

    # Exit a parse tree produced by QuietParser#defWaveFormIns.
    def exitDefWaveFormIns(self, ctx:QuietParser.DefWaveFormInsContext):
        pass


    # Enter a parse tree produced by QuietParser#defWaveInput.
    def enterDefWaveInput(self, ctx:QuietParser.DefWaveInputContext):
        pass

    # Exit a parse tree produced by QuietParser#defWaveInput.
    def exitDefWaveInput(self, ctx:QuietParser.DefWaveInputContext):
        pass


    # Enter a parse tree produced by QuietParser#waveOpIns.
    def enterWaveOpIns(self, ctx:QuietParser.WaveOpInsContext):
        pass

    # Exit a parse tree produced by QuietParser#waveOpIns.
    def exitWaveOpIns(self, ctx:QuietParser.WaveOpInsContext):
        pass


    # Enter a parse tree produced by QuietParser#portCfgIns.
    def enterPortCfgIns(self, ctx:QuietParser.PortCfgInsContext):
        pass

    # Exit a parse tree produced by QuietParser#portCfgIns.
    def exitPortCfgIns(self, ctx:QuietParser.PortCfgInsContext):
        pass


    # Enter a parse tree produced by QuietParser#wavePlayIns.
    def enterWavePlayIns(self, ctx:QuietParser.WavePlayInsContext):
        pass

    # Exit a parse tree produced by QuietParser#wavePlayIns.
    def exitWavePlayIns(self, ctx:QuietParser.WavePlayInsContext):
        pass


    # Enter a parse tree produced by QuietParser#signalCapIns.
    def enterSignalCapIns(self, ctx:QuietParser.SignalCapInsContext):
        pass

    # Exit a parse tree produced by QuietParser#signalCapIns.
    def exitSignalCapIns(self, ctx:QuietParser.SignalCapInsContext):
        pass


    # Enter a parse tree produced by QuietParser#pmFloatPara.
    def enterPmFloatPara(self, ctx:QuietParser.PmFloatParaContext):
        pass

    # Exit a parse tree produced by QuietParser#pmFloatPara.
    def exitPmFloatPara(self, ctx:QuietParser.PmFloatParaContext):
        pass


    # Enter a parse tree produced by QuietParser#pmTimePara.
    def enterPmTimePara(self, ctx:QuietParser.PmTimeParaContext):
        pass

    # Exit a parse tree produced by QuietParser#pmTimePara.
    def exitPmTimePara(self, ctx:QuietParser.PmTimeParaContext):
        pass


    # Enter a parse tree produced by QuietParser#moduleTmIns.
    def enterModuleTmIns(self, ctx:QuietParser.ModuleTmInsContext):
        pass

    # Exit a parse tree produced by QuietParser#moduleTmIns.
    def exitModuleTmIns(self, ctx:QuietParser.ModuleTmInsContext):
        pass


    # Enter a parse tree produced by QuietParser#dataTransTmIns.
    def enterDataTransTmIns(self, ctx:QuietParser.DataTransTmInsContext):
        pass

    # Exit a parse tree produced by QuietParser#dataTransTmIns.
    def exitDataTransTmIns(self, ctx:QuietParser.DataTransTmInsContext):
        pass


    # Enter a parse tree produced by QuietParser#mathOpTmIns.
    def enterMathOpTmIns(self, ctx:QuietParser.MathOpTmInsContext):
        pass

    # Exit a parse tree produced by QuietParser#mathOpTmIns.
    def exitMathOpTmIns(self, ctx:QuietParser.MathOpTmInsContext):
        pass


    # Enter a parse tree produced by QuietParser#waitOpTmIns.
    def enterWaitOpTmIns(self, ctx:QuietParser.WaitOpTmInsContext):
        pass

    # Exit a parse tree produced by QuietParser#waitOpTmIns.
    def exitWaitOpTmIns(self, ctx:QuietParser.WaitOpTmInsContext):
        pass


    # Enter a parse tree produced by QuietParser#syncOpTmIns.
    def enterSyncOpTmIns(self, ctx:QuietParser.SyncOpTmInsContext):
        pass

    # Exit a parse tree produced by QuietParser#syncOpTmIns.
    def exitSyncOpTmIns(self, ctx:QuietParser.SyncOpTmInsContext):
        pass


    # Enter a parse tree produced by QuietParser#number.
    def enterNumber(self, ctx:QuietParser.NumberContext):
        pass

    # Exit a parse tree produced by QuietParser#number.
    def exitNumber(self, ctx:QuietParser.NumberContext):
        pass


    # Enter a parse tree produced by QuietParser#complexLiteral.
    def enterComplexLiteral(self, ctx:QuietParser.ComplexLiteralContext):
        pass

    # Exit a parse tree produced by QuietParser#complexLiteral.
    def exitComplexLiteral(self, ctx:QuietParser.ComplexLiteralContext):
        pass


    # Enter a parse tree produced by QuietParser#realPart.
    def enterRealPart(self, ctx:QuietParser.RealPartContext):
        pass

    # Exit a parse tree produced by QuietParser#realPart.
    def exitRealPart(self, ctx:QuietParser.RealPartContext):
        pass


    # Enter a parse tree produced by QuietParser#imaginaryPart.
    def enterImaginaryPart(self, ctx:QuietParser.ImaginaryPartContext):
        pass

    # Exit a parse tree produced by QuietParser#imaginaryPart.
    def exitImaginaryPart(self, ctx:QuietParser.ImaginaryPartContext):
        pass


    # Enter a parse tree produced by QuietParser#timeLiteral.
    def enterTimeLiteral(self, ctx:QuietParser.TimeLiteralContext):
        pass

    # Exit a parse tree produced by QuietParser#timeLiteral.
    def exitTimeLiteral(self, ctx:QuietParser.TimeLiteralContext):
        pass


    # Enter a parse tree produced by QuietParser#portLiteral.
    def enterPortLiteral(self, ctx:QuietParser.PortLiteralContext):
        pass

    # Exit a parse tree produced by QuietParser#portLiteral.
    def exitPortLiteral(self, ctx:QuietParser.PortLiteralContext):
        pass


    # Enter a parse tree produced by QuietParser#phyPort.
    def enterPhyPort(self, ctx:QuietParser.PhyPortContext):
        pass

    # Exit a parse tree produced by QuietParser#phyPort.
    def exitPhyPort(self, ctx:QuietParser.PhyPortContext):
        pass


    # Enter a parse tree produced by QuietParser#lgcPort.
    def enterLgcPort(self, ctx:QuietParser.LgcPortContext):
        pass

    # Exit a parse tree produced by QuietParser#lgcPort.
    def exitLgcPort(self, ctx:QuietParser.LgcPortContext):
        pass


    # Enter a parse tree produced by QuietParser#string.
    def enterString(self, ctx:QuietParser.StringContext):
        pass

    # Exit a parse tree produced by QuietParser#string.
    def exitString(self, ctx:QuietParser.StringContext):
        pass


    # Enter a parse tree produced by QuietParser#variableType.
    def enterVariableType(self, ctx:QuietParser.VariableTypeContext):
        pass

    # Exit a parse tree produced by QuietParser#variableType.
    def exitVariableType(self, ctx:QuietParser.VariableTypeContext):
        pass


    # Enter a parse tree produced by QuietParser#ordinaryType.
    def enterOrdinaryType(self, ctx:QuietParser.OrdinaryTypeContext):
        pass

    # Exit a parse tree produced by QuietParser#ordinaryType.
    def exitOrdinaryType(self, ctx:QuietParser.OrdinaryTypeContext):
        pass


    # Enter a parse tree produced by QuietParser#withLengthArrayType.
    def enterWithLengthArrayType(self, ctx:QuietParser.WithLengthArrayTypeContext):
        pass

    # Exit a parse tree produced by QuietParser#withLengthArrayType.
    def exitWithLengthArrayType(self, ctx:QuietParser.WithLengthArrayTypeContext):
        pass


    # Enter a parse tree produced by QuietParser#noLengthArrayType.
    def enterNoLengthArrayType(self, ctx:QuietParser.NoLengthArrayTypeContext):
        pass

    # Exit a parse tree produced by QuietParser#noLengthArrayType.
    def exitNoLengthArrayType(self, ctx:QuietParser.NoLengthArrayTypeContext):
        pass


    # Enter a parse tree produced by QuietParser#variable.
    def enterVariable(self, ctx:QuietParser.VariableContext):
        pass

    # Exit a parse tree produced by QuietParser#variable.
    def exitVariable(self, ctx:QuietParser.VariableContext):
        pass


    # Enter a parse tree produced by QuietParser#phyQubit.
    def enterPhyQubit(self, ctx:QuietParser.PhyQubitContext):
        pass

    # Exit a parse tree produced by QuietParser#phyQubit.
    def exitPhyQubit(self, ctx:QuietParser.PhyQubitContext):
        pass



del QuietParser