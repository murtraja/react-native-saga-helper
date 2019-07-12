import sys;

ACTION_TYPE_SUCCESS = "Success";
ACTION_TYPE_ACTION = "Action"

ONE_TAB_SPACE = '  ';

OUTPUT_DELIMITERS = "\n\n============{}============";

ACTION_TYPE_TEMPLATE='''export const {} = '{}';'''

ACTION_CREATOR_TEMPLATE='''export const {} = (params) => ({{
<TAB>type: {},
<TAB>params,
}});
'''.replace('<TAB>', ONE_TAB_SPACE)

SUCCESS_ACTION_CREATOR_TEMPLATE='''export const {0} = ({2}) => ({{
<TAB>type: {1},
<TAB>{2},
}});
'''.replace('<TAB>', ONE_TAB_SPACE)

REDUCER_INITIAL_STATE_TEMPLATE='''<TAB>{0}: [],'''.replace('<TAB>', ONE_TAB_SPACE)

REDUCER_ACTION_TEMPLATE='''<TAB><TAB>case {}:
<TAB><TAB>return {{
<TAB><TAB><TAB>...state,
<TAB><TAB>}}'''.replace('<TAB>', ONE_TAB_SPACE)

REDUCER_SUCCESS_TEMPLATE='''<TAB><TAB>case {0}:
<TAB><TAB>return {{
<TAB><TAB><TAB>...state,
<TAB><TAB><TAB>{1}: action.{1},
<TAB><TAB>}}
'''.replace('<TAB>', ONE_TAB_SPACE);

SAGA_TEMPLATE='''export function* {0}(action) {{
<TAB>try {{
<TAB><TAB>
<TAB><TAB>if (response) {{
<TAB><TAB><TAB>yield put({1}(response));
<TAB><TAB>}} else {{
<TAB><TAB><TAB>yield put(errorActionSet(error));
<TAB><TAB>}}
<TAB>}} catch (error) {{
<TAB><TAB>yield put(errorActionSet(error));
<TAB>}}
}}
'''.replace('<TAB>', ONE_TAB_SPACE)

REPO_TEMPLATE = '''<TAB>{0} = (params = {{}}) => {{
<TAB><TAB>const queryParams = {{
<TAB><TAB><TAB>...params
<TAB><TAB>}}
<TAB><TAB>return this.resource.list(queryParams, false);
<TAB>}}
'''.replace('<TAB>', ONE_TAB_SPACE)

TAKE_SAGA_TEMPLATE= ONE_TAB_SPACE + '''takeEvery({}, {}),'''

def get_action_type_name(action_name, action_type):
    action_type_name = action_name + '_' + action_type.upper();
    return action_type_name;

def get_action_response_name(action_name):
    capitalize_action_name = [x.capitalize() for x in action_name.split('_')]
    return 'response'+''.join(capitalize_action_name)

def get_action_type_declaration(action_name, action_type):
    action_type_name = get_action_type_name(action_name, action_type)
    return ACTION_TYPE_TEMPLATE.format(action_type_name, action_type_name);

def get_camel_case_action_name(action_name, capitalize_first_letter=False):
    split_action_name = action_name.split('_')
    camel_cased_action_name = [x.lower().capitalize() for x in split_action_name]
    if capitalize_first_letter:
        return ''.join(camel_cased_action_name)
    
    first_word = camel_cased_action_name[0]
    first_word = first_word[0].lower() + first_word[1:]
    camel_cased_action_name[0] = first_word
    return ''.join(camel_cased_action_name)

def get_action_creator_name(action_name, action_type):
    action_type_name = get_action_type_name(action_name, action_type)
    split_action_name = action_name.split('_') + [action_type.upper()];
    camel_cased_action_name = [x.lower().capitalize() for x in split_action_name]
    first_word = camel_cased_action_name[0]
    first_word = first_word[0].lower() + first_word[1:]
    camel_cased_action_name[0] = first_word
    creator_name = ''.join(camel_cased_action_name)
    # print("computed action_creator_name as {}".format(creator_name))
    return ACTION_CREATOR_TEMPLATE.format(creator_name, action_type_name);

