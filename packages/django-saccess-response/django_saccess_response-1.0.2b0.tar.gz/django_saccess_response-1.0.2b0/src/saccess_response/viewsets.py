from rest_framework.viewsets import ViewSetMixin
from .mixins import (
    SaccessCreateModelMixin,
    SaccessListModelMixin,
    SaccessRetrieveModelMixin,
    SaccessUpdateModelMixin,
    SaccessDestroyModelMixin
)


# This viewset provides read-only actions (list and retrieve) for the model.
# It limits HTTP methods to GET, HEAD, and OPTIONS, making it suitable for
# endpoints where data should only be viewed, not modified.
class SaccessReadOnlyModelViewSet(SaccessListModelMixin, SaccessRetrieveModelMixin, ViewSetMixin):
    http_method_names = ['get', 'head', 'options']


# This viewset provides full CRUD (Create, Retrieve, Update, Delete) operations for the model.
# It allows multiple HTTP methods (GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS),
# enabling both data retrieval and modifications.
class SaccessModelViewSet(
    SaccessListModelMixin,
    SaccessCreateModelMixin,
    SaccessRetrieveModelMixin,
    SaccessUpdateModelMixin,
    SaccessDestroyModelMixin,
    ViewSetMixin
):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']
