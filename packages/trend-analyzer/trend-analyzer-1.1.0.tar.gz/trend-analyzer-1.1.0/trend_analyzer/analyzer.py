# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Module for performing trends analysis.

Exposes a single class TrendAnalyzer that allows to get extract trends from
vector store based on provided LLM.
"""

# pylint: disable=C0330, g-bad-import-order, g-multiple-import

from __future__ import annotations

import logging
import operator
import pathlib
import re
from typing import Final

import langchain_community
import smart_open
from langchain import chains
from langchain.chains.sql_database import prompt as sql_prompts
from langchain_community.tools.sql_database import tool as sql_database_tool
from langchain_core import (
  language_models,
  output_parsers,
  prompts,
  runnables,
  vectorstores,
)

TREND_ANALYZER_DESCRIPTION: Final[str] = """
  Operates on various tables in database and extracts topics from categories
  with such metrics as qoq_growth (quarter over quarter growth or simply
  growth), index (relative volume or size of an interest in the topic).
  Trend analyzer operates on multiple tables located in database and uses only
  data from them to answer user questions.
"""


def _format_docs(docs):
  return '\n\n'.join(doc.page_content for doc in docs)


class TrendsAnalyzer:
  """Handles prompts related to analyzing trends.

  Attributes:
    vect_store: Vector store containing data on trends.
    llm: LLM responsible to handle prompts.
    db_uri: SqlAlchemy based uri for creating DB connection.
    verbose: Whether to log intermediate steps during TrendsAnalyzer runs.
  """

  def __init__(
    self,
    vect_store: vectorstores.VectorStore,
    llm: language_models.BaseLanguageModel,
    db_uri: str,
    verbose: bool = False,
  ) -> None:
    """Initializes TrendsAnalyzer.

    Args:
      vect_store: Vector store containing data on trends.
      llm: LLM responsible to handle prompts.
      db_uri: SqlAlchemy based uri for creating DB connection.
      verbose: Whether to log intermediate steps.
    """
    self.vect_store = vect_store
    self.llm = llm
    self.db_uri = db_uri
    self.verbose = verbose

  @property
  def db(self) -> langchain_community.utilities.SQLDatabase:
    """Creates db from saved uri."""
    return langchain_community.utilities.SQLDatabase.from_uri(self.db_uri)

  @property
  def execute_query(self) -> sql_database_tool.QuerySQLDataBaseTool:
    """Tool responsible for executing SQL queries."""
    return sql_database_tool.QuerySQLDataBaseTool(db=self.db)

  def _query_cleaner(self, text: str) -> str:
    """Ensures that queries is extracted correctly from response."""
    if 'sqlquery' in text.lower() and (
      query_match := re.search('sqlquery: select .+$', text, re.IGNORECASE)
    ):
      return query_match.group(0).split(': ')[1]
    return text.split('\n')[1]

  @property
  def sql_prompt(self) -> prompts.PromptTemplate:
    """Prepared prompt to be issues to selected database."""
    prompt = sql_prompts.SQL_PROMPTS[self.db.dialect].partial(
      table_info=self.db.get_context()['table_info']
    )
    prompt_parts = prompt.template.split('Question: {input}')

    prompt_template = (
      TREND_ANALYZER_DESCRIPTION
      + prompt_parts[0]
      + '\nNever do `INNER JOIN` unless explicitly asked.'
      + '\nAlways include metric used in ORDER BY in SELECT statement.'
      + '\nQuestion: {input}'
    )
    return prompts.PromptTemplate(
      template=prompt_template,
      input_variables=prompt.input_variables,
      partial_variables=prompt.partial_variables,
    )

  @property
  def write_query(self):
    """Tool responsible for generating and cleaning SQL queries."""
    return (
      chains.create_sql_query_chain(
        llm=self.llm, db=self.db, prompt=self.sql_prompt
      )
      | self._query_cleaner
    )

  @property
  def prompt(self) -> prompts.PromptTemplate:
    """Builds correct prompt to send to LLM.

    Prompt contains format instructions to get output result.
    """
    with smart_open.open(
      pathlib.Path(__file__).resolve().parent / 'prompt_template.txt',
      'r',
      encoding='utf-8',
    ) as f:
      template = f.readlines()
    return prompts.PromptTemplate(
      template=' '.join(template),
      input_variables=['question'],
    )

  def analyze(self, text: str) -> str:
    """Performs trend analysis based on a provided question.

    Args:
      text: Question to LLM.

    Returns:
      LLM response.
    """
    question = {'question': text}
    sql_chain = runnables.RunnablePassthrough.assign(
      query=self.write_query
    ).assign(result=operator.itemgetter('query') | self.execute_query)
    if self.verbose:
      logging.info('sql_chain response: %s', sql_chain.invoke(question))
    chain = (
      sql_chain | self.prompt | self.llm | output_parsers.StrOutputParser()
    )
    if self.verbose:
      logging.info('trend analyzer chain response: %s', chain.invoke(question))
    return chain.invoke(question)
