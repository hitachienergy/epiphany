from pathlib import Path
from typing import Any, Callable, Dict, List, Set

import yaml

from src.config.os_type import OSArch
from src.config.version import Version
from src.error import CriticalError, OldManifestVersion


def load_yaml_file_all(filename: Path) -> List[Any]:
    try:
        with open(filename, encoding="utf-8") as req_handler:
            return list(yaml.safe_load_all(req_handler))
    except yaml.YAMLError as yaml_err:
        raise CriticalError(f'Failed loading: `{yaml_err}`') from yaml_err
    except Exception as err:
        raise CriticalError(f'Failed loading: `{filename}`') from err


def load_yaml_file(filename: Path) -> Any:
    return load_yaml_file_all(filename)[0]


class ManifestReader:
    """
    Load the manifest file and call defined parser methods to process required documents.
    Main running method is :func:`~manifest_reader.ManifestReader.parse_manifest` which returns formatted manifest output.
    """

    def __init__(self, dest_manifest: Path):
        self.__dest_manifest = dest_manifest

        self.__k8s_as_cloud_service: bool = False

        self.__requested_components: Set = set()
        self.__requested_features: Set = set()

    def __parse_cluster_doc(self, cluster_doc: Dict):
        """
        Parse `epiphany-cluster` document and extract only used components.

        :param cluster_doc: handler to a `epiphany-cluster` document
        :raises:
            :class:`OldManifestVersion`: can be raised when old manifest version used
        """
        if Version(cluster_doc['version']) < Version('2.0.1'):
            raise OldManifestVersion(cluster_doc['version'])

        try:
            self.__k8s_as_cloud_service = cluster_doc['specification']['cloud']['k8s_as_cloud_service']
        except KeyError:
            self.__k8s_as_cloud_service = False

        components = cluster_doc['specification']['components']
        for component in components:
            if components[component]['count'] > 0:
                self.__requested_components.add(component)

    def __parse_feature_mappings_doc(self, feature_mappings_doc: Dict):
        """
        Parse `configuration/feature-mappings` document and extract only used features (based on `epiphany-cluster` doc).

        :param feature_mappings_doc: handler to a `configuration/feature-mappings` document
        """
        mappings = feature_mappings_doc['specification']['mappings']
        for mapping in mappings.keys() & self.__requested_components:
            for feature in mappings[mapping]:
                self.__requested_features.add(feature)

        if self.__k8s_as_cloud_service:
            self.__requested_features.add('k8s-as-cloud-service')

    def parse_manifest(self) -> Dict[str, Any]:
        """
        Load the manifest file, call parsers on required docs and return formatted output.
        """
        required_docs: Set[str] = {'epiphany-cluster', 'configuration/feature-mappings'}
        parse_doc: Dict[str, Callable] = {
            'epiphany-cluster':               self.__parse_cluster_doc,
            'configuration/feature-mappings': self.__parse_feature_mappings_doc
        }

        parsed_docs: Set[str] = set()
        for manifest_doc in load_yaml_file_all(self.__dest_manifest):
            try:
                kind: str = manifest_doc['kind']
                parse_doc[kind](manifest_doc)
                parsed_docs.add(kind)
            except KeyError:
                pass

        if len(parsed_docs) < len(required_docs):
            raise CriticalError(f'ManifestReader - could not find document(s): {parsed_docs ^ required_docs}')

        return {'requested-components': sorted(list(self.__requested_components)),
                'requested-features': sorted(list(self.__requested_features))}
