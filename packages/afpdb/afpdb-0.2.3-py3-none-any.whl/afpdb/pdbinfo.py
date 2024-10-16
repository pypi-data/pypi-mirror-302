import requests

class Entry:
    def __init__(self, pdb_code):
        self.pdb_code = pdb_code
        self.api_url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_code}"
        self.metadata = self.fetch_metadata()
        self.ids=self.get_entity_ids()
        self.polymer = {}
        pid=self.get_polymer_entity_ids()
        if len(pid):
            self.polymer=self.fetch_entity_metadata(pid[0])
        exit()
        print(self.ids)

    def fetch_metadata(self):
        response = requests.get(self.api_url)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def fetch_entity_metadata(self, entity):
        api_url=f"https://data.rcsb.org/rest/v1/core/polymer_entity/{self.pdb_code}/{entity}"
        print(api_url)
        exit()
        response = requests.get(self.api_url)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_resolution(self):
        return self.metadata.get('rcsb_entry_info', {}).get('resolution_combined', [None])

    def get_model_type(self):
        return self.metadata.get('rcsb_entry_info', {}).get('experimental_method', None)

    def get_publication_date(self):
        return self.metadata.get('rcsb_entry_container_identifiers', {}).get('deposit_date', None)

    def get_release_date(self):
        return self.metadata.get('rcsb_accession_info', {}).get('initial_release_date', None)

    def get_organism(self):
        return self.polymer.get('rcsb_entity_source_organism', [{}]).get('scientific_name', None)

    def get_expression_system(self):
        return self.polymer.get('rcsb_entity_source_organism', [{}]).get('expression_system', None)

    def get_polymer_entity_ids(self):
        return self.ids.get('polymer_entity_ids', {})

    def get_entity_ids(self):
        return self.metadata.get('rcsb_entry_container_identifiers', {})

    def get_assembly_ids(self):
        return self.ids.get('assembly_ids', [])

# Example usage:
entry = Entry('1crn')
print("Resolution:", entry.get_resolution())
print("Model Type:", entry.get_model_type())
print("Publication Date:", entry.get_publication_date())
print("Release Date:", entry.get_release_date())
print("Organism:", entry.get_organism())
print("Expression System:", entry.get_expression_system())
print("Polymer Entity IDs:", entry.get_polymer_entity_ids())
print("Non-Polymer Entity IDs:", entry.get_non_polymer_entity_ids())
print("Assembly IDs:", entry.get_assembly_ids())
