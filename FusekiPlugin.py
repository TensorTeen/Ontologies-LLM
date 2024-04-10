import requests
import pandas  as pd

class SparqlServer():
    def __init__(self, server,Dataset_Name):
        self.server = server
        self.Dataset_Name = Dataset_Name
        
    def send_request(self, query):
        """
        Sends a SPARQL query request to the server.

        Args:
            query (str): The SPARQL query to be sent.

        Returns:
            requests.Response: The response object containing the server's response to the query.
        """
        
        
        headers = {"Content-Type": "application/sparql-query"}
        response = requests.post(self.server + f"{self.Dataset_Name}" + "/sparql", headers=headers, data=query,verify=False)
        return response
    
    def remove_prefix(self,predicate):
        return predicate.split("#")[-1]
    
    def run(self, query):
        """
        Executes the given query and returns the response.

        Parameters:
        query (str): The query to be executed.

        Returns:
        dict: The response from the server. If the response status code is 200, it returns the JSON response.
              Otherwise, it returns a dictionary with an empty list of predicates.
        """
        
        response = self.send_request(query)
        if response.status_code == 200:
            return response.json()
        else:
            return {"predicates": []}

    def parse_json(self, data):
        
        """
         Parses the JSON object from Fuseki Server and converts it into a pandas DataFrame.

         Parameters:
         - data (dict): The JSON object to be parsed.

         Returns:
         - df (pandas.DataFrame): The parsed DataFrame."""  
               
        variable_names = data['head']['vars']

        if len(variable_names) > 1:
            df_data = {}
            for var_name in variable_names:
                df_data[var_name] = [binding[var_name]['value'].split("#")[-1] for binding in data['results']['bindings']]
            df = pd.DataFrame(df_data)
        else:
            elements = [binding['element']['value'].split("#")[-1] for binding in data['results']['bindings']]
            df = pd.DataFrame(elements, columns=variable_names)

        return df   
