import cli.helpers.data_types as data_types
from cli.helpers.data_loader import load_all_data_files
from cli.helpers.objdict_helpers import merge_objdict
from cli.helpers.doc_list_helpers import select_first
from helpers.Step import Step


class DefaultMerger(Step):
    def __init__(self, docs):
        super().__init__(__name__)
        self.docs = docs

    def run(self):
        merged_docs = []

        for doc in self.docs:
            files = load_all_data_files(data_types.DEFAULT, doc.provider, doc.kind)
            file_with_defaults = select_first(files, lambda x: x.name == 'default')
            self.logger.info("Merging: " + doc.kind)
            merge_objdict(file_with_defaults, doc)
            merged_docs.append(file_with_defaults)

        return merged_docs

