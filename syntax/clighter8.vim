hi default link clighter8Decl Identifier
hi default link clighter8Ref Type
hi default link clighter8Prepro PreProc
hi default link clighter8Stat Keyword
hi default link clighter8Expr Type

""" hi default link clighter8StructDecl Identifier
""" hi default link clighter8UnionDecl Identifier
""" hi default link clighter8ClassDecl Identifier
""" hi default link clighter8EnumDecl Identifier
""" hi default link clighter8FieldDecl Identifier
""" hi default link clighter8EnumConstantDecl Constant
""" hi default link clighter8FunctionDecl Identifier
""" hi default link clighter8VarDecl Identifier
""" hi default link clighter8ParmDecl Identifier
""" hi default link clighter8TypedefDecl Identifier
""" hi default link clighter8CxxMethod Identifier
""" hi default link clighter8Namespace Identifier
""" hi default link clighter8Constructor Identifier
""" hi default link clighter8Destructor Identifier
""" hi default link clighter8TemplateTypeParameter Identifier
""" hi default link clighter8TemplateNoneTypeParameter Identifier
""" hi default link clighter8FunctionTemplate Identifier
""" hi default link clighter8ClassTemplate Identifier
""" hi default link clighter8TypeRef Type
""" hi default link clighter8TemplateRef Type
""" hi default link clighter8NamespaceRef Type
""" hi default link clighter8MemberRef Type
""" hi default link clighter8DeclRefExpr Type
""" hi default link clighter8MemberRefExpr Type
""" hi default link clighter8CallExpr Type
""" hi default link clighter8MacroInstantiation Constant
""" hi default link clighter8InclusionDirective cIncluded
""" 

hi default link clighter8Usage IncSearch

