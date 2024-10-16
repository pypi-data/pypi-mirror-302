from mimetypes import add_type

from fastapi.encoders import jsonable_encoder
from sqlmodel import func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from mtmai.deps import CurrentUser
from mtmai.llm.embedding import embedding_hf
from mtmai.models.blog import Post
from mtmai.models.models import Document, DocumentIndex
from mtmai.models.search_index import SearchIndex, SearchIndexResponse, SearchRequest


async def create_post_search_index(db: AsyncSession, post: Post, post_content: str):
    search_index = SearchIndex(
        content_type="post",
        content_id=post.id,
        title=post.title,
        content=post_content,
    )
    db.add(search_index)
    await db.commit()
    await db.refresh(search_index)
    return search_index


async def embeding_post(*, session: AsyncSession, doc_id, content: str):
    """创建文档索引 基于大语言 embedding 的 索引（可能过时，改用 SearchIndex）"""

    # Create Document
    doc = Document(content=content)
    session.add(doc)
    await session.flush()  # Flush to get the id without committing

    embedding_model = "mixedbread-ai/mxbai-embed-large-v1"
    embedding_result = await embedding_hf(inputs=[content], model_name=embedding_model)
    doc_index = DocumentIndex(
        document_id=doc_id, embedding=embedding_result[0], emb_model=embedding_model
    )
    session.add(doc_index)


async def search_list(session: AsyncSession, req: SearchRequest):
    """
    综合搜索, 支持搜索站点, 文档, 知识库。返回搜索结果的摘要条目。
    前端，通常点击条目后，打开详细操作页
    参考： https://www.w3cschool.cn/article/34124192.html

    TODO: 可以考虑添加高亮显示的功能。
    """
    search_query = req.q
    data_type = req.dataType
    offset = req.skip
    limit = req.limit
    app = req.app or "mtmai_copilot"

    query = select(SearchIndex)

    if data_type:
        query = query.where(SearchIndex.content_type == add_type)

    if search_query:
        query = query.where(
            func.to_tsvector("english", SearchIndex.content_summary).op("@@")(
                func.plainto_tsquery("english", search_query)
            )
        )
    query = query.where(SearchIndex.is_deleted == False)
    query = query.where(SearchIndex.owner_id == CurrentUser.id)

    # 添加排序逻辑
    if search_query:
        query = query.order_by(
            func.ts_rank(
                func.to_tsvector("english", SearchIndex.content_summary),
                func.plainto_tsquery("english", search_query),
            ).desc()
        )
    else:
        # 无搜索词，按创建时间排序
        query = query.order_by(SearchIndex.created_at.desc())

    # 获取总数
    total_count = await session.scalar(
        select(func.count()).select_from(query.subquery())
    )

    query = query.offset(offset).limit(limit)

    # 获取总数

    result = await session.exec(query)
    items = result.all()

    # 查询搜索索引
    # index_sql = text("""
    # SELECT id, type, title,
    #        ts_headline('english', content, plainto_tsquery(:query)) as snippet,
    #        url,
    #        ts_rank(search_vector, plainto_tsquery(:query)) as rank
    # FROM search_index
    # WHERE search_vector @@ plainto_tsquery(:query)
    # """)

    # # 查询原始表（这里以 sites 表为例）
    # sites_sql = text("""
    # SELECT id, 'site' as type, title,
    #        left(description, 200) as snippet,
    #        url,
    #        0 as rank
    # FROM sites
    # WHERE to_tsvector('english', title || ' ' || description) @@ plainto_tsquery(:query)
    # AND id NOT IN (SELECT id FROM search_index WHERE type = 'site')
    # """)

    # # 执行查询
    # index_result = await session.exec(index_sql, {"query": query})
    # sites_result = await session.exec(sites_sql, {"query": query})

    # # 合并结果
    # all_items = [dict(row) for row in index_result.mappings()] + [dict(row) for row in sites_result.mappings()]

    # # 排序和分页
    # sorted_items = sorted(all_items, key=lambda x: x['rank'], reverse=True)
    # paginated_items = sorted_items[offset:offset+limit]

    # items = [SearchResultItem(**item) for item in paginated_items]

    # # 计算总数
    # total = len(all_items)
    # total_pages = (total + request.per_page - 1) // request.per_page

    # 使用 jsonable_encoder 确保正确序列化
    serialized_items = jsonable_encoder(items)
    return SearchIndexResponse(
        data=serialized_items,
        count=total_count,
    )
