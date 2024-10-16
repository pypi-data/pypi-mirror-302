import pandas as pd
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext


def get_list_view_test(username, password, sharepoint_site, list_name, view_name="All Items"):    
    # Authenticate and create a ClientContext
    ctx_auth = AuthenticationContext(url=sharepoint_site)
    ctx_auth.acquire_token_for_user(username, password)
    ctx = ClientContext(sharepoint_site, ctx_auth)

    tasks_list = ctx.web.lists.get_by_title(list_name)

    # Retrieve all list items
    items = tasks_list.items.get_all()
    ctx.load(items)
    ctx.execute_query()

    # Create a list to store item data
    item_data = []
    col_data = []
    name = ['Title', 'title', 'Linktitle', 'LinkTitle', "Caller_x0020_NameId"]
    # Iterate over the items and append their field values to the list
    for item in items:
        item_fields = {field_name: item.properties[field_name] for field_name in item.properties}
        col_fields = {field_name: item.properties[field_name] for field_name in item.properties if field_name in name}
        item_data.append(item_fields)
        col_data.append(col_fields)

    # Create a DataFrame from the item data
    df = pd.DataFrame(item_data)

    # Rename columns to show only columns visable in the sharepoint list
    fields = tasks_list.fields.get().execute_query()
    field_mapping = {field.internal_name: field.title for field in fields}
    view = tasks_list.views.get_by_title(view_name)
    view_fields = view.view_fields.get().execute_query()

    visible_fields = {field: field_mapping[field] for field in view_fields if field_mapping.get(field)}
    visible_fields = {k: v for k, v in visible_fields.items() if k in df.columns}

    df.rename(columns=visible_fields, inplace=True)
    df = df[list(visible_fields.values())]
    df2 = pd.DataFrame(col_data)
    if "Caller_x0020_NameId" in df2.columns:
        df2 = df2.rename(columns = {"Caller_x0020_NameId": "Caller Name ID" })
    return pd.merge(df2, df, left_index=True, right_index=True, how='outer')


