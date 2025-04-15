import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

load_dotenv()

# LLM 모델 설정
model = ChatOpenAI(model="gpt-4o-mini")

# MCP 서버 실행을 위한 파라미터 설정
server_params = StdioServerParameters(
    command="python",
    args=["C:/wanted/practice_MCP/basic_server.py"]
)

# 클라이언트 비동기 실행
async def main():
    async with stdio_client(server_params) as (read, write):
        
        async with ClientSession(read, write) as session:
    
            await session.initialize()
            
            tools = await load_mcp_tools(session)
            agent = create_react_agent(model, tools)
            # agent_response = await agent.ainvoke({"messages": [{"role": "user", "content": "'6 + 7 * 5'를 계산해줘"}]})            
            agent_response = await agent.ainvoke({"messages": "6 + 7 * 5 를 구하시오"})
            
            print(agent_response)
            
            
if __name__ == "__main__":
    asyncio.run(main())
    