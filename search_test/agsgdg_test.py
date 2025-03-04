from mini_search import MiniSearch

mini_search = MiniSearch()

print("添加数据")
_id = mini_search.index("test").add("常见的Rag框架", """
1. **LangChain**
   - **简介**：是一个用于开发语言相关应用程序的框架。它提供了一系列工具，可用于构建基于大型语言模型（LLM）的应用，如问答系统、聊天机器人等。
   - **特点**：
     - **模块化**：其组件包括模型、提示（Prompts）、索引（Indices）等，可以灵活组合这些模块来实现不同的功能。例如，在构建一个文档问答系统时，可以使用不同的文本分割方法（如按字符、按句子等）来创建索引，然后结合合适的提示模板和语言模型来回答问题。
     - **支持多种数据源**：能够处理多种格式的文档，如PDF、HTML、Markdown等，将这些文档转换为可用于问答的知识源。
     - **集成多种语言模型**：可以与OpenAI的GPT系列、Hugging Face的语言模型等多种模型集成，方便开发者根据需求和成本等因素选择合适的模型。
   - **应用场景**：
     - **企业知识问答系统**：企业可以将内部文档（如产品手册、规章制度等）加载到LangChain中，员工可以通过问答系统快速获取知识。
     - **智能客服系统**：结合产品知识库，快速回答客户关于产品的问题。

2. **Haystack**
   - **简介**：是一个用于构建端到端问答系统的开源框架，专注于信息检索和自然语言处理。
   - **特点**：
     - **高效的检索功能**：使用倒排索引等技术，能够快速从大量文档中检索出与问题相关的内容。例如，在一个包含大量新闻文章的知识库中，能迅速找到与特定新闻事件相关的文章段落。
     - **管道（Pipeline）架构**：允许开发者构建复杂的处理管道，包括文档预处理、检索、后处理等阶段。可以在管道中添加不同的组件，如文本清理工具、实体提取器等，来优化问答系统的性能。
     - **支持多种模型和评估指标**：与多种语言模型集成，并且提供了评估问答系统性能的指标，如准确率、召回率等，方便对系统进行优化。
   - **应用场景**：
     - **文档搜索和问答**：在法律、医疗等领域，帮助用户快速从专业文档中找到答案。例如，律师可以使用它从法律条文和案例文档中检索相关信息。
     - **语义搜索系统**：用于改善传统搜索引擎的体验，提供更符合语义的搜索结果。

3. **Weaviate**
   - **简介**：是一个开源的向量数据库和搜索引擎，它在RAG（检索增强生成）架构中起到关键的知识存储和检索作用。
   - **特点**：
     - **向量存储和检索**：将文本等数据转换为向量表示，通过计算向量相似度来检索相关内容。例如，将产品描述转换为向量，当用户询问关于产品的问题时，能够快速找到与之最相似的产品描述相关的知识。
     - **支持多种数据类型和语义关联**：不仅可以处理文本，还能处理图像、音频等多种数据类型。并且能够建立数据之间的语义关联，如在一个包含产品和用户评论的知识库中，能关联产品特性与用户评价。
     - **可扩展性和分布式架构**：适合处理大规模数据，能够在分布式环境中运行，随着数据量的增加可以方便地进行扩展。
   - **应用场景**：
     - **多模态知识管理**：在电商平台，同时管理产品图片、描述和用户反馈等信息，为用户提供更全面的产品知识问答服务。
     - **复杂知识图谱构建**：用于构建跨领域的知识图谱，整合不同类型的数据资源，实现知识的关联和检索。
""")[0]

print("查询数据")
print(mini_search.index("test").get(_id))

print("修改数据")
mini_search.index("test").set("常见的RAG框架介绍", """
常见的RAG框架介绍
1. **LangChain**
   - **简介**：是一个用于开发语言相关应用程序的框架。它提供了一系列工具，可用于构建基于大型语言模型（LLM）的应用，如问答系统、聊天机器人等。
   - **特点**：
     - **模块化**：其组件包括模型、提示（Prompts）、索引（Indices）等，可以灵活组合这些模块来实现不同的功能。例如，在构建一个文档问答系统时，可以使用不同的文本分割方法（如按字符、按句子等）来创建索引，然后结合合适的提示模板和语言模型来回答问题。
     - **支持多种数据源**：能够处理多种格式的文档，如PDF、HTML、Markdown等，将这些文档转换为可用于问答的知识源。
     - **集成多种语言模型**：可以与OpenAI的GPT系列、Hugging Face的语言模型等多种模型集成，方便开发者根据需求和成本等因素选择合适的模型。
   - **应用场景**：
     - **企业知识问答系统**：企业可以将内部文档（如产品手册、规章制度等）加载到LangChain中，员工可以通过问答系统快速获取知识。
     - **智能客服系统**：结合产品知识库，快速回答客户关于产品的问题。

2. **Haystack**
   - **简介**：是一个用于构建端到端问答系统的开源框架，专注于信息检索和自然语言处理。
   - **特点**：
     - **高效的检索功能**：使用倒排索引等技术，能够快速从大量文档中检索出与问题相关的内容。例如，在一个包含大量新闻文章的知识库中，能迅速找到与特定新闻事件相关的文章段落。
     - **管道（Pipeline）架构**：允许开发者构建复杂的处理管道，包括文档预处理、检索、后处理等阶段。可以在管道中添加不同的组件，如文本清理工具、实体提取器等，来优化问答系统的性能。
     - **支持多种模型和评估指标**：与多种语言模型集成，并且提供了评估问答系统性能的指标，如准确率、召回率等，方便对系统进行优化。
   - **应用场景**：
     - **文档搜索和问答**：在法律、医疗等领域，帮助用户快速从专业文档中找到答案。例如，律师可以使用它从法律条文和案例文档中检索相关信息。
     - **语义搜索系统**：用于改善传统搜索引擎的体验，提供更符合语义的搜索结果。

3. **Weaviate**
   - **简介**：是一个开源的向量数据库和搜索引擎，它在RAG（检索增强生成）架构中起到关键的知识存储和检索作用。
   - **特点**：
     - **向量存储和检索**：将文本等数据转换为向量表示，通过计算向量相似度来检索相关内容。例如，将产品描述转换为向量，当用户询问关于产品的问题时，能够快速找到与之最相似的产品描述相关的知识。
     - **支持多种数据类型和语义关联**：不仅可以处理文本，还能处理图像、音频等多种数据类型。并且能够建立数据之间的语义关联，如在一个包含产品和用户评论的知识库中，能关联产品特性与用户评价。
     - **可扩展性和分布式架构**：适合处理大规模数据，能够在分布式环境中运行，随着数据量的增加可以方便地进行扩展。
   - **应用场景**：
     - **多模态知识管理**：在电商平台，同时管理产品图片、描述和用户反馈等信息，为用户提供更全面的产品知识问答服务。
     - **复杂知识图谱构建**：用于构建跨领域的知识图谱，整合不同类型的数据资源，实现知识的关联和检索。
""", _id)

print(mini_search.index("test").get(_id))

print("删除数据")
mini_search.index("test").delete(_id)
print(mini_search.index("test").get(_id))