""" The comments below a extracted from libclang's python bindings

"""
" Declaration Kinds
" A declaration whose specific kind is not exposed via this interface.
"
" Unexposed declarations have the same operations as any other kind of
" declaration; one can extract their location information, spelling, find their
" definitions, etc. However, the specific kind of the declaration is not
" reported.
hi default link clighter8UnexposedDecl                         Identifier
" A C or C++ struct.
hi default link clighter8StructDecl                            Identifier
" A C or C++ union.
hi default link clighter8UnionDecl                             Identifier
" A C++ class.
hi default link clighter8ClassDecl                             Identifier
" An enumeration.
hi default link clighter8EnumDecl                              Identifier
" A field (in C) or non-static data member (in C++) in a struct, union, or C++
" class.
hi default link clighter8FieldDecl                             Identifier
" An enumerator constant.
hi default link clighter8EnumConstantDecl                      Constant
" A function.
hi default link clighter8FunctionDecl                          Identifier
" A variable.
hi default link clighter8VarDecl                               Identifier
" A function or method parameter.
hi default link clighter8ParmDecl                              Identifier
" An Objective-C @interface.
hi default link clighter8ObjcInterfaceDecl                     Identifier
" An Objective-C @interface for a category.
hi default link clighter8ObjcCategoryDecl                      Identifier
" An Objective-C @protocol declaration.
hi default link clighter8ObjcProtocolDecl                      Identifier
" An Objective-C @property declaration.
hi default link clighter8ObjcPropertyDecl                      Identifier
" An Objective-C instance variable.
hi default link clighter8ObjcIvarDecl                          Identifier
" An Objective-C instance method.
hi default link clighter8ObjcInstanceMethodDecl                Identifier
" An Objective-C class method.
hi default link clighter8ObjcClassMethodDecl                   Identifier
" An Objective-C @implementation.
hi default link clighter8ObjcImplementationDecl                Identifier
" An Objective-C @implementation for a category.
hi default link clighter8ObjcCategoryImplDecl                  Identifier
" A typedef.
hi default link clighter8TypedefDecl                           Identifier
" A C++ class method.
hi default link clighter8CxxMethod                             Identifier
" A C++ namespace.
hi default link clighter8Namespace                             Identifier
" A linkage specification, e.g. 'extern "C"'.
hi default link clighter8LinkageSpec                           Identifier
" A C++ constructor.
hi default link clighter8Constructor                           Identifier
" A C++ destructor.
hi default link clighter8Destructor                            Identifier
" A C++ conversion function.
hi default link clighter8ConversionFunction                    Identifier
" A C++ template type parameter
hi default link clighter8TemplateTypeParameter                 Identifier
" A C++ non-type template paramater.
hi default link clighter8TemplateNonTypeParameter              Identifier
" A C++ template template parameter.
hi default link clighter8TemplateTemplateParameter             Identifier
" A C++ function template.
hi default link clighter8FunctionTemplate                      Identifier
" A C++ class template.
hi default link clighter8ClassTemplate                         Identifier
" A C++ class template partial specialization.
hi default link clighter8ClassTemplatePartialSpecialization    Identifier
" A C++ namespace alias declaration.
hi default link clighter8NamespaceAlias                        Identifier
" A C++ using directive
hi default link clighter8UsingDirective                        Identifier
" A C++ using declaration
hi default link clighter8UsingDeclaration                      Identifier
" A Type alias decl.
hi default link clighter8TypeAliasDecl                         Identifier
" A Objective-C synthesize decl
hi default link clighter8ObjcSynthesizeDecl                    Identifier
" A Objective-C dynamic decl
hi default link clighter8ObjcDynamicDecl                       Identifier
" A C++ access specifier decl.
hi default link clighter8CxxAccessSpecDecl                     Identifier
"""
" Reference Kinds
hi default link clighter8ObjcSuperClassRef                     Type
hi default link clighter8ObjcProtocolRef                       Type
hi default link clighter8ObjcClassRef                          Type
" A reference to a type declaration.
"
" A type reference occurs anywhere where a type is named but not
" declared. For example, given:
"   typedef unsigned sizeType;
"   sizeType size;
"
" The typedef is a declaration of sizeType (CXCursor_TypedefDecl),
" while the type of the variable "size" is referenced. The cursor
" referenced by the type of size is the typedef for sizeType.
hi default link clighter8TypeRef                               Type
hi default link clighter8CxxBaseSpecifier                      Type
" A reference to a class template, function template, template
" template parameter, or class template partial specialization.
hi default link clighter8TemplateRef                           Type
" A reference to a namespace or namepsace alias.
hi default link clighter8NamespaceRef                          Type
" A reference to a member of a struct, union, or class that occurs in
" some non-expression context, e.g., a designated initializer.
hi default link clighter8MemberRef                             Type
" A reference to a labeled statement.
hi default link clighter8LabelRef                              Type
" A reference to a set of overloaded functions or function templates
" that has not yet been resolved to a specific function or function template.
hi default link clighter8OverloadedDeclRef                     Type
" A reference to a variable that occurs in some non-expression
" context, e.g., a C++ lambda capture list.
hi default link clighter8VariableRef                           Type
"""
" Invalid/Error Kinds
hi default link clighter8InvalidFile                           Error
hi default link clighter8NoDeclFound                           Error
hi default link clighter8NotImplemented                        Error
hi default link clighter8InvalidCode                           Error
"""
" Expression Kinds
" An expression whose specific kind is not exposed via this interface.
"
" Unexposed expressions have the same operations as any other kind of
" expression; one can extract their location information, spelling, children,
" etc. However, the specific kind of the expression is not reported.
hi default link clighter8UnexposedExpr                         Normal
" An expression that refers to some value declaration, such as a function,
" varible, or enumerator.
hi default link clighter8DeclRefExpr                           Type
" An expression that refers to a member of a struct, union, class, Objective-C
" class, etc.
hi default link clighter8MemberRefExpr                         Type
" An expression that calls a function.
hi default link clighter8CallExpr                              Type
" An expression that sends a message to an Objective-C object or class.
hi default link clighter8ObjcMessageExpr                       Normal
" An expression that represents a block literal.
hi default link clighter8BlockExpr                             Normal
" An integer literal.
hi default link clighter8IntegerLiteral                        Normal
" A floating point number literal.
hi default link clighter8FloatingLiteral                       Normal
" An imaginary number literal.
hi default link clighter8ImaginaryLiteral                      Normal
" A string literal.
hi default link clighter8StringLiteral                         Normal
" A character literal.
hi default link clighter8CharacterLiteral                      Normal
" A parenthesized expression, e.g. "(1)".
"
" This AST node is only formed if full location information is requested.
hi default link clighter8ParenExpr                             Normal
" This represents the unary-expression's (except sizeof and
" alignof).
hi default link clighter8UnaryOperator                         Normal
" [C99 6.5.2.1] Array Subscripting.
hi default link clighter8ArraySubscriptExpr                    Normal
" A builtin binary operation expression such as "x + y" or
" "x <= y".
hi default link clighter8BinaryOperator                        Normal
" Compound assignment such as "+=".
hi default link clighter8CompoundAssignmentOperator            Normal
" The ?: ternary operator.
hi default link clighter8ConditionalOperator                   Normal
" An explicit cast in C (C99 6.5.4) or a C-style cast in C++
" (C++ [expr.cast]), which uses the syntax (Type)expr.
"
" For example: (int)f.
hi default link clighter8CstyleCastExpr                        Normal
" [C99 6.5.2.5]
hi default link clighter8CompoundLiteralExpr                   Normal
" Describes an C or C++ initializer list.
hi default link clighter8InitListExpr                          Normal
" The GNU address of label extension, representing &&label.
hi default link clighter8AddrLabelExpr                         Normal
" This is the GNU Statement Expression extension: ({int X=4; X;})
hi default link clighter8StmtExpr                              Normal
" Represents a C11 generic selection.
hi default link clighter8GenericSelectionExpr                  Normal
" Implements the GNU _Null extension, which is a name for a null
" pointer constant that has integral type (e.g., int or long) and is the same
" size and alignment as a pointer.
"
" The _Null extension is typically only used by system headers, which define
" NULL as _Null in C++ rather than using 0 (which is an integer that may not
" match the size of a pointer).
hi default link clighter8GnuNullExpr                           Normal
" C++'s staticCast<> expression.
hi default link clighter8CxxStaticCastExpr                     Normal
" C++'s dynamicCast<> expression.
hi default link clighter8CxxDynamicCastExpr                    Normal
" C++'s reinterpretCast<> expression.
hi default link clighter8CxxReinterpretCastExpr                Normal
" C++'s constCast<> expression.
hi default link clighter8CxxConstCastExpr                      Normal
" Represents an explicit C++ type conversion that uses "functional"
" notion (C++ [expr.type.conv]).
"
" Example:
" \code
"   x = int(0.5);
" \endcode
hi default link clighter8CxxFunctionalCastExpr                 Normal
" A C++ typeid expression (C++ [expr.typeid]).
hi default link clighter8CxxTypeidExpr                         Normal
" [C++ 2.13.5] C++ Boolean Literal.
hi default link clighter8CxxBoolLiteralExpr                    Normal
" [C++0x 2.14.7] C++ Pointer Literal.
hi default link clighter8CxxNullPtrLiteralExpr                 Normal
" Represents the "this" expression in C++
hi default link clighter8CxxThisExpr                           Normal
" [C++ 15] C++ Throw Expression.
"
" This handles 'throw' and 'throw' assignment-expression. When
" assignment-expression isn't present, Op will be null.
hi default link clighter8CxxThrowExpr                          Normal
" A new expression for memory allocation and constructor calls, e.g:
" "new CXXNewExpr(foo)".
hi default link clighter8CxxNewExpr                            Normal
" A delete expression for memory deallocation and destructor calls,
" e.g. "delete[] pArray".
hi default link clighter8CxxDeleteExpr                         Normal
" Represents a unary expression.
hi default link clighter8CxxUnaryExpr                          Normal
" ObjCStringLiteral, used for Objective-C string literals i.e. "foo".
hi default link clighter8ObjcStringLiteral                     Normal
" ObjCEncodeExpr, used for in Objective-C.
hi default link clighter8ObjcEncodeExpr                        Normal
" ObjCSelectorExpr used for in Objective-C.
hi default link clighter8ObjcSelectorExpr                      Normal
" Objective-C's protocol expression.
hi default link clighter8ObjcProtocolExpr                      Normal
" An Objective-C "bridged" cast expression, which casts between
" Objective-C pointers and C pointers, transferring ownership in the process.
"
" \code
"   NSString *str = (_BridgeTransfer NSString *)CFCreateString();
" \endcode
hi default link clighter8ObjcBridgeCastExpr                    Normal
" Represents a C++0x pack expansion that produces a sequence of
" expressions.
"
" A pack expansion expression contains a pattern (which itself is an
" expression) followed by an ellipsis. For example:
hi default link clighter8PackExpansionExpr                     Normal
" Represents an expression that computes the length of a parameter
" pack.
hi default link clighter8SizeOfPackExpr                        Normal
" Represents a C++ lambda expression that produces a local function
" object.
"
"  \code
"  void abssort(float *x, unsigned N) {
"    std::sort(x, x + N,
"              [](float a, float b) {
"                return std::abs(a) < std::abs(b);
"              });
"  }
"  \endcode
hi default link clighter8LambdaExpr                            Normal
" Objective-c Boolean Literal.
hi default link clighter8ObjBoolLiteralExpr                    Normal
" Represents the "self" expression in a ObjC method.
hi default link clighter8ObjSelfExpr                           Normal
" OpenMP 4.0 [2.4, Array Section].
hi default link clighter8OmpArraySectionExpr                   Normal
" Represents an @available(...) check.
hi default link clighter8ObjcAvailabilityCheckExpr             Normal
" A statement whose specific kind is not exposed via this interface.
"
" Unexposed statements have the same operations as any other kind of statement;
" one can extract their location information, spelling, children, etc. However,
" the specific kind of the statement is not reported.
hi default link clighter8UnexposedStmt                         Statement
" A labelled statement in a function.
hi default link clighter8LabelStmt                             Statement
" A compound statement
hi default link clighter8CompoundStmt                          Statement
" A case statement.
hi default link clighter8CaseStmt                              Statement
" A default statement.
hi default link clighter8DefaultStmt                           Statement
" An if statement.
hi default link clighter8IfStmt                                Statement
" A switch statement.
hi default link clighter8SwitchStmt                            Statement
" A while statement.
hi default link clighter8WhileStmt                             Statement
" A do statement.
hi default link clighter8DoStmt                                Statement
" A for statement.
hi default link clighter8ForStmt                               Statement
" A goto statement.
hi default link clighter8GotoStmt                              Statement
" An indirect goto statement.
hi default link clighter8IndirectGotoStmt                      Statement
" A continue statement.
hi default link clighter8ContinueStmt                          Statement
" A break statement.
hi default link clighter8BreakStmt                             Statement
" A return statement.
hi default link clighter8ReturnStmt                            Statement
" A GNU-style inline assembler statement.
hi default link clighter8AsmStmt                               Statement
" Objective-C's overall @try-@catch-@finally statement.
hi default link clighter8ObjcAtTryStmt                         Statement
" Objective-C's @catch statement.
hi default link clighter8ObjcAtCatchStmt                       Statement
" Objective-C's @finally statement.
hi default link clighter8ObjcAtFinallyStmt                     Statement
" Objective-C's @throw statement.
hi default link clighter8ObjcAtThrowStmt                       Statement
" Objective-C's @synchronized statement.
hi default link clighter8ObjcAtSynchronizedStmt                Statement
" Objective-C's autorealease pool statement.
hi default link clighter8ObjcAutoreleasePoolStmt               Statement
" Objective-C's for collection statement.
hi default link clighter8ObjcForCollectionStmt                 Statement
" C++'s catch statement.
hi default link clighter8CxxCatchStmt                          Statement
" C++'s try statement.
hi default link clighter8CxxTryStmt                            Statement
" C++'s for (*                                 : *) statement.
hi default link clighter8CxxForRangeStmt                       Statement
" Windows Structured Exception Handling's try statement.
hi default link clighter8SehTryStmt                            Statement
" Windows Structured Exception Handling's except statement.
hi default link clighter8SehExceptStmt                         Statement
" Windows Structured Exception Handling's finally statement.
hi default link clighter8SehFinallyStmt                        Statement
" A MS inline assembly statement extension.
hi default link clighter8MsAsmStmt                             Statement
" The null statement.
hi default link clighter8NullStmt                              Statement
" Adaptor class for mixing declarations with statements and expressions.
hi default link clighter8DeclStmt                              Statement
" OpenMP parallel directive.
hi default link clighter8OmpParallelDirective                  Statement
" OpenMP SIMD directive.
hi default link clighter8OmpSimdDirective                      Statement
" OpenMP for directive.
hi default link clighter8OmpForDirective                       Statement
" OpenMP sections directive.
hi default link clighter8OmpSectionsDirective                  Statement
" OpenMP section directive.
hi default link clighter8OmpSectionDirective                   Statement
" OpenMP single directive.
hi default link clighter8OmpSingleDirective                    Statement
" OpenMP parallel for directive.
hi default link clighter8OmpParallelForDirective               Statement
" OpenMP parallel sections directive.
hi default link clighter8OmpParallelSectionsDirective          Statement
" OpenMP task directive.
hi default link clighter8OmpTaskDirective                      Statement
" OpenMP master directive.
hi default link clighter8OmpMasterDirective                    Statement
" OpenMP critical directive.
hi default link clighter8OmpCriticalDirective                  Statement
" OpenMP taskyield directive.
hi default link clighter8OmpTaskyieldDirective                 Statement
" OpenMP barrier directive.
hi default link clighter8OmpBarrierDirective                   Statement
" OpenMP taskwait directive.
hi default link clighter8OmpTaskwaitDirective                  Statement
" OpenMP flush directive.
hi default link clighter8OmpFlushDirective                     Statement
" Windows Structured Exception Handling's leave statement.
hi default link clighter8SehLeaveStmt                          Statement
" OpenMP ordered directive.
hi default link clighter8OmpOrderedDirective                   Statement
" OpenMP atomic directive.
hi default link clighter8OmpAtomicDirective                    Statement
" OpenMP for SIMD directive.
hi default link clighter8OmpForSimdDirective                   Statement
" OpenMP parallel for SIMD directive.
hi default link clighter8OmpParallelforsimdDirective           Statement
" OpenMP target directive.
hi default link clighter8OmpTargetDirective                    Statement
" OpenMP teams directive.
hi default link clighter8OmpTeamsDirective                     Statement
" OpenMP taskgroup directive.
hi default link clighter8OmpTaskgroupDirective                 Statement
" OpenMP cancellation point directive.
hi default link clighter8OmpCancellationPointDirective         Statement
" OpenMP cancel directive.
hi default link clighter8OmpCancelDirective                    Statement
" OpenMP target data directive.
hi default link clighter8OmpTargetDataDirective                Statement
" OpenMP taskloop directive.
hi default link clighter8OmpTaskLoopDirective                  Statement
" OpenMP taskloop simd directive.
hi default link clighter8OmpTaskLoopSimdDirective              Statement
" OpenMP distribute directive.
hi default link clighter8OmpDistributeDirective                Statement
" OpenMP target enter data directive.
hi default link clighter8OmpTargetEnterDataDirective           Statement
" OpenMP target exit data directive.
hi default link clighter8OmpTargetExitDataDirective            Statement
" OpenMP target parallel directive.
hi default link clighter8OmpTargetParallelDirective            Statement
" OpenMP target parallel for directive.
hi default link clighter8OmpTargetParallelforDirective         Statement
" OpenMP target update directive.
hi default link clighter8OmpTargetUpdateDirective              Statement
" OpenMP distribute parallel for directive.
hi default link clighter8OmpDistributeParallelforDirective     Statement
" OpenMP distribute parallel for simd directive.
hi default link clighter8OmpDistributeParallelForSimdDirective Statement
" OpenMP distribute simd directive.
hi default link clighter8OmpDistributeSimdDirective            Statement
" OpenMP target parallel for simd directive.
hi default link clighter8OmpTargetParallelForSimdDirective     Statement
" OpenMP target simd directive.
hi default link clighter8OmpTargetSimdDirective                Statement
" OpenMP teams distribute directive.
hi default link clighter8OmpTeamsDistributeDirective           Statement
"""
" Other Kinds
" Cursor that represents the translation unit itself.
"
" The translation unit cursor exists primarily to act as the root cursor for
" traversing the contents of a translation unit.
hi default link clighter8TranslationUnit                       Normal
"""
" Attributes
" An attribute whoe specific kind is note exposed via this interface
hi default link clighter8UnexposedAttr                         Normal
hi default link clighter8IbActionAttr                          Normal
hi default link clighter8IbOutletAttr                          Normal
hi default link clighter8IbOutletCollectionAttr                Normal
hi default link clighter8CxxFinalAttr                          Normal
hi default link clighter8CxxOverrideAttr                       Normal
hi default link clighter8AnnotateAttr                          Normal
hi default link clighter8AsmLabelAttr                          Normal
hi default link clighter8PackedAttr                            Normal
hi default link clighter8PureAttr                              Normal
hi default link clighter8ConstAttr                             Normal
hi default link clighter8NoduplicateAttr                       Normal
hi default link clighter8CudaconstantAttr                      Normal
hi default link clighter8CudadeviceAttr                        Normal
hi default link clighter8CudaglobalAttr                        Normal
hi default link clighter8CudahostAttr                          Normal
hi default link clighter8CudasharedAttr                        Normal
hi default link clighter8VisibilityAttr                        Normal
hi default link clighter8DllexportAttr                         Normal
hi default link clighter8DllimportAttr                         Normal
"""
" Preprocessing
hi default link clighter8PreprocessingDirective                PreProc
hi default link clighter8MacroDefinition                       PreProc
hi default link clighter8MacroInstantiation                    Constant
hi default link clighter8InclusionDirective                    cIncluded
"""
" Extra declaration
" A module import declaration.
hi default link clighter8ModuleImportDecl                      Special
" A type alias template declaration
hi default link clighter8TypeAliasTemplateDecl                 Special
" A staticAssert or _StaticAssert node
hi default link clighter8StaticAssert                          Special
" A friend declaration
hi default link clighter8FriendDecl                            Special
" A code completion overload candidate.
hi default link clighter8OverloadCandidate                     Special
