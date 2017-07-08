from clang import cindex

KindToGroup = {
    ###
    # Declaration Kinds
    # A declaration whose specific kind is not exposed via this interface.
    #
    # Unexposed declarations have the same operations as any other kind of
    # declaration; one can extract their location information, spelling, find their
    # definitions, etc. However, the specific kind of the declaration is not
    # reported.
    cindex.CursorKind.UNEXPOSED_DECL                                                : 'clighter8UnexposedDecl',
    # A C or C++ struct.
    cindex.CursorKind.STRUCT_DECL                                                   : 'clighter8StructDecl',
    # A C or C++ union.
    cindex.CursorKind.UNION_DECL                                                    : 'clighter8UnionDecl',
    # A C++ class.
    cindex.CursorKind.CLASS_DECL                                                    : 'clighter8ClassDecl',
    # An enumeration.
    cindex.CursorKind.ENUM_DECL                                                     : 'clighter8EnumDecl',
    # A field (in C) or non-static data member (in C++) in a struct, union, or C++
    # class.
    cindex.CursorKind.FIELD_DECL                                                    : 'clighter8FieldDecl',
    # An enumerator constant.
    cindex.CursorKind.ENUM_CONSTANT_DECL                                            : 'clighter8EnumConstantDecl',
    # A function.
    cindex.CursorKind.FUNCTION_DECL                                                 : 'clighter8FunctionDecl',
    # A variable.
    cindex.CursorKind.VAR_DECL                                                      : 'clighter8VarDecl',
    # A function or method parameter.
    cindex.CursorKind.PARM_DECL                                                     : 'clighter8ParmDecl',
    # An Objective-C @interface.
    cindex.CursorKind.OBJC_INTERFACE_DECL                                           : 'clighter8ObjcInterfaceDecl',
    # An Objective-C @interface for a category.
    cindex.CursorKind.OBJC_CATEGORY_DECL                                            : 'clighter8ObjcCategoryDecl',
    # An Objective-C @protocol declaration.
    cindex.CursorKind.OBJC_PROTOCOL_DECL                                            : 'clighter8ObjcProtocolDecl',
    # An Objective-C @property declaration.
    cindex.CursorKind.OBJC_PROPERTY_DECL                                            : 'clighter8ObjcPropertyDecl',
    # An Objective-C instance variable.
    cindex.CursorKind.OBJC_IVAR_DECL                                                : 'clighter8ObjcIvarDecl',
    # An Objective-C instance method.
    cindex.CursorKind.OBJC_INSTANCE_METHOD_DECL                                     : 'clighter8ObjcInstanceMethodDecl',
    # An Objective-C class method.
    cindex.CursorKind.OBJC_CLASS_METHOD_DECL                                        : 'clighter8ObjcClassMethodDecl',
    # An Objective-C @implementation.
    cindex.CursorKind.OBJC_IMPLEMENTATION_DECL                                      : 'clighter8ObjcImplementationDecl',
    # An Objective-C @implementation for a category.
    cindex.CursorKind.OBJC_CATEGORY_IMPL_DECL                                       : 'clighter8ObjcCategoryImplDecl',
    # A typedef.
    cindex.CursorKind.TYPEDEF_DECL                                                  : 'clighter8TypedefDecl',
    # A C++ class method.
    cindex.CursorKind.CXX_METHOD                                                    : 'clighter8CxxMethod',
    # A C++ namespace.
    cindex.CursorKind.NAMESPACE                                                     : 'clighter8Namespace',
    # A linkage specification, e.g. 'extern "C"'.
    cindex.CursorKind.LINKAGE_SPEC                                                  : 'clighter8LinkageSpec',
    # A C++ constructor.
    cindex.CursorKind.CONSTRUCTOR                                                   : 'clighter8Constructor',
    # A C++ destructor.
    cindex.CursorKind.DESTRUCTOR                                                    : 'clighter8Destructor',
    # A C++ conversion function.
    cindex.CursorKind.CONVERSION_FUNCTION                                           : 'clighter8ConversionFunction',
    # A C++ template type parameter
    cindex.CursorKind.TEMPLATE_TYPE_PARAMETER                                       : 'clighter8TemplateTypeParameter',
    # A C++ non-type template paramater.
    cindex.CursorKind.TEMPLATE_NON_TYPE_PARAMETER                                   : 'clighter8TemplateNonTypeParameter',
    # A C++ template template parameter.
    cindex.CursorKind.TEMPLATE_TEMPLATE_PARAMETER                                   : 'clighter8TemplateTemplateParameter',
    # A C++ function template.
    cindex.CursorKind.FUNCTION_TEMPLATE                                             : 'clighter8FunctionTemplate',
    # A C++ class template.
    cindex.CursorKind.CLASS_TEMPLATE                                                : 'clighter8ClassTemplate',
    # A C++ class template partial specialization.
    cindex.CursorKind.CLASS_TEMPLATE_PARTIAL_SPECIALIZATION                         : 'clighter8ClassTemplatePartialSpecialization',
    # A C++ namespace alias declaration.
    cindex.CursorKind.NAMESPACE_ALIAS                                               : 'clighter8NamespaceAlias',
    # A C++ using directive
    cindex.CursorKind.USING_DIRECTIVE                                               : 'clighter8UsingDirective',
    # A C++ using declaration
    cindex.CursorKind.USING_DECLARATION                                             : 'clighter8UsingDeclaration',
    # A Type alias decl.
    cindex.CursorKind.TYPE_ALIAS_DECL                                               : 'clighter8TypeAliasDecl',
    # A Objective-C synthesize decl
    cindex.CursorKind.OBJC_SYNTHESIZE_DECL                                          : 'clighter8ObjcSynthesizeDecl',
    # A Objective-C dynamic decl
    cindex.CursorKind.OBJC_DYNAMIC_DECL                                             : 'clighter8ObjcDynamicDecl',
    # A C++ access specifier decl.
    cindex.CursorKind.CXX_ACCESS_SPEC_DECL                                          : 'clighter8CxxAccessSpecDecl',
    ###
    # Reference Kinds
    cindex.CursorKind.OBJC_SUPER_CLASS_REF                                          : 'clighter8ObjcSuperClassRef',
    cindex.CursorKind.OBJC_PROTOCOL_REF                                             : 'clighter8ObjcProtocolRef',
    cindex.CursorKind.OBJC_CLASS_REF                                                : 'clighter8ObjcClassRef',
    # A reference to a type declaration.
    #
    # A type reference occurs anywhere where a type is named but not
    # declared. For example, given:
    #   typedef unsigned sizeType;
    #   sizeType size;
    #
    # The typedef is a declaration of sizeType (CXCursor_TypedefDecl),
    # while the type of the variable "size" is referenced. The cursor
    # referenced by the type of size is the typedef for sizeType.
    cindex.CursorKind.TYPE_REF                                                      : 'clighter8TypeRef',
    cindex.CursorKind.CXX_BASE_SPECIFIER                                            : 'clighter8CxxBaseSpecifier',
    # A reference to a class template, function template, template
    # template parameter, or class template partial specialization.
    cindex.CursorKind.TEMPLATE_REF                                                  : 'clighter8TemplateRef',
    # A reference to a namespace or namepsace alias.
    cindex.CursorKind.NAMESPACE_REF                                                 : 'clighter8NamespaceRef',
    # A reference to a member of a struct, union, or class that occurs in
    # some non-expression context, e.g., a designated initializer.
    cindex.CursorKind.MEMBER_REF                                                    : 'clighter8MemberRef',
    # A reference to a labeled statement.
    cindex.CursorKind.LABEL_REF                                                     : 'clighter8LabelRef',
    # A reference to a set of overloaded functions or function templates
    # that has not yet been resolved to a specific function or function template.
    cindex.CursorKind.OVERLOADED_DECL_REF                                           : 'clighter8OverloadedDeclRef',
    # A reference to a variable that occurs in some non-expression
    # context, e.g., a C++ lambda capture list.
    cindex.CursorKind.VARIABLE_REF                                                  : 'clighter8VariableRef',
    ###
    # Invalid/Error Kinds
    cindex.CursorKind.INVALID_FILE                                                  : 'clighter8InvalidFile',
    cindex.CursorKind.NO_DECL_FOUND                                                 : 'clighter8NoDeclFound',
    cindex.CursorKind.NOT_IMPLEMENTED                                               : 'clighter8NotImplemented',
    cindex.CursorKind.INVALID_CODE                                                  : 'clighter8InvalidCode',
    ###
    # Expression Kinds
    # An expression whose specific kind is not exposed via this interface.
    #
    # Unexposed expressions have the same operations as any other kind of
    # expression; one can extract their location information, spelling, children,
    # etc. However, the specific kind of the expression is not reported.
    cindex.CursorKind.UNEXPOSED_EXPR                                                : 'clighter8UnexposedExpr',
    # An expression that refers to some value declaration, such as a function,
    # varible, or enumerator.
    cindex.CursorKind.DECL_REF_EXPR                                                 : 'clighter8DeclRefExpr',
    # An expression that refers to a member of a struct, union, class, Objective-C
    # class, etc.
    cindex.CursorKind.MEMBER_REF_EXPR                                               : 'clighter8MemberRefExpr',
    # An expression that calls a function.
    cindex.CursorKind.CALL_EXPR                                                     : 'clighter8CallExpr',
    # An expression that sends a message to an Objective-C object or class.
    cindex.CursorKind.OBJC_MESSAGE_EXPR                                             : 'clighter8ObjcMessageExpr',
    # An expression that represents a block literal.
    cindex.CursorKind.BLOCK_EXPR                                                    : 'clighter8BlockExpr',
    # An integer literal.
    cindex.CursorKind.INTEGER_LITERAL                                               : 'clighter8IntegerLiteral',
    # A floating point number literal.
    cindex.CursorKind.FLOATING_LITERAL                                              : 'clighter8FloatingLiteral',
    # An imaginary number literal.
    cindex.CursorKind.IMAGINARY_LITERAL                                             : 'clighter8ImaginaryLiteral',
    # A string literal.
    cindex.CursorKind.STRING_LITERAL                                                : 'clighter8StringLiteral',
    # A character literal.
    cindex.CursorKind.CHARACTER_LITERAL                                             : 'clighter8CharacterLiteral',
    # A parenthesized expression, e.g. "(1)".
    #
    # This AST node is only formed if full location information is requested.
    cindex.CursorKind.PAREN_EXPR                                                    : 'clighter8ParenExpr',
    # This represents the unary-expression's (except sizeof and
    # alignof).
    cindex.CursorKind.UNARY_OPERATOR                                                : 'clighter8UnaryOperator',
    # [C99 6.5.2.1] Array Subscripting.
    cindex.CursorKind.ARRAY_SUBSCRIPT_EXPR                                          : 'clighter8ArraySubscriptExpr',
    # A builtin binary operation expression such as "x + y" or
    # "x <= y".
    cindex.CursorKind.BINARY_OPERATOR                                               : 'clighter8BinaryOperator',
    # Compound assignment such as "+=".
    cindex.CursorKind.COMPOUND_ASSIGNMENT_OPERATOR                                  : 'clighter8CompoundAssignmentOperator',
    # The ?: ternary operator.
    cindex.CursorKind.CONDITIONAL_OPERATOR                                          : 'clighter8ConditionalOperator',
    # An explicit cast in C (C99 6.5.4) or a C-style cast in C++
    # (C++ [expr.cast]), which uses the syntax (Type)expr.
    #
    # For example: (int)f.
    cindex.CursorKind.CSTYLE_CAST_EXPR                                              : 'clighter8CstyleCastExpr',
    # [C99 6.5.2.5]
    cindex.CursorKind.COMPOUND_LITERAL_EXPR                                         : 'clighter8CompoundLiteralExpr',
    # Describes an C or C++ initializer list.
    cindex.CursorKind.INIT_LIST_EXPR                                                : 'clighter8InitListExpr',
    # The GNU address of label extension, representing &&label.
    cindex.CursorKind.ADDR_LABEL_EXPR                                               : 'clighter8AddrLabelExpr',
    # This is the GNU Statement Expression extension: ({int X=4; X;})
    cindex.CursorKind.StmtExpr                                                      : 'clighter8StmtExpr',
    # Represents a C11 generic selection.
    cindex.CursorKind.GENERIC_SELECTION_EXPR                                        : 'clighter8GenericSelectionExpr',
    # Implements the GNU _Null extension, which is a name for a null
    # pointer constant that has integral type (e.g., int or long) and is the same
    # size and alignment as a pointer.
    #
    # The _Null extension is typically only used by system headers, which define
    # NULL as _Null in C++ rather than using 0 (which is an integer that may not
    # match the size of a pointer).
    cindex.CursorKind.GNU_NULL_EXPR                                                 : 'clighter8GnuNullExpr',
    # C++'s staticCast<> expression.
    cindex.CursorKind.CXX_STATIC_CAST_EXPR                                          : 'clighter8CxxStaticCastExpr',
    # C++'s dynamicCast<> expression.
    cindex.CursorKind.CXX_DYNAMIC_CAST_EXPR                                         : 'clighter8CxxDynamicCastExpr',
    # C++'s reinterpretCast<> expression.
    cindex.CursorKind.CXX_REINTERPRET_CAST_EXPR                                     : 'clighter8CxxReinterpretCastExpr',
    # C++'s constCast<> expression.
    cindex.CursorKind.CXX_CONST_CAST_EXPR                                           : 'clighter8CxxConstCastExpr',
    # Represents an explicit C++ type conversion that uses "functional"
    # notion (C++ [expr.type.conv]).
    #
    # Example:
    # \code
    #   x = int(0.5);
    # \endcode
    cindex.CursorKind.CXX_FUNCTIONAL_CAST_EXPR                                      : 'clighter8CxxFunctionalCastExpr',
    # A C++ typeid expression (C++ [expr.typeid]).
    cindex.CursorKind.CXX_TYPEID_EXPR                                               : 'clighter8CxxTypeidExpr',
    # [C++ 2.13.5] C++ Boolean Literal.
    cindex.CursorKind.CXX_BOOL_LITERAL_EXPR                                         : 'clighter8CxxBoolLiteralExpr',
    # [C++0x 2.14.7] C++ Pointer Literal.
    cindex.CursorKind.CXX_NULL_PTR_LITERAL_EXPR                                     : 'clighter8CxxNullPtrLiteralExpr',
    # Represents the "this" expression in C++
    cindex.CursorKind.CXX_THIS_EXPR                                                 : 'clighter8CxxThisExpr',
    # [C++ 15] C++ Throw Expression.
    #
    # This handles 'throw' and 'throw' assignment-expression. When
    # assignment-expression isn't present, Op will be null.
    cindex.CursorKind.CXX_THROW_EXPR                                                : 'clighter8CxxThrowExpr',
    # A new expression for memory allocation and constructor calls, e.g:
    # "new CXXNewExpr(foo)".
    cindex.CursorKind.CXX_NEW_EXPR                                                  : 'clighter8CxxNewExpr',
    # A delete expression for memory deallocation and destructor calls,
    # e.g. "delete[] pArray".
    cindex.CursorKind.CXX_DELETE_EXPR                                               : 'clighter8CxxDeleteExpr',
    # Represents a unary expression.
    cindex.CursorKind.CXX_UNARY_EXPR                                                : 'clighter8CxxUnaryExpr',
    # ObjCStringLiteral, used for Objective-C string literals i.e. "foo".
    cindex.CursorKind.OBJC_STRING_LITERAL                                           : 'clighter8ObjcStringLiteral',
    # ObjCEncodeExpr, used for in Objective-C.
    cindex.CursorKind.OBJC_ENCODE_EXPR                                              : 'clighter8ObjcEncodeExpr',
    # ObjCSelectorExpr used for in Objective-C.
    cindex.CursorKind.OBJC_SELECTOR_EXPR                                            : 'clighter8ObjcSelectorExpr',
    # Objective-C's protocol expression.
    cindex.CursorKind.OBJC_PROTOCOL_EXPR                                            : 'clighter8ObjcProtocolExpr',
    # An Objective-C "bridged" cast expression, which casts between
    # Objective-C pointers and C pointers, transferring ownership in the process.
    #
    # \code
    #   NSString *str = (_BridgeTransfer NSString *)CFCreateString();
    # \endcode
    cindex.CursorKind.OBJC_BRIDGE_CAST_EXPR                                         : 'clighter8ObjcBridgeCastExpr',
    # Represents a C++0x pack expansion that produces a sequence of
    # expressions.
    #
    # A pack expansion expression contains a pattern (which itself is an
    # expression) followed by an ellipsis. For example:
    cindex.CursorKind.PACK_EXPANSION_EXPR                                           : 'clighter8PackExpansionExpr',
    # Represents an expression that computes the length of a parameter
    # pack.
    cindex.CursorKind.SIZE_OF_PACK_EXPR                                             : 'clighter8SizeOfPackExpr',
    # Represents a C++ lambda expression that produces a local function
    # object.
    #
    #  \code
    #  void abssort(float *x, unsigned N) {
    #    std::sort(x, x + N,
    #              [](float a, float b) {
    #                return std::abs(a) < std::abs(b);
    #              });
    #  }
    #  \endcode
    cindex.CursorKind.LAMBDA_EXPR                                                   : 'clighter8LambdaExpr',
    # Objective-c Boolean Literal.
    cindex.CursorKind.OBJ_BOOL_LITERAL_EXPR                                         : 'clighter8ObjBoolLiteralExpr',
    # Represents the "self" expression in a ObjC method.
    cindex.CursorKind.OBJ_SELF_EXPR                                                 : 'clighter8ObjSelfExpr',
    # OpenMP 4.0 [2.4, Array Section].
    #cindex.CursorKind.OMP_ARRAY_SECTION_EXPR                                        : 'clighter8OmpArraySectionExpr',
    # Represents an @available(...) check.
    #cindex.CursorKind.OBJC_AVAILABILITY_CHECK_EXPR                                  : 'clighter8ObjcAvailabilityCheckExpr',
    # A statement whose specific kind is not exposed via this interface.
    #
    # Unexposed statements have the same operations as any other kind of statement;
    # one can extract their location information, spelling, children, etc. However,
    # the specific kind of the statement is not reported.
    cindex.CursorKind.UNEXPOSED_STMT                                                : 'clighter8UnexposedStmt',
    # A labelled statement in a function.
    cindex.CursorKind.LABEL_STMT                                                    : 'clighter8LabelStmt',
    # A compound statement
    cindex.CursorKind.COMPOUND_STMT                                                 : 'clighter8CompoundStmt',
    # A case statement.
    cindex.CursorKind.CASE_STMT                                                     : 'clighter8CaseStmt',
    # A default statement.
    cindex.CursorKind.DEFAULT_STMT                                                  : 'clighter8DefaultStmt',
    # An if statement.
    cindex.CursorKind.IF_STMT                                                       : 'clighter8IfStmt',
    # A switch statement.
    cindex.CursorKind.SWITCH_STMT                                                   : 'clighter8SwitchStmt',
    # A while statement.
    cindex.CursorKind.WHILE_STMT                                                    : 'clighter8WhileStmt',
    # A do statement.
    cindex.CursorKind.DO_STMT                                                       : 'clighter8DoStmt',
    # A for statement.
    cindex.CursorKind.FOR_STMT                                                      : 'clighter8ForStmt',
    # A goto statement.
    cindex.CursorKind.GOTO_STMT                                                     : 'clighter8GotoStmt',
    # An indirect goto statement.
    cindex.CursorKind.INDIRECT_GOTO_STMT                                            : 'clighter8IndirectGotoStmt',
    # A continue statement.
    cindex.CursorKind.CONTINUE_STMT                                                 : 'clighter8ContinueStmt',
    # A break statement.
    cindex.CursorKind.BREAK_STMT                                                    : 'clighter8BreakStmt',
    # A return statement.
    cindex.CursorKind.RETURN_STMT                                                   : 'clighter8ReturnStmt',
    # A GNU-style inline assembler statement.
    cindex.CursorKind.ASM_STMT                                                      : 'clighter8AsmStmt',
    # Objective-C's overall @try-@catch-@finally statement.
    cindex.CursorKind.OBJC_AT_TRY_STMT                                              : 'clighter8ObjcAtTryStmt',
    # Objective-C's @catch statement.
    cindex.CursorKind.OBJC_AT_CATCH_STMT                                            : 'clighter8ObjcAtCatchStmt',
    # Objective-C's @finally statement.
    cindex.CursorKind.OBJC_AT_FINALLY_STMT                                          : 'clighter8ObjcAtFinallyStmt',
    # Objective-C's @throw statement.
    cindex.CursorKind.OBJC_AT_THROW_STMT                                            : 'clighter8ObjcAtThrowStmt',
    # Objective-C's @synchronized statement.
    cindex.CursorKind.OBJC_AT_SYNCHRONIZED_STMT                                     : 'clighter8ObjcAtSynchronizedStmt',
    # Objective-C's autorealease pool statement.
    cindex.CursorKind.OBJC_AUTORELEASE_POOL_STMT                                    : 'clighter8ObjcAutoreleasePoolStmt',
    # Objective-C's for collection statement.
    cindex.CursorKind.OBJC_FOR_COLLECTION_STMT                                      : 'clighter8ObjcForCollectionStmt',
    # C++'s catch statement.
    cindex.CursorKind.CXX_CATCH_STMT                                                : 'clighter8CxxCatchStmt',
    # C++'s try statement.
    cindex.CursorKind.CXX_TRY_STMT                                                  : 'clighter8CxxTryStmt',
    # C++'s for (*                                                                  : *) statement.
    cindex.CursorKind.CXX_FOR_RANGE_STMT                                            : 'clighter8CxxForRangeStmt',
    # Windows Structured Exception Handling's try statement.
    cindex.CursorKind.SEH_TRY_STMT                                                  : 'clighter8SehTryStmt',
    # Windows Structured Exception Handling's except statement.
    cindex.CursorKind.SEH_EXCEPT_STMT                                               : 'clighter8SehExceptStmt',
    # Windows Structured Exception Handling's finally statement.
    cindex.CursorKind.SEH_FINALLY_STMT                                              : 'clighter8SehFinallyStmt',
    # A MS inline assembly statement extension.
    cindex.CursorKind.MS_ASM_STMT                                                   : 'clighter8MsAsmStmt',
    # The null statement.
    cindex.CursorKind.NULL_STMT                                                     : 'clighter8NullStmt',
    # Adaptor class for mixing declarations with statements and expressions.
    cindex.CursorKind.DECL_STMT                                                     : 'clighter8DeclStmt',
    # OpenMP parallel directive.
    #cindex.CursorKind.OMP_PARALLEL_DIRECTIVE                                        : 'clighter8OmpParallelDirective',
    # OpenMP SIMD directive.
    #cindex.CursorKind.OMP_SIMD_DIRECTIVE                                            : 'clighter8OmpSimdDirective',
    # OpenMP for directive.
    #cindex.CursorKind.OMP_FOR_DIRECTIVE                                             : 'clighter8OmpForDirective',
    # OpenMP sections directive.
    #cindex.CursorKind.OMP_SECTIONS_DIRECTIVE                                        : 'clighter8OmpSectionsDirective',
    # OpenMP section directive.
    #cindex.CursorKind.OMP_SECTION_DIRECTIVE                                         : 'clighter8OmpSectionDirective',
    # OpenMP single directive.
    #cindex.CursorKind.OMP_SINGLE_DIRECTIVE                                          : 'clighter8OmpSingleDirective',
    # OpenMP parallel for directive.
    #cindex.CursorKind.OMP_PARALLEL_FOR_DIRECTIVE                                    : 'clighter8OmpParallelForDirective',
    # OpenMP parallel sections directive.
    #cindex.CursorKind.OMP_PARALLEL_SECTIONS_DIRECTIVE                               : 'clighter8OmpParallelSectionsDirective',
    # OpenMP task directive.
    #cindex.CursorKind.OMP_TASK_DIRECTIVE                                            : 'clighter8OmpTaskDirective',
    # OpenMP master directive.
    #cindex.CursorKind.OMP_MASTER_DIRECTIVE                                          : 'clighter8OmpMasterDirective',
    # OpenMP critical directive.
    #cindex.CursorKind.OMP_CRITICAL_DIRECTIVE                                        : 'clighter8OmpCriticalDirective',
    # OpenMP taskyield directive.
    #cindex.CursorKind.OMP_TASKYIELD_DIRECTIVE                                       : 'clighter8OmpTaskyieldDirective',
    # OpenMP barrier directive.
    #cindex.CursorKind.OMP_BARRIER_DIRECTIVE                                         : 'clighter8OmpBarrierDirective',
    # OpenMP taskwait directive.
    #cindex.CursorKind.OMP_TASKWAIT_DIRECTIVE                                        : 'clighter8OmpTaskwaitDirective',
    # OpenMP flush directive.
    #cindex.CursorKind.OMP_FLUSH_DIRECTIVE                                           : 'clighter8OmpFlushDirective',
    # Windows Structured Exception Handling's leave statement.
    #cindex.CursorKind.SEH_LEAVE_STMT                                                : 'clighter8SehLeaveStmt',
    # OpenMP ordered directive.
    #cindex.CursorKind.OMP_ORDERED_DIRECTIVE                                         : 'clighter8OmpOrderedDirective',
    # OpenMP atomic directive.
    #cindex.CursorKind.OMP_ATOMIC_DIRECTIVE                                          : 'clighter8OmpAtomicDirective',
    # OpenMP for SIMD directive.
    #cindex.CursorKind.OMP_FOR_SIMD_DIRECTIVE                                        : 'clighter8OmpForSimdDirective',
    # OpenMP parallel for SIMD directive.
    #cindex.CursorKind.OMP_PARALLELFORSIMD_DIRECTIVE                                 : 'clighter8OmpParallelforsimdDirective',
    # OpenMP target directive.
    #cindex.CursorKind.OMP_TARGET_DIRECTIVE                                          : 'clighter8OmpTargetDirective',
    # OpenMP teams directive.
    #cindex.CursorKind.OMP_TEAMS_DIRECTIVE                                           : 'clighter8OmpTeamsDirective',
    # OpenMP taskgroup directive.
    #cindex.CursorKind.OMP_TASKGROUP_DIRECTIVE                                       : 'clighter8OmpTaskgroupDirective',
    # OpenMP cancellation point directive.
    #cindex.CursorKind.OMP_CANCELLATION_POINT_DIRECTIVE                              : 'clighter8OmpCancellationPointDirective',
    # OpenMP cancel directive.
    #cindex.CursorKind.OMP_CANCEL_DIRECTIVE                                          : 'clighter8OmpCancelDirective',
    # OpenMP target data directive.
    #cindex.CursorKind.OMP_TARGET_DATA_DIRECTIVE                                     : 'clighter8OmpTargetDataDirective',
    # OpenMP taskloop directive.
    #cindex.CursorKind.OMP_TASK_LOOP_DIRECTIVE                                       : 'clighter8OmpTaskLoopDirective',
    # OpenMP taskloop simd directive.
    #cindex.CursorKind.OMP_TASK_LOOP_SIMD_DIRECTIVE                                  : 'clighter8OmpTaskLoopSimdDirective',
    # OpenMP distribute directive.
    #cindex.CursorKind.OMP_DISTRIBUTE_DIRECTIVE                                      : 'clighter8OmpDistributeDirective',
    # OpenMP target enter data directive.
    #cindex.CursorKind.OMP_TARGET_ENTER_DATA_DIRECTIVE                               : 'clighter8OmpTargetEnterDataDirective',
    # OpenMP target exit data directive.
    #cindex.CursorKind.OMP_TARGET_EXIT_DATA_DIRECTIVE                                : 'clighter8OmpTargetExitDataDirective',
    # OpenMP target parallel directive.
    #cindex.CursorKind.OMP_TARGET_PARALLEL_DIRECTIVE                                 : 'clighter8OmpTargetParallelDirective',
    # OpenMP target parallel for directive.
    #cindex.CursorKind.OMP_TARGET_PARALLELFOR_DIRECTIVE                              : 'clighter8OmpTargetParallelforDirective',
    # OpenMP target update directive.
    #cindex.CursorKind.OMP_TARGET_UPDATE_DIRECTIVE                                   : 'clighter8OmpTargetUpdateDirective',
    # OpenMP distribute parallel for directive.
    #cindex.CursorKind.OMP_DISTRIBUTE_PARALLELFOR_DIRECTIVE                          : 'clighter8OmpDistributeParallelforDirective',
    # OpenMP distribute parallel for simd directive.
    #cindex.CursorKind.OMP_DISTRIBUTE_PARALLEL_FOR_SIMD_DIRECTIVE                    : 'clighter8OmpDistributeParallelForSimdDirective',
    # OpenMP distribute simd directive.
    #cindex.CursorKind.OMP_DISTRIBUTE_SIMD_DIRECTIVE                                 : 'clighter8OmpDistributeSimdDirective',
    # OpenMP target parallel for simd directive.
    #cindex.CursorKind.OMP_TARGET_PARALLEL_FOR_SIMD_DIRECTIVE                        : 'clighter8OmpTargetParallelForSimdDirective',
    # OpenMP target simd directive.
    #cindex.CursorKind.OMP_TARGET_SIMD_DIRECTIVE                                     : 'clighter8OmpTargetSimdDirective',
    # OpenMP teams distribute directive.
    #cindex.CursorKind.OMP_TEAMS_DISTRIBUTE_DIRECTIVE                                : 'clighter8OmpTeamsDistributeDirective',
    ###
    # Other Kinds
    # Cursor that represents the translation unit itself.
    #
    # The translation unit cursor exists primarily to act as the root cursor for
    # traversing the contents of a translation unit.
    cindex.CursorKind.TRANSLATION_UNIT                                              : 'clighter8TranslationUnit',
    ###
    # Attributes
    # An attribute whoe specific kind is note exposed via this interface
    cindex.CursorKind.UNEXPOSED_ATTR                                                : 'clighter8UnexposedAttr',
    cindex.CursorKind.IB_ACTION_ATTR                                                : 'clighter8IbActionAttr',
    cindex.CursorKind.IB_OUTLET_ATTR                                                : 'clighter8IbOutletAttr',
    cindex.CursorKind.IB_OUTLET_COLLECTION_ATTR                                     : 'clighter8IbOutletCollectionAttr',
    cindex.CursorKind.CXX_FINAL_ATTR                                                : 'clighter8CxxFinalAttr',
    cindex.CursorKind.CXX_OVERRIDE_ATTR                                             : 'clighter8CxxOverrideAttr',
    cindex.CursorKind.ANNOTATE_ATTR                                                 : 'clighter8AnnotateAttr',
    cindex.CursorKind.ASM_LABEL_ATTR                                                : 'clighter8AsmLabelAttr',
    cindex.CursorKind.PACKED_ATTR                                                   : 'clighter8PackedAttr',
    cindex.CursorKind.PURE_ATTR                                                     : 'clighter8PureAttr',
    cindex.CursorKind.CONST_ATTR                                                    : 'clighter8ConstAttr',
    cindex.CursorKind.NODUPLICATE_ATTR                                              : 'clighter8NoduplicateAttr',
    cindex.CursorKind.CUDACONSTANT_ATTR                                             : 'clighter8CudaconstantAttr',
    cindex.CursorKind.CUDADEVICE_ATTR                                               : 'clighter8CudadeviceAttr',
    cindex.CursorKind.CUDAGLOBAL_ATTR                                               : 'clighter8CudaglobalAttr',
    cindex.CursorKind.CUDAHOST_ATTR                                                 : 'clighter8CudahostAttr',
    cindex.CursorKind.CUDASHARED_ATTR                                               : 'clighter8CudasharedAttr',
    cindex.CursorKind.VISIBILITY_ATTR                                               : 'clighter8VisibilityAttr',
    cindex.CursorKind.DLLEXPORT_ATTR                                                : 'clighter8DllexportAttr',
    cindex.CursorKind.DLLIMPORT_ATTR                                                : 'clighter8DllimportAttr',
    ###
    # Preprocessing
    cindex.CursorKind.PREPROCESSING_DIRECTIVE                                       : 'clighter8PreprocessingDirective',
    cindex.CursorKind.MACRO_DEFINITION                                              : 'clighter8MacroDefinition',
    cindex.CursorKind.MACRO_INSTANTIATION                                           : 'clighter8MacroInstantiation',
    cindex.CursorKind.INCLUSION_DIRECTIVE                                           : 'clighter8InclusionDirective',
    ###
    # Extra declaration
    # A module import declaration.
    cindex.CursorKind.MODULE_IMPORT_DECL                                            : 'clighter8ModuleImportDecl',
    # A type alias template declaration
    cindex.CursorKind.TYPE_ALIAS_TEMPLATE_DECL                                      : 'clighter8TypeAliasTemplateDecl',
    # A staticAssert or _StaticAssert node
    #cindex.CursorKind.STATIC_ASSERT                                                 : 'clighter8StaticAssert',
    # A friend declaration
    #cindex.CursorKind.FRIEND_DECL                                                   : 'clighter8FriendDecl',
    # A code completion overload candidate.
    cindex.CursorKind.OVERLOAD_CANDIDATE                                            : 'clighter8OverloadCandidate',
}


