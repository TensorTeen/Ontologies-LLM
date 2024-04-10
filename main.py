from FusekiPlugin import SparqlServer
from GeminiPlugin import *
from VectorStorePlugin import *
import re
import pandas as pd



class GetAnswer:
    def __init__(self,data_file,FusekiServerAddress="http://localhost:3030/",FusekiServerDatabase="Elements",x_col="query",y_col="sparql") -> None:
        self.FusekiServer = SparqlServer(FusekiServerAddress,FusekiServerDatabase)
        retr = AnalogicalDatabase(data_file,x_col,y_col)
        retr = retr.get_retr()
        self.final_chain = GeminiPlugin(retr)
        
            
    def get_answer(self,query,):
        sparql_query = self.clean_sparql_string(self.final_chain.get_answer(query))
        print("SPARQL Query :",sparql_query)
        out_json = self.FusekiServer.run(sparql_query)
        out_df = self.FusekiServer.parse_json(out_json)
        return out_df
        
    def clean_sparql_string(self,sparql_str):
        pattern = r'^```sparql\s*(.*?)\s*```$'
        cleaned_string = re.sub(pattern, r'\1', sparql_str, flags=re.DOTALL)
        return cleaned_string.strip()


data_file = 'data.csv'
x_col = "query"
y_col = "sparql"
df = pd.DataFrame()
df[x_col] = ["List of transition elements, their electronegativity, atomic mass, electronic structure","List of elements whose atomic radius is close to that of iron, We choose 15% as the window"]
df[y_col] = ["""PREFIX ae: <http://semantic.iitm.ac.in/AlloyOnto/Elements#>PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>SELECT ?element (str(?b) as ?number) (str(?c) as ?electronegativity)(str(?d) as ?AtomicMass) ?ElectronicStructure (str(?f) as ?group)WHERE{?element ae:is_transition_metal "true"^^xsd:boolean .OPTIONAL { ?element ae:number ?b . }OPTIONAL { ?element ae:electronegativity ?c .}OPTIONAL { ?element ae:atomic_mass ?d .}OPTIONAL { ?element ae:electronic_structure ?ElectronicStructure . }OPTIONAL { ?element ae:group ?f .}} ORDER BY ?b""","""
PREFIX ae: <http://semantic.iitm.ac.in/AlloyOnto/Elements#>PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>SELECT ?iron (str(?ri) as ?iron_radius) ?element (str(?ei) as ?element_radius) (str(abs(?ei-?ri)*100/?ei) as ?percent_diff)WHERE{?iron ae:long_name "Iron" .?element rdf:type ae:Elements .?iron ae:atomic_radius ?ri .?element ae:atomic_radius ?ei .FILTER(abs(?ei-?ri) < 0.15*?ei)}"""]
df.to_csv(data_file)

solution = GetAnswer(data_file)
