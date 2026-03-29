import pandas as pd
import json
import numpy as np
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_groq import ChatGroq
from langchain_experimental.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent

class GroqService:
    def __init__(self):
        """
        Initializes the LangChain integration with the Groq API lazily.
        """
        self._llm = None

    def _get_llm(self):
        import os
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is missing. Please set it to use AI features.")
        if self._llm is None:
            self._llm = ChatGroq(
                model="llama-3.3-70b-versatile",
                temperature=0.1,
                max_tokens=1000,
                api_key=api_key,
            )
        return self._llm

    def analyze_csv(self, file_path):
        """
        Processes a CSV file returning schema details and the pandas DataFrame.
        """
        df = pd.read_csv(file_path)
        
        # Replace NaN with None in describe and head so it serializes to valid JSON null
        desc_df = df.describe(include='all').replace({np.nan: None})
        sample_df = df.head(3).replace({np.nan: None})
        
        # Summarize the data to give context to the LLM mappings
        schema = {
            "columns": list(df.columns),
            "types": {k: str(v) for k, v in df.dtypes.items()},
            "summary": desc_df.to_dict(),
            "sample": sample_df.to_dict(orient='records')
        }
        
        return schema, df

    def generate_chart_config(self, prompt, schema):
        """
        LangChain extraction pipeline.
        Parses user's natural language to return a valid ECharts configuration or a Metric Card configuration.
        """
        parser = JsonOutputParser()
        
        template = """
        You are an expert data visualization architect.
        A user wants to visualize their dataset based on this prompt: "{prompt}"
        
        The dataset schema and numerical summary is:
        {schema}
        
        The frontend supports two output formats:
        
        FORMAT 1: SINGLE NUMERIC METRIC (KPI CARD)
        If the user strictly asks for a single numeric value (e.g. "average of X", "maximum Y", "total count of Z"), use the `summary` data provided above to find the exact mathematical value (like `mean`, `max`, `min`, `count`).
        Return a JSON like:
        {{
            "is_metric": true,
            "title": "Average X",
            "value": "123.45"
        }}
        
        FORMAT 2: ECHARTS VISUALIZATION
        If the user asks for a chart or graph (bar, line, scatter, etc.):
        The frontend will supply the raw data directly into the ECharts `dataset.source` property as an array of JSON objects.
        DO NOT include `dataset` or `data` arrays in your JSON output. 
        Instead, you MUST use the ECharts `encode` property inside `series` to map the dataset columns to the X and Y axes.
        Return a JSON like:
        {{
            "is_metric": false,
            "tooltip": {{"trigger": "axis"}},
            "xAxis": {{"type": "category"}},
            "yAxis": {{"type": "value"}},
            "series": [{{"type": "bar", "encode": {{"x": "ExactColumnNameForX", "y": "ExactColumnNameForY"}}}}]
        }}
        Make sure the chart types match the user's intent.
        
        Respond ONLY with a valid JSON object fulfilling the {format_instructions}.
        """
        
        prompt_template = PromptTemplate(
            template=template,
            input_variables=["prompt", "schema"],
            partial_variables={"format_instructions": parser.get_format_instructions()}
        )
        
        chain = prompt_template | self._get_llm() | parser
        
        return chain.invoke({
            "prompt": prompt, 
            "schema": json.dumps(schema)
        })

    def query_data(self, question, df):
        """
        Data Q&A bot using LangChain's Pandas DataFrame agent.
        It runs Python code against the pandas dataframe to find the answer.
        """
        try:
            agent = create_pandas_dataframe_agent(
                self._get_llm(),
                df,
                verbose=False,
                agent_type="tool-calling",
                allow_dangerous_code=True
            )

            result = agent.invoke({"input": question})
            return result.get("output", result.get("answer", "No answer could be determined."))
        except Exception:
            # Fallback path for restrictive/cloud runtimes where agent execution may fail.
            sample_rows = df.head(25).replace({np.nan: None}).to_dict(orient='records')
            schema = {k: str(v) for k, v in df.dtypes.items()}

            fallback_prompt = f"""
            You are a data analyst. Answer the user's question using ONLY the provided dataframe context.

            User question:
            {question}

            Dataframe schema:
            {json.dumps(schema)}

            Dataframe sample rows (up to 25 rows):
            {json.dumps(sample_rows)}

            Rules:
            - If the answer cannot be determined reliably from the provided sample, say that clearly.
            - Keep the answer concise and factual.
            """

            fallback_res = self._get_llm().invoke(fallback_prompt)
            content = getattr(fallback_res, "content", None)
            return content if content else "I could not determine a reliable answer from the available data sample."
