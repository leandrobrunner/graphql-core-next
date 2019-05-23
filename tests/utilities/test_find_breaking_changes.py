from graphql.type import (
    GraphQLSchema,
    GraphQLDeprecatedDirective,
    GraphQLIncludeDirective,
    GraphQLSkipDirective,
)
from graphql.utilities import (
    BreakingChangeType,
    DangerousChangeType,
    build_schema,
    find_breaking_changes,
    find_dangerous_changes,
)


def describe_find_breaking_changes():
    def should_detect_if_a_type_was_removed_or_not():
        old_schema = build_schema(
            """
            type Type1
            type Type2
            """
        )

        new_schema = build_schema(
            """
            type Type2
            """
        )

        assert find_breaking_changes(old_schema, new_schema) == [
            (BreakingChangeType.TYPE_REMOVED, "Type1 was removed.")
        ]
        assert find_breaking_changes(old_schema, old_schema) == []

    def should_detect_if_a_type_changed_its_type():
        old_schema = build_schema(
            """
            interface Type1
            """
        )

        new_schema = build_schema(
            """
            union Type1
            """
        )

        assert find_breaking_changes(old_schema, new_schema) == [
            (
                BreakingChangeType.TYPE_CHANGED_KIND,
                "Type1 changed from an Interface type to a Union type.",
            )
        ]

    def should_detect_if_a_field_on_type_was_deleted_or_changed_type():
        old_schema = build_schema(
            """
            type TypeA
            type TypeB

            interface Type1 {
              field1: TypeA
              field2: String
              field3: String
              field4: TypeA
              field6: String
              field7: [String]
              field8: Int
              field9: Int!
              field10: [Int]!
              field11: Int
              field12: [Int]
              field13: [Int!]
              field14: [Int]
              field15: [[Int]]
              field16: Int!
              field17: [Int]
              field18: [[Int!]!]
            }
            """
        )

        new_schema = build_schema(
            """
            type TypeA
            type TypeB

            interface Type1 {
              field1: TypeA
              field3: Boolean
              field4: TypeB
              field5: String
              field6: [String]
              field7: String
              field8: Int!
              field9: Int
              field10: [Int]
              field11: [Int]!
              field12: [Int!]
              field13: [Int]
              field14: [[Int]]
              field15: [Int]
              field16: [Int]!
              field17: [Int]!
              field18: [[Int!]]
            }
            """
        )

        assert find_breaking_changes(old_schema, new_schema) == [
            (BreakingChangeType.FIELD_REMOVED, "Type1.field2 was removed."),
            (
                BreakingChangeType.FIELD_CHANGED_KIND,
                "Type1.field3 changed type from String to Boolean.",
            ),
            (
                BreakingChangeType.FIELD_CHANGED_KIND,
                "Type1.field4 changed type from TypeA to TypeB.",
            ),
            (
                BreakingChangeType.FIELD_CHANGED_KIND,
                "Type1.field6 changed type from String to [String].",
            ),
            (
                BreakingChangeType.FIELD_CHANGED_KIND,
                "Type1.field7 changed type from [String] to String.",
            ),
            (
                BreakingChangeType.FIELD_CHANGED_KIND,
                "Type1.field9 changed type from Int! to Int.",
            ),
            (
                BreakingChangeType.FIELD_CHANGED_KIND,
                "Type1.field10 changed type from [Int]! to [Int].",
            ),
            (
                BreakingChangeType.FIELD_CHANGED_KIND,
                "Type1.field11 changed type from Int to [Int]!.",
            ),
            (
                BreakingChangeType.FIELD_CHANGED_KIND,
                "Type1.field13 changed type from [Int!] to [Int].",
            ),
            (
                BreakingChangeType.FIELD_CHANGED_KIND,
                "Type1.field14 changed type from [Int] to [[Int]].",
            ),
            (
                BreakingChangeType.FIELD_CHANGED_KIND,
                "Type1.field15 changed type from [[Int]] to [Int].",
            ),
            (
                BreakingChangeType.FIELD_CHANGED_KIND,
                "Type1.field16 changed type from Int! to [Int]!.",
            ),
            (
                BreakingChangeType.FIELD_CHANGED_KIND,
                "Type1.field18 changed type from [[Int!]!] to [[Int!]].",
            ),
        ]

    def should_detect_if_fields_on_input_types_changed_kind_or_were_removed():
        old_schema = build_schema(
            """
            input InputType1 {
              field1: String
              field2: Boolean
              field3: [String]
              field4: String!
              field5: String
              field6: [Int]
              field7: [Int]!
              field8: Int
              field9: [Int]
              field10: [Int!]
              field11: [Int]
              field12: [[Int]]
              field13: Int!
              field14: [[Int]!]
              field15: [[Int]!]
            }
            """
        )

        new_schema = build_schema(
            """
            input InputType1 {
              field1: Int
              field3: String
              field4: String
              field5: String!
              field6: [Int]!
              field7: [Int]
              field8: [Int]!
              field9: [Int!]
              field10: [Int]
              field11: [[Int]]
              field12: [Int]
              field13: [Int]!
              field14: [[Int]]
              field15: [[Int!]!]
            }
            """
        )

        assert find_breaking_changes(old_schema, new_schema) == [
            (
                BreakingChangeType.FIELD_CHANGED_KIND,
                "InputType1.field1 changed type from String to Int.",
            ),
            (BreakingChangeType.FIELD_REMOVED, "InputType1.field2 was removed."),
            (
                BreakingChangeType.FIELD_CHANGED_KIND,
                "InputType1.field3 changed type from [String] to String.",
            ),
            (
                BreakingChangeType.FIELD_CHANGED_KIND,
                "InputType1.field5 changed type from String to String!.",
            ),
            (
                BreakingChangeType.FIELD_CHANGED_KIND,
                "InputType1.field6 changed type from [Int] to [Int]!.",
            ),
            (
                BreakingChangeType.FIELD_CHANGED_KIND,
                "InputType1.field8 changed type from Int to [Int]!.",
            ),
            (
                BreakingChangeType.FIELD_CHANGED_KIND,
                "InputType1.field9 changed type from [Int] to [Int!].",
            ),
            (
                BreakingChangeType.FIELD_CHANGED_KIND,
                "InputType1.field11 changed type from [Int] to [[Int]].",
            ),
            (
                BreakingChangeType.FIELD_CHANGED_KIND,
                "InputType1.field12 changed type from [[Int]] to [Int].",
            ),
            (
                BreakingChangeType.FIELD_CHANGED_KIND,
                "InputType1.field13 changed type from Int! to [Int]!.",
            ),
            (
                BreakingChangeType.FIELD_CHANGED_KIND,
                "InputType1.field15 changed type from [[Int]!] to [[Int!]!].",
            ),
        ]

    def should_detect_if_a_required_field_is_added_to_an_input_type():
        old_schema = build_schema(
            """
            input InputType1 {
              field1: String
            }
            """
        )

        new_schema = build_schema(
            """
            input InputType1 {
                field1: String
                requiredField: Int!
                optionalField1: Boolean
                optionalField2: Boolean! = false
            }
            """
        )

        assert find_breaking_changes(old_schema, new_schema) == [
            (
                BreakingChangeType.REQUIRED_INPUT_FIELD_ADDED,
                "A required field requiredField on input type InputType1 was added.",
            )
        ]

    def should_detect_if_a_type_was_removed_from_a_union_type():
        old_schema = build_schema(
            """
            type Type1
            type Type2
            type Type3

            union UnionType1 = Type1 | Type2
            """
        )

        new_schema = build_schema(
            """
            type Type1
            type Type2
            type Type3

            union UnionType1 = Type1 | Type3
            """
        )

        assert find_breaking_changes(old_schema, new_schema) == [
            (
                BreakingChangeType.TYPE_REMOVED_FROM_UNION,
                "Type2 was removed from union type UnionType1.",
            )
        ]

    def should_detect_if_a_value_was_removed_from_an_enum_type():
        old_schema = build_schema(
            """
            enum EnumType1 {
              VALUE0
              VALUE1
              VALUE2
            }
            """
        )

        new_schema = build_schema(
            """
            enum EnumType1 {
              VALUE0
              VALUE2
              VALUE3
            }
            """
        )

        assert find_breaking_changes(old_schema, new_schema) == [
            (
                BreakingChangeType.VALUE_REMOVED_FROM_ENUM,
                "VALUE1 was removed from enum type EnumType1.",
            )
        ]

    def should_detect_if_a_field_argument_was_removed():
        old_schema = build_schema(
            """
            interface Interface1 {
              field1(arg1: Boolean, objectArg: String): String
            }

            type Type1 {
              field1(name: String): String
            }
            """
        )

        new_schema = build_schema(
            """
            interface Interface1 {
              field1: String
            }

            type Type1 {
              field1: String
            }
            """
        )

        assert find_breaking_changes(old_schema, new_schema) == [
            (BreakingChangeType.ARG_REMOVED, "Interface1.field1 arg arg1 was removed"),
            (
                BreakingChangeType.ARG_REMOVED,
                "Interface1.field1 arg objectArg was removed",
            ),
            (BreakingChangeType.ARG_REMOVED, "Type1.field1 arg name was removed"),
        ]

    def should_detect_if_a_field_argument_has_changed_type():
        old_schema = build_schema(
            """
            type Type1 {
              field1(
                arg1: String
                arg2: String
                arg3: [String]
                arg4: String
                arg5: String!
                arg6: String!
                arg7: [Int]!
                arg8: Int
                arg9: [Int]
                arg10: [Int!]
                arg11: [Int]
                arg12: [[Int]]
                arg13: Int!
                arg14: [[Int]!]
                arg15: [[Int]!]
              ): String
            }
            """
        )

        new_schema = build_schema(
            """
            type Type1 {
              field1(
                arg1: Int
                arg2: [String]
                arg3: String
                arg4: String!
                arg5: Int
                arg6: Int!
                arg7: [Int]
                arg8: [Int]!
                arg9: [Int!]
                arg10: [Int]
                arg11: [[Int]]
                arg12: [Int]
                arg13: [Int]!
                arg14: [[Int]]
                arg15: [[Int!]!]
               ): String
            }
            """
        )

        assert find_breaking_changes(old_schema, new_schema) == [
            (
                BreakingChangeType.ARG_CHANGED_KIND,
                "Type1.field1 arg arg1 has changed type from String to Int",
            ),
            (
                BreakingChangeType.ARG_CHANGED_KIND,
                "Type1.field1 arg arg2 has changed type from String to [String]",
            ),
            (
                BreakingChangeType.ARG_CHANGED_KIND,
                "Type1.field1 arg arg3 has changed type from [String] to String",
            ),
            (
                BreakingChangeType.ARG_CHANGED_KIND,
                "Type1.field1 arg arg4 has changed type from String to String!",
            ),
            (
                BreakingChangeType.ARG_CHANGED_KIND,
                "Type1.field1 arg arg5 has changed type from String! to Int",
            ),
            (
                BreakingChangeType.ARG_CHANGED_KIND,
                "Type1.field1 arg arg6 has changed type from String! to Int!",
            ),
            (
                BreakingChangeType.ARG_CHANGED_KIND,
                "Type1.field1 arg arg8 has changed type from Int to [Int]!",
            ),
            (
                BreakingChangeType.ARG_CHANGED_KIND,
                "Type1.field1 arg arg9 has changed type from [Int] to [Int!]",
            ),
            (
                BreakingChangeType.ARG_CHANGED_KIND,
                "Type1.field1 arg arg11 has changed type from [Int] to [[Int]]",
            ),
            (
                BreakingChangeType.ARG_CHANGED_KIND,
                "Type1.field1 arg arg12 has changed type from [[Int]] to [Int]",
            ),
            (
                BreakingChangeType.ARG_CHANGED_KIND,
                "Type1.field1 arg arg13 has changed type from Int! to [Int]!",
            ),
            (
                BreakingChangeType.ARG_CHANGED_KIND,
                "Type1.field1 arg arg15 has changed type from [[Int]!] to [[Int!]!]",
            ),
        ]

    def should_detect_if_a_required_field_argument_was_added():
        old_schema = build_schema(
            """
            type Type1 {
              field1(arg1: String): String
            }
            """
        )

        new_schema = build_schema(
            """
            type Type1 {
              field1(
                arg1: String,
                newRequiredArg: String!
                newOptionalArg1: Int
                newOptionalArg2: Int! = 0
              ): String
            }
            """
        )

        assert find_breaking_changes(old_schema, new_schema) == [
            (
                BreakingChangeType.REQUIRED_ARG_ADDED,
                "A required arg newRequiredArg on Type1.field1 was added",
            )
        ]

    def should_not_flag_args_with_the_same_type_signature_as_breaking():
        old_schema = build_schema(
            """
            input InputType1 {
              field1: String
            }

            type Type1 {
              field1(arg1: Int!, arg2: InputType1): Int
            }
            """
        )

        new_schema = build_schema(
            """
            input InputType1 {
              field1: String
            }

            type Type1 {
              field1(arg1: Int!, arg2: InputType1): Int
            }
            """
        )

        assert find_breaking_changes(old_schema, new_schema) == []

    def should_consider_args_that_move_away_from_non_null_as_non_breaking():
        old_schema = build_schema(
            """
            type Type1 {
              field1(name: String!): String
            }
            """
        )

        new_schema = build_schema(
            """
            type Type1 {
              field1(name: String): String
            }
            """
        )

        assert find_breaking_changes(old_schema, new_schema) == []

    def should_detect_interfaces_removed_from_types():
        old_schema = build_schema(
            """
            interface Interface1

            type Type1 implements Interface1
            """
        )

        new_schema = build_schema(
            """
            interface Interface1

            type Type1
            """
        )

        assert find_breaking_changes(old_schema, new_schema) == [
            (
                BreakingChangeType.INTERFACE_REMOVED_FROM_OBJECT,
                "Type1 no longer implements interface Interface1.",
            )
        ]

    def should_detect_all_breaking_changes():
        old_schema = build_schema(
            """
            directive @DirectiveThatIsRemoved on FIELD_DEFINITION

            directive @DirectiveThatRemovesArg(arg1: String) on FIELD_DEFINITION

            directive @NonNullDirectiveAdded on FIELD_DEFINITION

            directive @DirectiveName on FIELD_DEFINITION | QUERY

            type ArgThatChanges {
                field1(id: Int): String
            }

            enum EnumTypeThatLosesAValue {
                VALUE0
                VALUE1
                VALUE2
            }

            interface Interface1
            type TypeThatLoosesInterface1 implements Interface1

            type TypeInUnion1
            type TypeInUnion2
            union UnionTypeThatLosesAType = TypeInUnion1 | TypeInUnion2

            type TypeThatChangesType

            type TypeThatGetsRemoved

            interface TypeThatHasBreakingFieldChanges {
                field1: String
                field2: String
            }
            """
        )

        new_schema = build_schema(
            """
            directive @DirectiveThatRemovesArg on FIELD_DEFINITION

            directive @NonNullDirectiveAdded(arg1: Boolean!) on FIELD_DEFINITION

            directive @DirectiveName on FIELD_DEFINITION

            type ArgThatChanges {
              field1(id: String): String
            }

            enum EnumTypeThatLosesAValue {
              VALUE1
              VALUE2
            }

            interface Interface1
            type TypeThatLoosesInterface1

            type TypeInUnion1
            type TypeInUnion2

            union UnionTypeThatLosesAType = TypeInUnion1

            interface TypeThatChangesType

            interface TypeThatHasBreakingFieldChanges {
              field2: Boolean
            }
            """
        )

        assert find_breaking_changes(old_schema, new_schema) == [
            (BreakingChangeType.TYPE_REMOVED, "Int was removed."),
            (BreakingChangeType.TYPE_REMOVED, "TypeThatGetsRemoved was removed."),
            (
                BreakingChangeType.TYPE_CHANGED_KIND,
                "TypeThatChangesType changed from an Object type to an"
                " Interface type.",
            ),
            (
                BreakingChangeType.FIELD_REMOVED,
                "TypeThatHasBreakingFieldChanges.field1 was removed.",
            ),
            (
                BreakingChangeType.FIELD_CHANGED_KIND,
                "TypeThatHasBreakingFieldChanges.field2 changed type"
                " from String to Boolean.",
            ),
            (
                BreakingChangeType.TYPE_REMOVED_FROM_UNION,
                "TypeInUnion2 was removed from union type UnionTypeThatLosesAType.",
            ),
            (
                BreakingChangeType.VALUE_REMOVED_FROM_ENUM,
                "VALUE0 was removed from enum type EnumTypeThatLosesAValue.",
            ),
            (
                BreakingChangeType.ARG_CHANGED_KIND,
                "ArgThatChanges.field1 arg id has changed type from Int to String",
            ),
            (
                BreakingChangeType.INTERFACE_REMOVED_FROM_OBJECT,
                "TypeThatLoosesInterface1 no longer implements interface Interface1.",
            ),
            (
                BreakingChangeType.DIRECTIVE_REMOVED,
                "DirectiveThatIsRemoved was removed",
            ),
            (
                BreakingChangeType.DIRECTIVE_ARG_REMOVED,
                "arg1 was removed from DirectiveThatRemovesArg",
            ),
            (
                BreakingChangeType.REQUIRED_DIRECTIVE_ARG_ADDED,
                "A required arg arg1 on directive NonNullDirectiveAdded was added",
            ),
            (
                BreakingChangeType.DIRECTIVE_LOCATION_REMOVED,
                "QUERY was removed from DirectiveName",
            ),
        ]

    def should_detect_if_a_directive_was_explicitly_removed():
        old_schema = build_schema(
            """
            directive @DirectiveThatIsRemoved on FIELD_DEFINITION
            directive @DirectiveThatStays on FIELD_DEFINITION
            """
        )

        new_schema = build_schema(
            """
            directive @DirectiveThatStays on FIELD_DEFINITION
            """
        )

        assert find_breaking_changes(old_schema, new_schema) == [
            (BreakingChangeType.DIRECTIVE_REMOVED, "DirectiveThatIsRemoved was removed")
        ]

    def should_detect_if_a_directive_was_implicitly_removed():
        old_schema = GraphQLSchema()

        new_schema = GraphQLSchema(
            directives=[GraphQLSkipDirective, GraphQLIncludeDirective]
        )

        assert find_breaking_changes(old_schema, new_schema) == [
            (
                BreakingChangeType.DIRECTIVE_REMOVED,
                f"{GraphQLDeprecatedDirective.name} was removed",
            )
        ]

    def should_detect_if_a_directive_argument_was_removed():
        old_schema = build_schema(
            """
            directive @DirectiveWithArg(arg1: String) on FIELD_DEFINITION
            """
        )

        new_schema = build_schema(
            """
            directive @DirectiveWithArg on FIELD_DEFINITION
            """
        )

        assert find_breaking_changes(old_schema, new_schema) == [
            (
                BreakingChangeType.DIRECTIVE_ARG_REMOVED,
                "arg1 was removed from DirectiveWithArg",
            )
        ]

    def should_detect_if_an_optional_directive_argument_was_added():
        old_schema = build_schema(
            """
            directive @DirectiveName on FIELD_DEFINITION
            """
        )

        new_schema = build_schema(
            """
            directive @DirectiveName(
              newRequiredArg: String!
              newOptionalArg1: Int
              newOptionalArg2: Int! = 0
            ) on FIELD_DEFINITION
            """
        )

        assert find_breaking_changes(old_schema, new_schema) == [
            (
                BreakingChangeType.REQUIRED_DIRECTIVE_ARG_ADDED,
                "A required arg newRequiredArg on directive DirectiveName was added",
            )
        ]

    def should_detect_locations_removed_from_a_directive():
        old_schema = build_schema(
            """
            directive @DirectiveName on FIELD_DEFINITION | QUERY
            """
        )

        new_schema = build_schema(
            """
            directive @DirectiveName on FIELD_DEFINITION
            """
        )

        assert find_breaking_changes(old_schema, new_schema) == [
            (
                BreakingChangeType.DIRECTIVE_LOCATION_REMOVED,
                "QUERY was removed from DirectiveName",
            )
        ]