def get_hlt_group(kind, whitelist, blacklist):
    group = KindToGroup.get(kind)

    if not group:
        if kind.is_declaration():
            group = 'clighter8Decl'
        elif kind.is_reference():
            group = 'clighter8Ref'
        elif kind.is_expression():
            group = 'clighter8Expr'
        elif kind.is_statement():
            group = 'clighter8Stat'
        elif kind.is_preprocessing():
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

    # if cursor.location.line != row or col < cursor.location.column or col >= cursor.location.column + \
        # len(symbol.spelling):
        # return None

    return symbol


def get_semantic_symbol(cursor):
    if not cursor:
        return None

    symbol = cursor.get_definition()
    if not symbol:
        symbol = cursor.referenced

        if not symbol:
            symbol = cursor.canonical

    if not symbol:
        return None

    if symbol.kind == cindex.CursorKind.CONSTRUCTOR or symbol.kind == cindex.CursorKind.DESTRUCTOR:
        symbol = symbol.semantic_parent

    return symbol


def search_by_usr(tu, bufname, usr, result):
    if not tu:
        return None

    tokens = tu.cursor.get_tokens()
    for token in tokens:
        cursor = get_cursor(
            tu, bufname, token.location.line, token.location.column)

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


def get_cwd_includes(tu, cwd):
    if not tu:
        return []

    result = []

    for i in tu.get_includes():
        if i.is_input_file:
            continue

        if not i.include.name.startswith(cwd):
            continue

        result.append(i.include.name)

    return result
