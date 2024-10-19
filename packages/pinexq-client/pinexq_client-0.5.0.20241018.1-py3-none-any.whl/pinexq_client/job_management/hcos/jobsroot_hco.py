from typing import Self

import httpx
from httpx import URL

from pinexq_client.core import MediaTypes, Link
from pinexq_client.core.hco.action_with_parameters_hco import ActionWithParametersHco
from pinexq_client.core.hco.hco_base import Hco
from pinexq_client.core.hco.link_hco import LinkHco
from pinexq_client.core.hco.unavailable import UnavailableAction, UnavailableLink
from pinexq_client.job_management.hcos.job_hco import JobLink
from pinexq_client.job_management.hcos.job_query_result_hco import (
	JobQueryResultHco,
	JobQueryResultLink
)
from pinexq_client.job_management.hcos.job_used_tags_hco import JobUsedTagsLink
from pinexq_client.job_management.known_relations import Relations
from pinexq_client.job_management.model.open_api_generated import (
	CreateJobParameters,
	JobQueryParameters,
	CreateSubJobParameters, SetJobsErrorStateParameters
)
from pinexq_client.job_management.model.sirenentities import JobsRootEntity


class CreateJobAction(ActionWithParametersHco[CreateJobParameters]):
    def execute(self, parameters: CreateJobParameters) -> JobLink:
        url: URL = self._execute_returns_url(parameters)
        link = Link.from_url(url, [str(Relations.CREATED_RESSOURCE)], "Created job", MediaTypes.SIREN)
        return JobLink.from_link(self._client, link)

    def default_parameters(self) -> CreateJobParameters:
        return self._get_default_parameters(CreateJobParameters, CreateJobParameters())


class CreateSubJobAction(ActionWithParametersHco[CreateSubJobParameters]):
    def execute(self, parameters: CreateSubJobParameters) -> JobLink:
        url = self._execute_returns_url(parameters)
        link = Link.from_url(url, [str(Relations.CREATED_RESSOURCE)], "Created sub-job", MediaTypes.SIREN)
        return JobLink.from_link(self._client, link)

    def default_parameters(self) -> CreateSubJobParameters:
        return self._get_default_parameters(CreateSubJobParameters, CreateSubJobParameters())


class JobQueryAction(ActionWithParametersHco):
    def execute(self, parameters: JobQueryParameters) -> JobQueryResultHco:
        url = self._execute_returns_url(parameters)
        link = Link.from_url(url, [str(Relations.CREATED_RESSOURCE)], "Created job query", MediaTypes.SIREN)
        # resolve link immediately
        return JobQueryResultLink.from_link(self._client, link).navigate()

    def default_parameters(self) -> JobQueryParameters:
        return self._get_default_parameters(JobQueryParameters, JobQueryParameters())


class JobSetToErrorStateAction(ActionWithParametersHco[SetJobsErrorStateParameters]):
    def execute(self, parameters: SetJobsErrorStateParameters):
        self._execute(parameters)

    def default_parameters(self) -> SetJobsErrorStateParameters:
        return self._get_default_parameters(SetJobsErrorStateParameters, SetJobsErrorStateParameters(
            message='Manually set to error state by admin',
            created_this_many_hours_ago=0,
        ))


class JobsRootHco(Hco[JobsRootEntity]):
    create_job_action: CreateJobAction | UnavailableAction
    job_query_action: JobQueryAction | UnavailableAction
    create_subjob_action: CreateSubJobAction | UnavailableAction
    used_tags_link: JobUsedTagsLink | UnavailableLink
    set_jobs_to_error_state: JobSetToErrorStateAction | UnavailableAction

    self_link: 'JobsRootLink'

    @classmethod
    def from_entity(cls, entity: JobsRootEntity, client: httpx.Client) -> Self:
        instance = cls(client, entity)

        Hco.check_classes(instance._entity.class_, ["JobsRoot"])
        instance.create_job_action = CreateJobAction.from_entity_optional(client, instance._entity, "CreateJob")
        instance.create_subjob_action = CreateSubJobAction.from_entity_optional(client, instance._entity,
                                                                                "CreateSubJob")
        instance.job_query_action = JobQueryAction.from_entity_optional(client, instance._entity, "CreateJobQuery")
        instance.used_tags_link = JobUsedTagsLink.from_entity_optional(
            instance._client, instance._entity, Relations.USED_TAGS)
        instance.self_link = JobsRootLink.from_entity(instance._client, instance._entity, Relations.SELF)
        instance.set_jobs_to_error_state = JobSetToErrorStateAction.from_entity_optional(instance._client, instance._entity,
                                                                                "SetJobsToErrorState")

        return instance


class JobsRootLink(LinkHco):
    def navigate(self) -> JobsRootHco:
        return JobsRootHco.from_entity(self._navigate_internal(JobsRootEntity), self._client)
