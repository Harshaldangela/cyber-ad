import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import uvicorn
from enhanced_api import app

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8007)