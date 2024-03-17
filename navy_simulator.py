import logging
from navy_manager import *

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def main() -> None:
    print("Start simulator")
    start_simulation_manager = Navy_manager().start()

if __name__ == '__main__':
    main()