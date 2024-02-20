import asyncio
import logging
import sys

from src.main import main

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    # asyncio.run(main())
    main()
