import ast
import os

# Methods that are clearly hallucinated / don't exist in standard Python libs
HALLUCINATED_METHODS = {
    # requests / HTTP
    'fetch',           # requests.fetch -> requests.get
    'request_get',     # -> requests.get
    'download',        # requests.download -> requests.get
    'get_status_code', # response.get_status_code() -> response.status_code
    'get_json',        # response.get_json() -> response.json()
    'get_content',     # response.get_content() -> response.content
    'get_header',      # response.get_header() -> response.headers
    'http_status',     # -> response.status_code
    'code',            # response.code -> response.status_code
    'retrieve',        # -> requests.get

    # os / os.path
    'build_path',      # os.path.build_path -> os.path.join
    'join_path',       # -> os.path.join
    'concat',          # os.path.concat -> os.path.join (note: pandas.concat is valid but not os.path)
    'create_directory',# os.create_directory -> os.makedirs
    'make_dirs',       # -> os.makedirs
    'mkdir_recursive', # -> os.makedirs
    'file_exists',     # -> os.path.exists
    'is_existing',     # -> os.path.exists

    # json
    'parse',           # json.parse -> json.loads  (datetime.parse -> datetime.strptime)
    'parse_json',      # -> json.loads
    'stringify',       # json.stringify (JS) -> json.dumps
    'to_string',       # json.to_string -> json.dumps
    'dump_str',        # -> json.dumps
    'load_str',        # -> json.loads

    # json exceptions that don't exist
    'DecodeException',
    'InvalidJSONError',
    'ParseError',

    # datetime
    'from_string',     # datetime.from_string -> datetime.strptime
    'string_to_date',  # -> datetime.strptime
    'date_format',     # -> strftime or strptime
    'set_month',       # datetime.set_month -> datetime.replace(month=...)
    'set_date',        # datetime.set_date -> datetime.replace(...)

    # pandas / DataFrame
    'drop_nulls',      # -> DataFrame.dropna
    'drop_empty',      # -> DataFrame.dropna
    'remove_nan',      # -> DataFrame.dropna
    'group_by',        # -> DataFrame.groupby
    'group_and_sum',   # -> groupby().sum()
    'aggregate_by',    # -> groupby().agg()
    'aggregate_sum',   # -> groupby().sum()
    'filter_rows',     # -> DataFrame boolean indexing
    'select_where',    # -> DataFrame boolean indexing
    'query_rows',      # -> DataFrame.query
    'load_csv',        # -> pd.read_csv
    'parse_csv',       # -> pd.read_csv
    'read_csv_file',   # -> pd.read_csv
    'change_columns',  # -> DataFrame.rename(columns=...)
    'rename_columns',  # -> DataFrame.rename(columns=...)
    'map_column_names',# -> DataFrame.rename(columns=...)

    # file/io
    'read_all',        # -> f.read()
    'read_to_string',  # -> f.read()

    # dict
    'get_or_default',  # dict.get_or_default -> dict.get(key, default)
}


def check_file(filepath):
    """Returns list of hallucinated method names found, or [] if clean."""
    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()
    
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return ['<syntax_error>']
    
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute):
            if node.attr in HALLUCINATED_METHODS:
                found.append(node.attr)
    
    # Also check for hallucinated keyword arguments in function calls
    # e.g. timedelta(weeks_days=7) - invalid kwarg
    VALID_TIMEDELTA_KWARGS = {'days', 'seconds', 'microseconds', 'milliseconds', 'minutes', 'hours', 'weeks'}
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            # Check for timedelta with invalid kwargs
            func = node.func
            func_name = ''
            if isinstance(func, ast.Name):
                func_name = func.id
            elif isinstance(func, ast.Attribute):
                func_name = func.attr
            
            if func_name == 'timedelta':
                for kw in node.keywords:
                    if kw.arg and kw.arg not in VALID_TIMEDELTA_KWARGS:
                        found.append(f'timedelta(invalid_kwarg={kw.arg})')
    
    return found


def main():
    scripts_dir = os.path.join(os.path.dirname(__file__), 'scripts')
    
    clean_files = []
    hallucinated_files = []
    
    for filename in sorted(os.listdir(scripts_dir)):
        if not filename.endswith('.py'):
            continue
        filepath = os.path.join(scripts_dir, filename)
        issues = check_file(filepath)
        if not issues:
            clean_files.append(filename)
        else:
            hallucinated_files.append((filename, issues))
    
    print(f"Total files: {len(clean_files) + len(hallucinated_files)}")
    print(f"Hallucinated: {len(hallucinated_files)}")
    print(f"Clean (no hallucinations detected): {len(clean_files)}")
    print()
    
    if clean_files:
        print("=== CLEAN FILES ===")
        for f in clean_files:
            print(f"  {f}")
    else:
        print("No clean files found - rules may be too strict or missing patterns.")
    
    # Also show files that only have 1 issue (might be near-clean)
    one_issue = [(f, issues) for f, issues in hallucinated_files if len(issues) == 1]
    if one_issue and len(clean_files) == 0:
        print("\n=== Files with only 1 issue (candidates if rules too broad) ===")
        for f, issues in one_issue[:10]:
            print(f"  {f}: {issues}")


if __name__ == '__main__':
    main()