def get_success_action_creator_name(action_name):
    action_type_name = get_action_type_name(action_name, ACTION_TYPE_SUCCESS);
    action_camel_case = get_camel_case_action_name(action_name, False);
    creator_name = action_camel_case + ACTION_TYPE_SUCCESS.lower().capitalize()
    action_response_name = get_action_response_name(action_name);

    return SUCCESS_ACTION_CREATOR_TEMPLATE.format(creator_name, action_type_name, action_response_name)

def get_reducer_action(action_name):
    action_action_name = get_action_type_name(action_name, ACTION_TYPE_ACTION);
    return REDUCER_ACTION_TEMPLATE.format(action_action_name);

def get_reducer_success(action_name):
    action_success_name = get_action_type_name(action_name, ACTION_TYPE_SUCCESS);
    action_response_name = get_action_response_name(action_name);
    # print(action_response_name)
    return REDUCER_SUCCESS_TEMPLATE.format(action_success_name, action_response_name)

def get_saga(action_name):
    saga_name = get_camel_case_action_name(action_name, False)
    success_action_creator_name = saga_name + ACTION_TYPE_SUCCESS.lower().capitalize()
    return SAGA_TEMPLATE.format(saga_name, success_action_creator_name);

def get_reducer_imports(action_name):
    action_action_name = get_action_type_name(action_name, ACTION_TYPE_ACTION);
    action_success_name = get_action_type_name(action_name, ACTION_TYPE_SUCCESS);
    return ONE_TAB_SPACE + "{}, {},".format(action_action_name, action_success_name)

def get_reducer_initial_state(action_name):
    action_response_name = get_action_response_name(action_name)
    return REDUCER_INITIAL_STATE_TEMPLATE.format(action_response_name);

def get_saga_imports(action_name):
    action_action_name = get_action_type_name(action_name, ACTION_TYPE_ACTION);
    action_creator_success_name = get_camel_case_action_name(action_name) + ACTION_TYPE_SUCCESS.lower().capitalize()
    return ONE_TAB_SPACE + "{}, {},".format(action_action_name, action_creator_success_name);

def get_take_saga(action_name):
    saga_name = get_camel_case_action_name(action_name);
    action_action_name = get_action_type_name(action_name, ACTION_TYPE_ACTION);
    return TAKE_SAGA_TEMPLATE.format(action_action_name, saga_name)
    
def get_repo_method(action_name):
    repo_name = get_camel_case_action_name(action_name);
    return REPO_TEMPLATE.format(repo_name);

def print_output_delimiter(delimiter):
    print(OUTPUT_DELIMITERS.format(delimiter));

def main(action_names):
    print("Now generating helpers with {}\n\n".format(", ".join(action_names)))

    print_output_delimiter('ACTIONS')
    for action_name in action_names:
        declaration_action = get_action_type_declaration(action_name, ACTION_TYPE_ACTION)
        declaration_success = get_action_type_declaration(action_name, ACTION_TYPE_SUCCESS)
        print(declaration_action)
        print(declaration_success)
        print('')

    for action_name in action_names:
        creator_action = get_action_creator_name(action_name, ACTION_TYPE_ACTION)
        creator_success = get_success_action_creator_name(action_name)
        print(creator_action)
        print(creator_success)

    print_output_delimiter('REDUCERS')
    for action_name in action_names:
        reducer_imports = get_reducer_imports(action_name);
        print(reducer_imports);
        
    print('');

    for action_name in action_names:
        reducer_initial_state = get_reducer_initial_state(action_name);
        print(reducer_initial_state);
    
    print('');
    
    for action_name in action_names:
        reducer_action = get_reducer_action(action_name);
        reducer_success = get_reducer_success(action_name);
        print(reducer_action);
        print(reducer_success);

    print_output_delimiter('SAGA')
    for action_name in action_names:
        saga_imports = get_saga_imports(action_name);
        print(saga_imports);

    print('')

    for action_name in action_names:
        saga = get_saga(action_name);
        print(saga);

    for action_name in action_names:
        take_saga = get_take_saga(action_name);
        print(take_saga);
    
    print('')

    for action_name in action_names:
        repo_method = get_repo_method(action_name);
        print(repo_method);


if  __name__ == "__main__":
    args_length = len(sys.argv)
    if args_length < 2:
        print("Usage: {} <ACTION_NAME>".format(sys.argv[0]));
        sys.exit();
    action_names = sys.argv[1:];
    main(action_names)