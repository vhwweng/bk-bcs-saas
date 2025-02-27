# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://opensource.org/licenses/MIT

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
from typing import Dict, List, Optional, Type

import attr

from backend.iam.permissions import decorators
from backend.iam.permissions.exceptions import AttrValidationError
from backend.iam.permissions.perm import PermCtx, Permission
from backend.iam.permissions.request import IAMResource, ResourceRequest
from backend.packages.blue_krill.data_types.enum import EnumField, StructuredEnum

from .cluster import ClusterPermission, related_cluster_perm
from .constants import ResourceType


def calc_iam_ns_id(cluster_id: str, name: Optional[str] = None, max_length: int = 32) -> Optional[str]:
    """
    计算出注册到权限中心的命名空间ID，具备唯一性.
    TODO 下一个 PR 中实现，方便 review
    """
    return "default"


class NamespaceAction(str, StructuredEnum):
    CREATE = EnumField('namespace_create', label='namespace_create')
    VIEW = EnumField('namespace_view', label='namespace_view')
    UPDATE = EnumField('namespace_update', label='namespace_update')
    DELETE = EnumField('namespace_delete', label='namespace_delete')
    USE = EnumField('namespace_use', label='namespace_use')


@attr.dataclass
class NamespacePermCtx(PermCtx):
    project_id: str = ''
    cluster_id: str = ''
    name: Optional[str] = None  # 命名空间名
    iam_ns_id: Optional[str] = None  # 注册到权限中心的命名空间ID

    def __attrs_post_init__(self):
        """权限中心的 resource_id 长度限制为32位"""
        self.iam_ns_id = calc_iam_ns_id(self.cluster_id, self.name)

    @property
    def resource_id(self) -> str:
        return self.iam_ns_id


class NamespaceRequest(ResourceRequest):
    resource_type: str = ResourceType.Namespace
    attr = {'_bk_iam_path_': f'/project,{{project_id}}/cluster,{{cluster_id}}/'}

    def _make_attribute(self, res_id: str) -> Dict:
        return {
            '_bk_iam_path_': self.attr['_bk_iam_path_'].format(
                project_id=self.attr_kwargs['project_id'], cluster_id=self.attr_kwargs['cluster_id']
            )
        }

    def _validate_attr_kwargs(self):
        if not self.attr_kwargs.get('project_id'):
            raise AttrValidationError('missing project_id or project_id is invalid')

        if not self.attr_kwargs.get('cluster_id'):
            raise AttrValidationError('missing cluster_id or cluster_id is invalid')


class related_namespace_perm(decorators.RelatedPermission):

    module_name: str = ResourceType.Namespace

    def _convert_perm_ctx(self, instance, args, kwargs) -> PermCtx:
        """仅支持第一个参数是 PermCtx 子类实例"""
        if len(args) <= 0:
            raise TypeError('missing NamespacePermCtx instance argument')
        if isinstance(args[0], PermCtx):
            return NamespacePermCtx(
                username=args[0].username,
                project_id=args[0].project_id,
                cluster_id=args[0].cluster_id,
                name=args[0].name,
            )
        else:
            raise TypeError('missing NamespacePermCtx instance argument')


class namespace_perm(decorators.Permission):
    module_name: str = ResourceType.Namespace


class NamespacePermission(Permission):
    """命名空间权限"""

    resource_type: str = ResourceType.Namespace
    resource_request_cls: Type[ResourceRequest] = NamespaceRequest
    parent_res_perm = ClusterPermission()

    @related_cluster_perm(method_name='can_use')
    def can_create(self, perm_ctx: NamespacePermCtx, raise_exception: bool = True) -> bool:
        return self.can_action(perm_ctx, NamespaceAction.CREATE, raise_exception)

    @related_cluster_perm(method_name='can_view')
    def can_view(self, perm_ctx: NamespacePermCtx, raise_exception: bool = True) -> bool:
        perm_ctx.validate_resource_id()
        return self.can_action(perm_ctx, NamespaceAction.VIEW, raise_exception)

    @related_cluster_perm(method_name='can_use')
    def can_update(self, perm_ctx: NamespacePermCtx, raise_exception: bool = True) -> bool:
        perm_ctx.validate_resource_id()
        return self.can_action_with_view(perm_ctx, NamespaceAction.UPDATE, NamespaceAction.VIEW, raise_exception)

    @related_cluster_perm(method_name='can_use')
    def can_delete(self, perm_ctx: NamespacePermCtx, raise_exception: bool = True) -> bool:
        perm_ctx.validate_resource_id()
        return self.can_action_with_view(perm_ctx, NamespaceAction.DELETE, NamespaceAction.VIEW, raise_exception)

    @related_cluster_perm(method_name='can_use')
    def can_use(self, perm_ctx: NamespacePermCtx, raise_exception: bool = True) -> bool:
        perm_ctx.validate_resource_id()
        return self.can_action_with_view(perm_ctx, NamespaceAction.USE, NamespaceAction.VIEW, raise_exception)

    def make_res_request(self, res_id: str, perm_ctx: NamespacePermCtx) -> ResourceRequest:
        return self.resource_request_cls(res_id, project_id=perm_ctx.project_id, cluster_id=perm_ctx.cluster_id)

    def get_parent_chain(self, perm_ctx: NamespacePermCtx) -> List[IAMResource]:
        return [
            IAMResource(ResourceType.Project, perm_ctx.project_id),
            IAMResource(ResourceType.Cluster, perm_ctx.cluster_id),
        ]

    def get_resource_id(self, perm_ctx: NamespacePermCtx) -> Optional[str]:
        return perm_ctx.iam_ns_id
