"""
Test langkit's new concrete syntax parser.

RA22-015: This is a temporary test, we'll get rid of it when tests are ported
to the new syntax.
"""

from __future__ import absolute_import, division, print_function

import os
from os import path as P
import subprocess
import sys


LK_LIB_DIR = P.join(os.environ['LANGKIT_ROOT_DIR'], 'contrib', 'lkt')
TESTS_DIR = P.join(os.environ['LANGKIT_ROOT_DIR'], 'testsuite', 'tests')

o = subprocess.check_output(
    [sys.executable, P.join(LK_LIB_DIR, 'manage.py'), 'make', '-P'],
    # CWD is the lib's directory so that lib is generated in the lib's dir, not
    # in the test dir.
    cwd=LK_LIB_DIR
)

tests = sorted(((P.join(root, f), P.basename(root))
                for root, _, files in os.walk(TESTS_DIR)
                for f in files
                if f == 'expected_concrete_syntax.lkt'), key=lambda x: x[1])

# TODO: for the moment we'll use a whitelist for tests, eventually we want to
# parse them all.
test_whitelist = {
    'abstract_fields', 'add_to_env_foreign', 'add_to_env_mult_dests',
    'analysis_unit', 'analysis_unit_from_node', 'array_types',
    'auto_ple_dispatcher', 'auto_populate', 'bare_lexing',
    'c_text_to_locale_string', 'can_reach', 'categories', 'character',
    'custom_parsing_rule', 'dflt_arg_val', 'dflt_arg_val_predicate',
    'domain_derived', 'dynvar_bind', 'dynvars_dflt', 'early_binding_error',
    'entity_bind', 'entity_bind_2', 'entity_bind_3', 'entity_cast',
    'entity_eq', 'entity_field_access', 'entity_length', 'entity_map',
    'entity_match', 'entity_resolver', 'enum_node_inherit', 'enum_types',
    'env_get_all', 'exposed_bare_nodes', 'external', 'field_introspection',
    'foreign_env_md', 'full_sloc_image', 'ghost_nodes', 'hashes',
    'import_argcount', 'indent_trivia', 'is_a', 'let_underscore', 'lifetimes',
    'logging', 'lookup_token', 'lower_dispatch', 'lower_dispatch_rewrite',
    'map_index', 'match', 'memoized_big_table', 'memoized_env',
    'memoized_inf_recurs', 'memoized_property_array_arg', 'memoized_unit',
    'memoized_unit_loading', 'neq', 'new_node', 'newline', 'node_comparison',
    'node_conversion', 'node_env_concrete_subclass', 'node_env_empty',
    'node_negative_index', 'node_none_check', 'node_type_introspection',
    'null_list_get', 'ple_after_reparse', 'ple_resilience', 'ple_resilience_2',
    'ple_subunits', 'ple_subunits_2', 'populate_error', 'pred_kind_in',
    'private_predicate_props', 'properties_introspection', 'public',
    'qualifier_sloc_range', 'rebindings', 'ref_after_reparse', 'rewriting',
    'siblings', 'stack_overflow', 'struct_update', 'symbol_type',
    'synthetic_props', 'tokens', 'top_level_predicate', 'trailing_garbage',
    'unbounded_string_buffer', 'unicode_buffer', 'unit_canon', 'unit_filename',
    'unparse_empty_list', 'unparse_no_canon', 'unparse_or_skip',
    'wrapper_caches'
}

whitelisted_tests = [t for t in tests if t[1] in test_whitelist]

for full_syntax_path, test_name in whitelisted_tests:
    header = 'Parsing concrete syntax for test {}'.format(test_name)
    print("{}\n{}\n".format(header, "=" * len(header)))
    sys.stdout.flush()
    subprocess.check_call(
        [P.join(LK_LIB_DIR, 'build', 'bin', 'parse'), "-f",
         full_syntax_path]
    )
    print()