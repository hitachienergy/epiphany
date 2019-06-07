from cli.helpers.data_loader import load_all_yaml_objs, types
from cli.helpers.objdict_helpers import merge_objdict
from cli.helpers.doc_list_helpers import select_first
from cli.helpers.Step import Step


class DefaultMerger(Step):
    def __init__(self, docs):
        super().__init__(__name__)
        self.docs = docs

    def run(self):
        merged_docs = []

        for doc in self.docs:
            files_with_defaults = load_all_yaml_objs(types.DEFAULT, doc.provider, doc.kind)
            self.logger.info('Merging: ' + doc.kind+' name: '+doc.name)
            merged = self.merge_parent(files_with_defaults, doc)
            merged_docs.append(merged)

        return merged_docs

    def merge_parent(self, files, doc):
        if hasattr(doc, 'based_on'):
            self.logger.info(doc.name + ' is based on: '+doc.based_on)
            parent = select_first(files, lambda x: x.name == doc.based_on)
            merged_parent = self.merge_parent(files, parent)
            merge_objdict(merged_parent, doc)
            return merged_parent
        default_doc = select_first(files, lambda x: x.name == 'default')
        merge_objdict(default_doc, doc)
        return default_doc