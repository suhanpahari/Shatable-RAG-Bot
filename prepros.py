# prepros.py
from llm_add import llm
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException


def make_results_appropriate(query, results):
    template = '''
    You are given a query and a set of results.
    Your task is to make the provided information more appropriate and relevant to the given query.
    Ensure the results directly address the query in a concise and coherent manner.

    Query: "{query}"

    Results: {results}

    Please modify the results to make them appropriate for the query.
    do not response anything else than the result.
    '''
    
    
    prompt = PromptTemplate.from_template(template)
    
    
    chain = prompt | llm
    
    
    response = chain.invoke(input={"query": query, "results": results})
    
    
    try:
        json_parser = JsonOutputParser()
        processed_response = json_parser.parse(response.content)
    except OutputParserException:
        processed_response = response.content  
    
    return processed_response
