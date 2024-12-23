import os
import sys
import io
import time
import json
from dotenv import load_dotenv
from langchain import hub
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader, JSONLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from pathlib import Path
from typing import Dict, Any
from langchain.schema import Document
import shutil


# 시작 시간 기록
# start_time = time.time()


load_dotenv()
os.getenv('OPENAI_API_KEY')
# print(f"환경 설정 완료: {time.time() - start_time:.2f}초")


sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')


# 현재 스크립트의 디렉토리를 기준으로 절대 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)  # 상위 디렉토리


# API 데이터 처리를 위한 함수 추가
def decode_api_data(encoded_data: str) -> dict:
    try:
        # base64로 디코딩하고 JSON으로 파싱
        import base64
        decoded_data = base64.b64decode(encoded_data)
        return json.loads(decoded_data)
    except Exception as e:
        print(f"API 데이터 디코딩 중 오류 발생: {str(e)}")
        return {}


# 문서 처리 방식 수정
def process_json_document(doc):
    # 제품명과 주성분을 강조하여 검색 가중치 높임
    content = f"""제품명: {doc['제품명']} {doc['제품명']} {doc['제품명']}
주성분: {doc['주성분']} {doc['주성분']}
업체명: {doc['업체명']}
효능: {doc['효능']}
사용법: {doc['사용법']}
주의사항: {doc['주의사항']}
이상반응: {doc['이상반응'] if doc['이상반응'] else ''}
약음식주의사항: {doc['약음식주의사항'] if doc['약음식주의사항'] else ''}
보관방법: {doc['보관방법'] if doc['보관방법'] else ''}"""
    
    metadata = {
        "제품명": doc['제품명'],
        "업체명": doc['업체명'],
        "주성분": doc['주성분'],
        "아이디": doc['아이디']
    }
    
    return Document(page_content=content, metadata=metadata)


# 데이터 파일 경로 설정
data_paths = [
    os.path.join(parent_dir, 'back', 'data.json')
]

# JSON 파일 구조 확인
documents = []  # documents 변수를 빈 리스트로 초기화
try:
    with open(data_paths[0], 'r', encoding='utf-8') as f:
        raw_docs = json.load(f)
    
    documents = [process_json_document(doc) for doc in raw_docs]
    
    # print(f"JSON 데이터 로딩 완료: {time.time() - start_time:.2f}초")
except Exception as e:
    print(f"JSON 데이터 로딩 중 오류 발생: {str(e)}")
    # 오류 발생 시에도 documents가 정의되어 있도록 함


# 문서가 비어있는지 확인
if not documents:
    print("문서를 가져오지 못했습니다. 프로그램을 종료합니다.")
    sys.exit(1)


# 문서 분할 시작
split_start = time.time()
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,  # 청크 크기 증가
    chunk_overlap=200,
    separators=["\n\n", "\n", ". ", ", ", " ", ""],
    length_function=len,
)
splits = text_splitter.split_documents(documents)
# print(f"문서 분할 완료: {time.time() - split_start:.2f}초, 분할된 문서 개수: {len(splits)}")


if not splits:
    print("분할된 문서가 없습니다. 프로그램을 종료합니다.")
    sys.exit(1)


# 벡터 저장소 생성/로드 로직 수정
cache_dir = os.path.join(parent_dir, 'back', 'vector_cache')
cache_file = os.path.join(cache_dir, 'index.faiss')

if os.path.exists(cache_file):
    # print("캐시된 벡터 저장소를 불러옵니다.")
    load_start = time.time()
    vectorstore = FAISS.load_local(
        cache_dir, 
        OpenAIEmbeddings(),
        allow_dangerous_deserialization=True  # 신뢰할 수 있는 로컬 캐시 파일 사용
    )
    # print(f"캐시된 벡터 저장소 로드 완료: {time.time() - load_start:.2f}초")
else:
    # print("새로운 벡터 저장소를 생성합니다.")
    create_start = time.time()
    vectorstore = FAISS.from_documents(
        documents=splits,
        embedding=OpenAIEmbeddings()
    )
    os.makedirs(cache_dir, exist_ok=True)
    vectorstore.save_local(cache_dir)
    # print(f"새로운 벡터 저장소 생성 완료: {time.time() - create_start:.2f}초")

# print(f"벡터 저장소 생성 완료: {time.time() - vector_start:.2f}초")


# 벡터 저장소 크기 확인
# try:
#     vector_count = vectorstore.index.ntotal
#     print(f"벡터 저장소에 저장된 벡터 수: {vector_count}")
# except:
#     print(f"벡터 저장소 크기를 확인할 수 없습니다.")


retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k": 5,  # 검색 결과 수를 3에서 5로 증가
        "score_threshold": 0.3,  # 유사도 임계값을 0.3에서 0.2로 낮춤
        "fetch_k": 20  # 초기 검색 결과 풀을 더 크게 설정
    }
)
# print(f"벡터 저장소 생성 완료: {time.time() - vector_start:.2f}초")


# # 벡터 저장소 상태 확인
# print(f"벡터 저장소 타입: {type(vectorstore)}")
# print(f"인덱스 타입: {type(vectorstore.index)}")
# print(f"사용 가능한 속성들: {dir(vectorstore.index)}")


prompt = PromptTemplate.from_template(
    """당신은 의약품 정보를 제공하는 전문 AI 어시스턴트입니다. 
주어진 정보에서 찾을 수 있는 정보를 사용하여 질문에 답변해 주세요.

다음 규칙을 반드시 따라주세요:
- 주어진 정보에 있는 정보만 사용하여 답변하세요
- 제품명이나 성분명이 부분적으로 일치하거나 발음이 유사한 경우에도 관련 의약품 정보를 찾아 제공하세요
- 검색어와 일치하지 않더라도 유사한 제품이 있다면 반드시 언급해 주세요
- 찾은 정보가 불완전하더라도 가능한 한 관련된 정보를 제공하세요
- 찾은 정보에 대해 다음 순서로 구조화하여 답변하세요:
  1. 제품명
  2. 업체명
  3. 주성분
  4. 효능
  5. 사용법
  6. 주의사항

#Context:
{context}

#Question:
{question}

#Answer:
"""
)


llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=1,  # 일관성을 위해 0으로 설정
)


rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)


# 응답 포맷 함수 수정
def format_response(question, answer):
    return f"""질문: {question}

답변: {answer}"""


# 질문 처리 시작
query_start = time.time()


# api_data.json 읽기
with open(os.path.join(parent_dir, 'back', 'api_data.json'), 'r') as file:
    api_data = json.load(file)['api_data']

# 하드코딩된 질문을 sys.argv에서 받아오도록 수정
if len(sys.argv) > 1:
    recieved_question = sys.argv[1]
else:
    recieved_question = "의약품에 대해 물어보세요"

answer = rag_chain.invoke(recieved_question)
print(format_response(recieved_question, answer))
# print(f"질문 처리 완료: {time.time() - query_start:.2f}초")
# print(f"전체 실행 시간: {time.time() - start_time:.2f}초")


def fix_json_file(input_path, output_path):
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # JSON 파일 파싱
        data = json.loads(content)
        
        # 올바른 형식으로 다시 저장
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print("JSON 파일이 성공적으로 수정되었습니다.")
    except json.JSONDecodeError as e:
        print(f"JSON 파싱 오류: {str(e)}")
        print(f"오류 위치: 줄 {e.lineno}, 열 {e.colno}")



