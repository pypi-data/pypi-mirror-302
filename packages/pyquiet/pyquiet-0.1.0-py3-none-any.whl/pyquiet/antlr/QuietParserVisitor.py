# Generated from QuietParser.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .QuietParser import QuietParser
else:
    from QuietParser import QuietParser

# This class defines a complete generic visitor for a parse tree produced by QuietParser.

class QuietParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by QuietParser#prog.
    def visitProg(self, ctx:QuietParser.ProgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#usingModule.
    def visitUsingModule(self, ctx:QuietParser.UsingModuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#fileSection.
    def visitFileSection(self, ctx:QuietParser.FileSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#fileSecDecl.
    def visitFileSecDecl(self, ctx:QuietParser.FileSecDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#fileSecContent.
    def visitFileSecContent(self, ctx:QuietParser.FileSecContentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#includeContent.
    def visitIncludeContent(self, ctx:QuietParser.IncludeContentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#gateSection.
    def visitGateSection(self, ctx:QuietParser.GateSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#gateSecDecl.
    def visitGateSecDecl(self, ctx:QuietParser.GateSecDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#gateSecContent.
    def visitGateSecContent(self, ctx:QuietParser.GateSecContentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#gateDefinition.
    def visitGateDefinition(self, ctx:QuietParser.GateDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#numberArray.
    def visitNumberArray(self, ctx:QuietParser.NumberArrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#numberList.
    def visitNumberList(self, ctx:QuietParser.NumberListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#pulseSection.
    def visitPulseSection(self, ctx:QuietParser.PulseSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#pulseSecDecl.
    def visitPulseSecDecl(self, ctx:QuietParser.PulseSecDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#pulseSecContent.
    def visitPulseSecContent(self, ctx:QuietParser.PulseSecContentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#customWave.
    def visitCustomWave(self, ctx:QuietParser.CustomWaveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#waveFunction.
    def visitWaveFunction(self, ctx:QuietParser.WaveFunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#waveFuncHeader.
    def visitWaveFuncHeader(self, ctx:QuietParser.WaveFuncHeaderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#waveFuncBody.
    def visitWaveFuncBody(self, ctx:QuietParser.WaveFuncBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#waveInsn.
    def visitWaveInsn(self, ctx:QuietParser.WaveInsnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#codeSection.
    def visitCodeSection(self, ctx:QuietParser.CodeSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#codeSecDecl.
    def visitCodeSecDecl(self, ctx:QuietParser.CodeSecDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#codeSecContent.
    def visitCodeSecContent(self, ctx:QuietParser.CodeSecContentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#entrySection.
    def visitEntrySection(self, ctx:QuietParser.EntrySectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#entrySecDecl.
    def visitEntrySecDecl(self, ctx:QuietParser.EntrySecDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#entrySecContent.
    def visitEntrySecContent(self, ctx:QuietParser.EntrySecContentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#layoutSection.
    def visitLayoutSection(self, ctx:QuietParser.LayoutSectionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#layoutSecDecl.
    def visitLayoutSecDecl(self, ctx:QuietParser.LayoutSecDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#layoutSecContent.
    def visitLayoutSecContent(self, ctx:QuietParser.LayoutSecContentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#portDecl.
    def visitPortDecl(self, ctx:QuietParser.PortDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#subPortList.
    def visitSubPortList(self, ctx:QuietParser.SubPortListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#subPort.
    def visitSubPort(self, ctx:QuietParser.SubPortContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#phySubPort.
    def visitPhySubPort(self, ctx:QuietParser.PhySubPortContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#lgcSubPort.
    def visitLgcSubPort(self, ctx:QuietParser.LgcSubPortContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#portAlias.
    def visitPortAlias(self, ctx:QuietParser.PortAliasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#bindPort.
    def visitBindPort(self, ctx:QuietParser.BindPortContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#function.
    def visitFunction(self, ctx:QuietParser.FunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#funcHeader.
    def visitFuncHeader(self, ctx:QuietParser.FuncHeaderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#inputArgs.
    def visitInputArgs(self, ctx:QuietParser.InputArgsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#outputArgs.
    def visitOutputArgs(self, ctx:QuietParser.OutputArgsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#formalVariable.
    def visitFormalVariable(self, ctx:QuietParser.FormalVariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#funcBody.
    def visitFuncBody(self, ctx:QuietParser.FuncBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#insnWithLabel.
    def visitInsnWithLabel(self, ctx:QuietParser.InsnWithLabelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#label.
    def visitLabel(self, ctx:QuietParser.LabelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#instruction.
    def visitInstruction(self, ctx:QuietParser.InstructionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#variableDecl.
    def visitVariableDecl(self, ctx:QuietParser.VariableDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#callFunc.
    def visitCallFunc(self, ctx:QuietParser.CallFuncContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#actualPara.
    def visitActualPara(self, ctx:QuietParser.ActualParaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#actualParaList.
    def visitActualParaList(self, ctx:QuietParser.ActualParaListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#actualVariableList.
    def visitActualVariableList(self, ctx:QuietParser.ActualVariableListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#controlQubit.
    def visitControlQubit(self, ctx:QuietParser.ControlQubitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#quantumOpIns.
    def visitQuantumOpIns(self, ctx:QuietParser.QuantumOpInsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#moduleCtIns.
    def visitModuleCtIns(self, ctx:QuietParser.ModuleCtInsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#moduleFmIns.
    def visitModuleFmIns(self, ctx:QuietParser.ModuleFmInsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#dataTransFmIns.
    def visitDataTransFmIns(self, ctx:QuietParser.DataTransFmInsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#mathOpFmIns.
    def visitMathOpFmIns(self, ctx:QuietParser.MathOpFmInsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#typeConvFmIns.
    def visitTypeConvFmIns(self, ctx:QuietParser.TypeConvFmInsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#moduleImIns.
    def visitModuleImIns(self, ctx:QuietParser.ModuleImInsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#dataTransImIns.
    def visitDataTransImIns(self, ctx:QuietParser.DataTransImInsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#logicOpImIns.
    def visitLogicOpImIns(self, ctx:QuietParser.LogicOpImInsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#mathOpImIns.
    def visitMathOpImIns(self, ctx:QuietParser.MathOpImInsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#moduleStdIns.
    def visitModuleStdIns(self, ctx:QuietParser.ModuleStdInsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#noParaOpIns.
    def visitNoParaOpIns(self, ctx:QuietParser.NoParaOpInsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#paraOpIns.
    def visitParaOpIns(self, ctx:QuietParser.ParaOpInsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#theta.
    def visitTheta(self, ctx:QuietParser.ThetaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#modulePmIns.
    def visitModulePmIns(self, ctx:QuietParser.ModulePmInsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#waveFormIns.
    def visitWaveFormIns(self, ctx:QuietParser.WaveFormInsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#customWaveFormIns.
    def visitCustomWaveFormIns(self, ctx:QuietParser.CustomWaveFormInsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#defWaveFormIns.
    def visitDefWaveFormIns(self, ctx:QuietParser.DefWaveFormInsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#defWaveInput.
    def visitDefWaveInput(self, ctx:QuietParser.DefWaveInputContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#waveOpIns.
    def visitWaveOpIns(self, ctx:QuietParser.WaveOpInsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#portCfgIns.
    def visitPortCfgIns(self, ctx:QuietParser.PortCfgInsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#wavePlayIns.
    def visitWavePlayIns(self, ctx:QuietParser.WavePlayInsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#signalCapIns.
    def visitSignalCapIns(self, ctx:QuietParser.SignalCapInsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#pmFloatPara.
    def visitPmFloatPara(self, ctx:QuietParser.PmFloatParaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#pmTimePara.
    def visitPmTimePara(self, ctx:QuietParser.PmTimeParaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#moduleTmIns.
    def visitModuleTmIns(self, ctx:QuietParser.ModuleTmInsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#dataTransTmIns.
    def visitDataTransTmIns(self, ctx:QuietParser.DataTransTmInsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#mathOpTmIns.
    def visitMathOpTmIns(self, ctx:QuietParser.MathOpTmInsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#waitOpTmIns.
    def visitWaitOpTmIns(self, ctx:QuietParser.WaitOpTmInsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#syncOpTmIns.
    def visitSyncOpTmIns(self, ctx:QuietParser.SyncOpTmInsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#number.
    def visitNumber(self, ctx:QuietParser.NumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#complexLiteral.
    def visitComplexLiteral(self, ctx:QuietParser.ComplexLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#realPart.
    def visitRealPart(self, ctx:QuietParser.RealPartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#imaginaryPart.
    def visitImaginaryPart(self, ctx:QuietParser.ImaginaryPartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#timeLiteral.
    def visitTimeLiteral(self, ctx:QuietParser.TimeLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#portLiteral.
    def visitPortLiteral(self, ctx:QuietParser.PortLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#phyPort.
    def visitPhyPort(self, ctx:QuietParser.PhyPortContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#lgcPort.
    def visitLgcPort(self, ctx:QuietParser.LgcPortContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#string.
    def visitString(self, ctx:QuietParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#variableType.
    def visitVariableType(self, ctx:QuietParser.VariableTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#ordinaryType.
    def visitOrdinaryType(self, ctx:QuietParser.OrdinaryTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#withLengthArrayType.
    def visitWithLengthArrayType(self, ctx:QuietParser.WithLengthArrayTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#noLengthArrayType.
    def visitNoLengthArrayType(self, ctx:QuietParser.NoLengthArrayTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#variable.
    def visitVariable(self, ctx:QuietParser.VariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QuietParser#phyQubit.
    def visitPhyQubit(self, ctx:QuietParser.PhyQubitContext):
        return self.visitChildren(ctx)



del QuietParser