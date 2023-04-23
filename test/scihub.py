import sys
sys.path.extend(["..", "."])

from src.paper_engine.engine.scihub import SciHub


result = SciHub.search("Design and Implementation of Multisteerable Matched Filters")
print(result)
