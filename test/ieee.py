import sys
sys.path.extend(["..", "."])

from src.paper_engine.engine.ieee import IEEE


result = IEEE.search("test")
print(result)
