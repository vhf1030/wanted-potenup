from mcp.server.fastmcp import FastMCP

# MCP 서버 이름
mcp = FastMCP("calculator")

# 도구 정의
@mcp.tool()
def add(a: int, b: int) -> int:
    '''
    더하기
    '''
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    '''
    곱하기
    '''
    return a * b

# MCP 서버 설정
if __name__ == "__main__":
    print('run server...')
    mcp.run(transport="stdio")