def describe_find_dangerous_changes():
    def should_detect_if_an_arguments_default_value_has_changed():
        old_schema = build_schema(
            """
            type Type1 {
              field1(name: String = "test"): String
            }
            """
        )

        new_schema = build_schema(
            """
            type Type1 {
              field1(name: String = "Test"): String
            }
            """
        )

        assert find_dangerous_changes(old_schema, new_schema) == [
            (
                DangerousChangeType.ARG_DEFAULT_VALUE_CHANGE,
                "Type1.field1 arg name has changed defaultValue",
            )
        ]

    def should_detect_if_a_value_was_added_to_an_enum_type():
        old_schema = build_schema(
            """
            enum EnumType1 {
              VALUE0
              VALUE1
            }
            """
        )

        new_schema = build_schema(
            """
            enum EnumType1 {
              VALUE0
              VALUE1
              VALUE2
            }
            """
        )

        assert find_dangerous_changes(old_schema, new_schema) == [
            (
                DangerousChangeType.VALUE_ADDED_TO_ENUM,
                "VALUE2 was added to enum type EnumType1.",
            )
        ]

    def should_detect_interfaces_added_to_types():
        old_schema = build_schema(
            """
            type Type1
            """
        )

        new_schema = build_schema(
            """
            interface Interface1

            type Type1 implements Interface1
            """
        )

        assert find_dangerous_changes(old_schema, new_schema) == [
            (
                DangerousChangeType.INTERFACE_ADDED_TO_OBJECT,
                "Interface1 added to interfaces implemented by Type1.",
            )
        ]

    def should_detect_if_a_type_was_added_to_a_union_type():
        old_schema = build_schema(
            """
            type Type1
            type Type2

            union UnionType1 = Type1
            """
        )

        new_schema = build_schema(
            """
            type Type1
            type Type2

            union UnionType1 = Type1 | Type2
            """
        )

        assert find_dangerous_changes(old_schema, new_schema) == [
            (
                DangerousChangeType.TYPE_ADDED_TO_UNION,
                "Type2 was added to union type UnionType1.",
            )
        ]

    def should_detect_if_an_optional_field_was_added_to_an_input():
        old_schema = build_schema(
            """
            input InputType1 {
                field1: String
            }
            """
        )

        new_schema = build_schema(
            """
            input InputType1 {
              field1: String
              field2: Int
            }
            """
        )

        assert find_dangerous_changes(old_schema, new_schema) == [
            (
                DangerousChangeType.OPTIONAL_INPUT_FIELD_ADDED,
                "An optional field field2 on input type InputType1 was added.",
            )
        ]

    def should_find_all_dangerous_changes():
        old_schema = build_schema(
            """
            enum EnumType1 {
              VALUE0
              VALUE1
            }

            type Type1 {
              field1(argThatChangesDefaultValue: String = "test"): String
            }

            interface Interface1
            type TypeThatGainsInterface1

            type TypeInUnion1
            union UnionTypeThatGainsAType = TypeInUnion1
            """
        )

        new_schema = build_schema(
            """
            enum EnumType1 {
              VALUE0
              VALUE1
              VALUE2
            }

            type Type1 {
              field1(argThatChangesDefaultValue: String = "Test"): String
            }

            interface Interface1
            type TypeThatGainsInterface1 implements Interface1

            type TypeInUnion1
            type TypeInUnion2
            union UnionTypeThatGainsAType = TypeInUnion1 | TypeInUnion2
            """
        )

        assert find_dangerous_changes(old_schema, new_schema) == [
            (
                DangerousChangeType.ARG_DEFAULT_VALUE_CHANGE,
                "Type1.field1 arg argThatChangesDefaultValue has changed defaultValue",
            ),
            (
                DangerousChangeType.VALUE_ADDED_TO_ENUM,
                "VALUE2 was added to enum type EnumType1.",
            ),
            (
                DangerousChangeType.INTERFACE_ADDED_TO_OBJECT,
                "Interface1 added to interfaces implemented"
                " by TypeThatGainsInterface1.",
            ),
            (
                DangerousChangeType.TYPE_ADDED_TO_UNION,
                "TypeInUnion2 was added to union type UnionTypeThatGainsAType.",
            ),
        ]

    def should_detect_if_an_optional_field_argument_was_added():
        old_schema = build_schema(
            """
            type Type1 {
              field1(arg1: String): String
            }
            """
        )

        new_schema = build_schema(
            """
            type Type1 {
              field1(arg1: String, arg2: String): String
            }
            """
        )

        assert find_dangerous_changes(old_schema, new_schema) == [
            (
                DangerousChangeType.OPTIONAL_ARG_ADDED,
                "An optional arg arg2 on Type1.field1 was added",
            )
        ]
