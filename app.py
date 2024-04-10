import streamlit as st
import pandas as pd
from main import GetAnswer


data_file = 'data.csv'
x_col = "query"
y_col = "sparql"
df = pd.DataFrame()
df[x_col] = ["List of transition elements, their electronegativity, atomic mass, electronic structure","List of elements whose atomic radius is close to that of iron, We choose 15% as the window"]
df[y_col] = ["""PREFIX ae: <http://semantic.iitm.ac.in/AlloyOnto/Elements#>PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>SELECT ?element (str(?b) as ?number) (str(?c) as ?electronegativity)(str(?d) as ?AtomicMass) ?ElectronicStructure (str(?f) as ?group)WHERE{?element ae:is_transition_metal "true"^^xsd:boolean .OPTIONAL { ?element ae:number ?b . }OPTIONAL { ?element ae:electronegativity ?c .}OPTIONAL { ?element ae:atomic_mass ?d .}OPTIONAL { ?element ae:electronic_structure ?ElectronicStructure . }OPTIONAL { ?element ae:group ?f .}} ORDER BY ?b""","""
PREFIX ae: <http://semantic.iitm.ac.in/AlloyOnto/Elements#>PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>SELECT ?iron (str(?ri) as ?iron_radius) ?element (str(?ei) as ?element_radius) (str(abs(?ei-?ri)*100/?ei) as ?percent_diff)WHERE{?iron ae:long_name "Iron" .?element rdf:type ae:Elements .?iron ae:atomic_radius ?ri .?element ae:atomic_radius ?ei .FILTER(abs(?ei-?ri) < 0.15*?ei)}"""]
df.to_csv(data_file)
solution = GetAnswer(data_file)



def process_query(query):  
  return solution.get_answer(query)

def main():
  """Main app function"""
  st.title("Query Processor")
  query = st.text_input("Enter your query:")
  
  if st.button("Submit"):
    if query:
      try:
        # Process the query and get the dataframe
        df = process_query(query)
        st.success("Query processed successfully!")
        st.dataframe(df)
      except Exception as e:
        st.error(f"Error processing query: {e}")
    else:
      st.warning("Please enter a query.")

if __name__ == "__main__":
  main()