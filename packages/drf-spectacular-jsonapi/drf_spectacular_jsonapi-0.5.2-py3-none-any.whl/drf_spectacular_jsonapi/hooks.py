import re
from warnings import warn

from django.urls import Resolver404, resolve
from rest_framework_extensions.settings import extensions_api_settings
from rest_framework_json_api.utils import get_resource_name


def fix_nested_path_parameters(endpoints):
    # If drf-extension package is used and there are nested routes, by default
    # the api paths will shown as /users/{parent_lookup_user_groups}/groups/ for example,
    # where `user_groups` will always be the lookup name of the django foreign key.

    # for json:api it would be better to change it to /users/{UserId}/groups/ (`ResourceType`Id)
    # then an openapi client can combine the parent resource type `User` by it self.
    # Otherwise it would not be possible for the client to determine the path parameter name on the fly...
    # thats why we patch it here for the schema reperesentation.
    fixed_enpoints = []
    for (path, path_regex, method, callback) in endpoints:
        if extensions_api_settings.DEFAULT_PARENT_LOOKUP_KWARG_NAME_PREFIX in path:
            nested_lookups = re.findall(
                r"(?<=\{)(parent_lookup.*)(?=\})", path)

            new_path = path
            for lookup in nested_lookups:
                parent_path = path.split(lookup)[0].replace('{', '')
                # fix trailing slashes setting
                if parent_path.endswith("/") and not path.endswith("/"):
                    parent_path = parent_path[:-1]

                try:
                    match = resolve(parent_path)
                    func = match.func
                    if hasattr(func, "cls"):
                        func = func.cls(action='list')

                        new_path = new_path.replace(
                            lookup, f"{get_resource_name(context={'view': func})}Id")

                except Resolver404:
                    warn(
                        message=f"Can't find path {parent_path} to fix nested path parameters")

            fixed_enpoints.append((new_path, path_regex, method, callback))
        else:
            fixed_enpoints.append((path, path_regex, method, callback))

    return fixed_enpoints
