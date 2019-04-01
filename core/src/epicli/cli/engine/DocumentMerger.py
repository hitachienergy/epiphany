import logging
import cli.helpers.data_types as data_types
from cli.helpers.data_loader import load_all_data_files
from cli.helpers.objdict_helpers import merge_objdict
from cli.helpers.doc_list_helpers import select_first

class DocumentMerger:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return

    def merge(self, docs):
        self.logger.info("Running document merger")
        merged_docs = []

        for doc in docs:
            files = load_all_data_files(data_types.DEFAULT, doc.provider, doc.kind)
            file_with_defaults = select_first(files, lambda x: x.name == 'default')
            self.logger.info("Merging doc: " + doc.kind)
            merge_objdict(file_with_defaults, doc)
            merged_docs.append(file_with_defaults)

        self.logger.info("Done merging\n")
        return merged_docs

